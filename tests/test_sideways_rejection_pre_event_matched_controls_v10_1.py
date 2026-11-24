import unittest
import numpy as np
import pandas as pd
from research.sideways_rejection_pre_event_matched_controls_v4 import COVARIATES
from research.sideways_rejection_pre_event_matched_controls_v10_1 import correlation_diagnostics

class V101CorrelationTests(unittest.TestCase):
    def test_constant_columns_excluded_and_counted(self):
        d={c:np.arange(10,dtype=float) for c in COVARIATES}
        d[COVARIATES[0]]=np.ones(10)
        f=pd.DataFrame(d); f["asset"]="BTC"; f["direction"]="upper"; f["definition"]="broad"; f["sequence_class"]="SEPARATION_FIRST"
        s,p=correlation_diagnostics(f,("asset","direction"),"test")
        self.assertEqual(s.iloc[0].constant_or_insufficient_covariate_count,1)
        self.assertEqual(s.iloc[0].variable_covariate_count,len(COVARIATES)-1)
        self.assertTrue(np.isfinite(s.iloc[0].correlation_effective_rank_nonconstant))
        self.assertEqual(len(p),(len(COVARIATES)-1)*(len(COVARIATES)-2)//2)
    def test_perfectly_correlated_columns_reported(self):
        d={c:np.arange(12,dtype=float)**2 for c in COVARIATES}
        f=pd.DataFrame(d); f["asset"]="ETH"; f["direction"]="lower"; f["definition"]="broad"
        s,p=correlation_diagnostics(f,("asset","direction"),"test")
        self.assertGreaterEqual(s.iloc[0].pairs_abs_ge_0_90,1)
        self.assertTrue((p.abs_correlation<=1.0000001).all())
    def test_single_variable_has_undefined_effective_rank(self):
        d={c:np.ones(8) for c in COVARIATES}; d[COVARIATES[0]]=np.arange(8,dtype=float)
        f=pd.DataFrame(d); f["asset"]="SOL"; f["direction"]="upper"
        s,_=correlation_diagnostics(f,("asset","direction"),"test")
        self.assertEqual(s.iloc[0].variable_covariate_count,1)
        self.assertTrue(pd.isna(s.iloc[0].correlation_effective_rank_nonconstant))
if __name__=="__main__": unittest.main()
