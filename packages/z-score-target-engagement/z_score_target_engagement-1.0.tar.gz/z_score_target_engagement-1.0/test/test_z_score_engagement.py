import unittest
# import pandas as pd # type: ignore
from z_score_engagement import *


class ZScoreAnalyzerTest(unittest.TestCase):

    test_df_path = "testdf.csv"
    testdf = pd.read_csv("testdf.csv")
    a = ZScoreAnalyzer(test_df_path, debug=True, verbose=False)

    #TODO: test batch loading and groupby


    def test_load_peptide_df(self):
        self.a = ZScoreAnalyzer(self.test_df_path, debug=True, verbose=False)
        a = self.a
        self.assertTrue(isinstance(a.pep_df, pd.DataFrame))
        self.assertEqual(a.pep_df.shape, (101, 102))

        a = ZScoreAnalyzer(self.test_df_path, protein_id="Q13889", debug=True, verbose=False)
        self.assertEqual(len(set(a.pep_df["Protein.Ids"].to_list())), 1)

        a = ZScoreAnalyzer(self.test_df_path, target="TEX30", debug=True, verbose=False)
        self.assertEqual(len(set(a.pep_df["Genes"].to_list())), 1)
        

    def test_get_quant_cols(self):
        a = self.a
        cols = a.get_quant_cols()
        self.assertTrue(isinstance(cols, list))
        self.assertEqual(len(cols), 99)
        self.assertTrue(a.quant_cols is not None)

    def test_log_transform(self):
        a = ZScoreAnalyzer(self.test_df_path, debug=True, verbose=False)
        quant_cols = a.get_quant_cols()
        quant_pep_df = a.pep_df.replace({None: np.nan,
                                             0: np.nan})
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols].astype(float))
        self.assertAlmostEqual(quant_pep_df[quant_cols].median().median(), 9.541170362453595)
    
    def test_median_normalize(self):
        a = self.a
        quant_cols = a.get_quant_cols()
        quant_pep_df = a.pep_df.replace({None: np.nan,
                                             0: np.nan})
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols].astype(float))
        melt_df = quant_pep_df.melt(id_vars=["Protein.Ids", "Genes", "Precursor.Id"], var_name="Compound", value_name="Log Abundance")
        pivoted_df = melt_df.pivot(index="Compound", columns=["Precursor.Id", "Genes", "Protein.Ids"], values="Log Abundance")
        normalized = a.median_normalize(pivoted_df)
        self.assertEqual(normalized[normalized.columns[1:]].median().median(), 0)

    def test_get_compound_name(self):
        test_names = ['MSR2156_SET1REP2A4_TAL0000738_DIA.d',
                      'MSR2154_SET1REP2A2_NUC1_DIA.d',
                      'MSR2154_SET1REP2A2_NUC_DIA.d',
                      'MSR2156_SET1REP2A4_TAL738_DIA.d',
                      'MSR6631_SET1REP2A1_FRA12000_DIA.d']
        correct_output = ['TAL738', 'NUC1', 'NUC', 'TAL738', 'FRA']
        result = [self.a.get_compound_name(name) for name in test_names]
        self.assertEqual(result, correct_output)

        num = self.a.get_tal_int("TAL00000789")
        notnum = self.a.get_tal_int("NOTNUM")
        self.assertEqual(num, 789)
        self.assertEqual(notnum, "NOTNUM")

    def test_get_z_score_df(self):
        a = ZScoreAnalyzer(self.test_df_path, debug=True, verbose=False)
        self.pep_df = a.process_pep_df()
        self.z_score = a.get_z_score_df()
        self.assertEqual(self.z_score.shape, (88, 64))
        zeros = list(np.zeros(64))
        self.assertEqual(self.z_score.median().to_list(), zeros)
    
    def test_get_full_hit_df(self):
        a = ZScoreAnalyzer(self.test_df_path, verbose=False)
        hit_df = a.get_full_hit_df()
        self.assertEqual(hit_df.shape, (5162, 5))
        names = ['Compound', 'Precursor.Id', 'Genes', 'Protein.Ids', 'Z Score']
        values = ['TAL743', 'AAEC(UniMod:4)NIVVTQPR2', 'DHX9', 'Q08211', -23.292744577395002]
        testSeries = pd.Series(values, index=names)
        self.hit_df = hit_df
        self.assertEqual((testSeries == hit_df.iloc[0]).sum(), 5)
    
    def test_get_hit_df(self):
        a = ZScoreAnalyzer(self.test_df_path, verbose=False)
        df = a.get_hit_df(threshold=-5)
        self.assertEqual(df.shape, (58,5))
        self.assertEqual((df['Z Score'] < -5).sum(), 58)
        c_df = a.get_hit_df(threshold=-5, residue='C')
        self.assertEqual((c_df['Z Score'] < -5).sum(), 33)
        def c_in_peptide(peptide):
            return "C" in peptide
        contains_c = c_df["Precursor.Id"].apply(c_in_peptide).sum()
        self.assertEqual(contains_c, 33)



if __name__ == '__main__':
    unittest.main(warnings="ignore")