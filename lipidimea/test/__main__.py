"""
lipidimea/test/__main__.py

Dylan Ross (dylan.ross@pnnl.gov)

    runs unit tests, imports defined test cases from all of the
    individual test modules
"""


import unittest


from lipidimea.test.msms._util import (
    TestMS2ToStr, TestStrToMS2, TestApplyArgsAndKwargs, TestPPMFromDeltaMz, TestTolFromPPM
)
from lipidimea.test.msms.dda import (
    Test_MSMSReaderDDA, Test_MSMSReaderDDACached, Test_ExtractAndFitChroms, 
    Test_ConsolidateChromFeats, Test_ExtractAndFitMs2Spectra, Test_AddPrecursorsAndFragmentsToDb,
    TestExtractDdaFeatures, TestConsolidateDdaFeatures
)
from lipidimea.test.msms.dia import (
    Test_SelectXicPeak, Test_LerpTogether, Test_DeconDistance, Test_DeconvoluteMs2Peaks,
    Test_AddSingleTargetResultsToDb, Test_Ms2PeaksToStr, Test_SingleTargetAnalysis, 
    TestExtractDiaFeatures, TestAddCalibratedCcsToDiaFeatures
)
from lipidimea.test.annotation import (
    TestDefaultSumCompLipidDBConfigs,
    TestSumCompLipidDB, TestRemoveLipidAnnotations, Test_AnnotateLipidsSumComposition, 
    Test_FilterAnnotationsByRTRange, Test_UpdateLipidIDsWithFragRules,
    TestAnnotateLipids
)
from lipidimea.test.util import (
    TestCreateResultsDb, TestDebugHandler
)
from lipidimea.test.params import (
    TestLoadParams, TestLoadDefaultParams, TestSaveParams
)


if __name__ == '__main__':
    # run all imported TestCases
    unittest.main(verbosity=2)
