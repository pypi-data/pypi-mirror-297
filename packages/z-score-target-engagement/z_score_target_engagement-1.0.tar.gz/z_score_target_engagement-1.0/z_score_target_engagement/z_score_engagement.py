import re
import matplotlib.pyplot as plt
import polars as pl
import pandas as pd
import numpy as np
import boto3
from dataclasses import dataclass

# Turn off annoying pandas warnings
pd.options.mode.chained_assignment = None
pd.set_option("future.no_silent_downcasting", True)
from warnings import simplefilter, catch_warnings
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def get_batches(pg_path):
    lazy_df = pl.scan_csv(pg_path,
                        separator="\t",
                        # storage_options=self.get_storage_options(),
                        infer_schema_length=10000,
                        )
    column_names = lazy_df.collect_schema().names()
    batches = []
    for column in column_names:
        batch = re.search(r'SET\d+(-\d+)?REP\d+(-\d+)?', column)
        if isinstance(batch, re.Match):
            batches.append(batch[0])
    batches = list(set(batches))
    return batches

@dataclass
class ZScoreAnalyzer():
    path: str
    protein_id: str = None
    batch_id: str = None
    target: str = None
    verbose: bool = True
    compounds: list[int] = None
    quant_cols: list[str] = None
    pep_df: pd.DataFrame = None # Raw pr_matrix
    z_scores: pd.DataFrame = None
    peptides: list[str] = None # type: ignore
    c_peptides: list[str] = None
    hit_df: pd.DataFrame = None 
    debug: bool = False
    dropna_portion: float = 0.5

    def __post_init__(self):
        if self.verbose:
            print("Loading pr matrix file...")
        self.load_peptide_df() # Load in raw pr_matrix for protein of iterest
        self.get_quant_cols()
        if not self.debug:
            self.z_scores = self.get_z_score_df()
            
            self.get_full_hit_df()
            if self.verbose:
                print("Done")
        return self

    def load_peptide_df(self):
        path = self.path
        if path.endswith(".tsv"):
            sep = "\t"
        elif path.endswith(".csv"):
            sep = ","
        lazy_df = pl.scan_csv(path,
                        separator=sep,
                        storage_options=self.get_storage_options(),
                        infer_schema_length=10000,
                        )
        
        # If provided, filter for either protein ID for gene name
        if self.protein_id is not None:
            lazy_df = lazy_df.filter(pl.col("Protein.Ids").str.contains(self.protein_id))#.collect(streaming=True).to_pandas()
        elif self.target is not None:
            lazy_df = lazy_df.filter(pl.col("Genes").str.contains(self.target))#.collect(streaming=True).to_pandas()

        # We always want these columns:
        identifier_columns = ["Protein.Ids", "Genes", "Precursor.Id"]
        # Collect all column names for filtering
        all_columns = lazy_df.collect_schema().names()

        # If a batchnum is provided, isolate the columns containing the batchnum. Otherwise, add on all abundance cols
        if self.batch_id is not None:
            column_names = identifier_columns + [col for col in all_columns if self.batch_id in col]
        else:
            column_names = identifier_columns + [col for col in all_columns if col.endswith(".d")]
        
        # Collect the df
        if column_names is not None: # Selec
            pep_df = lazy_df.select(column_names).collect(streaming=True).to_pandas()
        else: # Load in the whole thing!
            pep_df = lazy_df.collect(streaming=True).to_pandas()

        # Simplify protein ids. eg. P52701;P52701-2;P52701-3  -> P52701
        def process_protein_id(protein_id):
            return protein_id.split(";")[0]
        pep_df["Protein.Ids"] = pep_df["Protein.Ids"].apply(process_protein_id)

        # Group by gene
        pep_df = pep_df.sort_index(axis=1, level="Genes")

        self.pep_df = pep_df

        return pep_df

    def get_quant_cols(self):
        quant_cols =  [col for col in self.pep_df.columns if col.endswith(".d")]
        self.quant_cols = quant_cols
        return self.quant_cols
    
    def process_pep_df(self):
        if self.verbose:
            print("Processing .tsv file...")
        # Isolate quantitative columns
        quant_cols = self.get_quant_cols()
        ####quant_pep_df = self.pep_df[["Precursor.Id"] + quant_cols]

        # Log transform 
        quant_pep_df = self.pep_df.replace({None: np.nan,
                                             0: np.nan})
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols].astype(float))

        # Restructure df so columns are peptides
        melt_df = quant_pep_df.melt(id_vars=["Protein.Ids", "Genes", "Precursor.Id"], var_name="Compound", value_name="Log Abundance")
        pivoted_df = melt_df.pivot(index="Compound", columns=["Precursor.Id", "Genes", "Protein.Ids"], values="Log Abundance")
                
        # Median normalize by batch, eg REP1SET1
        normalized_df = self.median_normalize(pivoted_df)

        # Replace filenames with compound names
        normalized_df.reset_index(inplace=True) # expose compound column
        normalized_df['Compound'] = normalized_df["Compound"].apply(self.get_compound_name)

        if self.compounds is not None:
            # If provided with specific compounds of interst, isolate them
            normalized_df['Compound'] =  normalized_df["Compound"].apply(self.get_tal_int)
            filtered = normalized_df.loc[normalized_df["Compound"].isin(self.compounds)]
        else:
            # Remove positive and fractionation controls
            normalized_df = normalized_df.loc[~normalized_df["Compound"].isin(["NUC1", "NUC2", "NUC", "dBET6"])]
            filtered = normalized_df.loc[~normalized_df["Compound"].str.contains("FRA")]

        filtered.index = filtered["Compound"] # Add compound back as the index
        filtered = filtered.drop(columns=("Compound", "", ""))  # Drop the compound column

        return filtered
    
    def median_normalize(self, pivoted_df):
        # Take a df with peptides as columns and normalize by batch
        peptides = pivoted_df.columns.to_list()

        def get_batch_num(filename):
            batch = re.search(r'SET\d+(-\d+)?REP\d+(-\d+)?', filename)
            return batch[0]
        
        def subtract_batch_median(group):
            median = group[peptides].median().median()
            group[peptides] = group[peptides] - median
            return group
        
        if self.batch_id is None:
            # If no batch id is provided, then data probably comes from multiple batches so we'll need to group
            # by batch to normalize
            pivoted_df.reset_index(inplace=True) # expose filenames/compound
            pivoted_df["batch"] = pivoted_df["Compound"].apply(get_batch_num) # extract batch num from filename
            
            normalized_df = pivoted_df.groupby("batch").apply(subtract_batch_median, include_groups=False)#.reset_index()
            normalized_df.reset_index(inplace=True)
            normalized_df = normalized_df.drop(columns=[("batch", '',''), ('level_1', '','')])
        else: 
            # If batch id is provided, then we've already grouped by batch and we can just subtract the median
            median = pivoted_df.median().median()
            normalized_df = pivoted_df - median
        return normalized_df


    def get_tal_int(self, s):
        # Turn a string, "TAL###" into an int
        try:
            num = int(re.findall(r'\d+', s)[0])
            return num
        except IndexError: # No numbers in the string
            return s
    
    def get_tal_str(self, num):
        # Turn and int, ###, into a string "TAL###"
        return "TAL" + str(num)

    def get_compound_name(self, s: str) -> str:
        """
        Extracts the compound name from the name of the file.
    
        Parameters
        ----------
        s: str
            An entry from the "Filename" column, a path to where the file is located
        
        Returns
        -------
        str
            The name of the treatment compound
        """
        # Look for compounds with the name TAL####
        if "TAL" in s.upper():
            tal_num = re.search(r'TAL\d+(-\d+)?', s)[0]
            # Strip leading zeros if present
            num = int(re.search(r'\d+(-\d+)?', tal_num)[0])
            new_name = "TAL" + str(num)
            return new_name
        elif "DMSO" in s.upper():
            return "DMSO"
        elif "PRTC" in s.upper():
            return "PRTC"
        elif "nuclei" in s.lower():
            return "NUC"
        elif "nuc" in s.lower(): # cases where it is labeled as NUC2
            nuc_num = re.search(r'NUC\d+(-\d+)?', s)
            if nuc_num is None:
                return "NUC"
            else:
                return nuc_num[0]
        elif "dbet" in s.lower():
            return "dBET6"
        elif "FRA" in s.upper():
            return "FRA"
        elif "none" in s.lower():
            return "None"
        else:
            print(f"Unable to extract compound name from filename {s}.")
            name = input("Input the compound name here: ")
            return name
    
    def get_z_score_df(self):
        if self.z_scores is not None:
            return self.z_scores
        if self.verbose:
            print("Calculating Z scores...")
        df = self.process_pep_df()
        df = df.dropna(axis=1, thresh=df.shape[0]*self.dropna_portion)

        def get_MAD(data_series):
            # Get the median absolute deviation (MAD) from a pandas data series
            return abs(data_series - data_series.median()).median()
        
        for peptide in df.columns:
            MAD = get_MAD(df[peptide])
            df[peptide] = (df[peptide] - df[peptide].median())/MAD
        
        # If compounds specified, turn ints back to strings
        if self.compounds is not None:
            df = df.reset_index()
            df["Compound"] = df["Compound"].apply(self.get_tal_str)
            df.index = df["Compound"]
            df = df.drop(columns="Compound")

        df = df.dropna(axis=1, thresh=df.shape[0]*self.dropna_portion) # drop columns where more than given portion are nan (default 0.5)

        # Store peptdies and cysteine peptides
        self.peptides = df.columns.get_level_values(0).to_list()
        self.c_peptides = [col for col in self.peptides if "C" in col]
        
        self.z_scores = df
        return df
    
    def get_full_hit_df(self):
        if self.verbose:
            print("Pivoting Z score dataframe...")
        z_reset = self.z_scores.reset_index()
        melted_df = z_reset.melt(id_vars=[("Compound","","")],
                                value_name="Z Score")
        melted_df = melted_df.rename(columns={('Compound', '', ''):"Compound"})
        hit_df = melted_df.sort_values(by="Z Score")
        hit_df = hit_df[hit_df["Z Score"].notna()].reset_index(drop=True)
        self.hit_df = hit_df
        return self.hit_df
    
    def get_hit_df(self,
                   threshold=None,
                   residue=None):
        if self.hit_df is None:
            full_hit_df = self.get_full_hit_df()
        else:
            full_hit_df = self.hit_df
        if residue is not None:
            full_hit_df = full_hit_df.loc[full_hit_df["Precursor.Id"].str.contains(residue)]
        if threshold is not None:
            full_hit_df = full_hit_df.loc[full_hit_df["Z Score"] < threshold]
        return full_hit_df.sort_values(by="Z Score").reset_index(drop=True)


    def plot_all_z_scores(self,
                          threshold=None,
                          title=None,
                          save_path=None,
                          residue=None):
        z_df = self.z_scores
        peptides = z_df.columns.to_list()
        if residue is not None:
            peptides = [pep for pep in peptides if residue in pep]
        for peptide in peptides:
            scores = z_df[peptide]
            plt.scatter([peptide[0]]*len(scores), scores)
        if threshold is not None:
            plt.axhline(y=threshold,
                        color="red",
                        linestyle="dashed")
        plt.xticks(rotation=90)
        plt.ylabel("Robust Z Score")
        if title is None:
            plt.title("Abundance Z Score")
        else:
            plt.title(title)
        if save_path is not None:
            plt.savefig(save_path)
        plt.show()

    def plot_peptide_z_score(self, 
                             peptide, 
                             threshold=None,
                             highlight_hits=False,
                             save_path=None,
                             label_compounds=False,
                             color_by_compound=False,
                             title=None, 
                             plot_threshold=False):
        z_df = self.z_scores
        z_score = z_df[peptide]
        compound = z_score.index.to_list()

        if color_by_compound:
            # Plot compound by compound to get different colors
            for c in compound:
                c_zscore = z_score.loc[z_score.index==c]
                label = c_zscore.index.to_list()
                plt.scatter(label, c_zscore)
        else: # plot everything at once, same color
            plt.scatter(compound, z_score)

        if label_compounds:
            plt.xticks(compound, rotation=90)
        else:
            # Otherwise remove xticks to avoid crowding
            plt.tick_params(
                            axis='x',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            bottom=False,      # ticks along the bottom edge are off
                            top=False,         # ticks along the top edge are off
                            labelbottom=False)
            
        if highlight_hits:
            hits = z_score[z_score < threshold].dropna()
            plt.scatter(hits.index.to_list(), hits, color="red")
            plt.xticks(hits.index.to_list(), rotation=90)
            # Plot other instances of that compound
            for compound in hits.index.to_list():
                score = z_score.loc[z_score.index==compound]
                plt.scatter([compound]*len(score), score, color="red")

        if plot_threshold:
            plt.axhline(y=threshold,
                        color="red",
                        linestyle="dashed")
            
        if title is not None:
            plt.title(title)
        else:
            plt.title(f"Robust Z Score\nPeptide {peptide}")

        plt.ylabel("Robust Z Score")
        # plt.xlabel("Run")
        if save_path is not None:
            plt.savefig(save_path)

        plt.show()
    

    def get_num_false_hit(self,
                          hit_df=None,
                          threshold=None,
                          residue=None):
        if hit_df is None:
            hit_df = self.hit_df
        if threshold is not None:
            hit_df = hit_df.loc[hit_df["Z Score"]<threshold]
        if residue is not None:
            hit_df = hit_df.loc[hit_df["Precursor.Id"].str.contains(residue)]
        return hit_df.loc[hit_df["Compound"]=="DMSO"]["Z Score"].count(), hit_df.shape[0]

    def plot_false_hits(self,
                 hit_df=None,
                 residue=None,
                 save_path=None):
        if hit_df is None:
            hit_df = self.hit_df
        lower = hit_df["Z Score"].min()
        upper = hit_df["Z Score"].max()
        thresholds = list(np.linspace(lower, upper, 50))
        num_false_hit = []
        for i in thresholds:
            num_false_hit.append(self.get_num_false_hit(hit_df=hit_df, threshold=i, residue=residue)[0])
        plt.scatter(thresholds, num_false_hit)
        plt.title("Number of False DMSO Hits")
        plt.ylabel("Num False Hits")
        plt.xlabel("Z Score Cutoff")
        if save_path is not None:
            plt.savefig(save_path)
        plt.show()

    def get_storage_options(self) -> dict[str, str]:
        """Get AWS credentials to enable polars scan_parquet functionality.

        It's kind of annoying that this is currently necessary, but here we are...
        """
        credentials = boto3.Session().get_credentials()
        return {
            "aws_access_key_id": credentials.access_key,
            "aws_secret_access_key": credentials.secret_key,
            "session_token": credentials.token,
            "aws_region": "us-west-2",
        }


