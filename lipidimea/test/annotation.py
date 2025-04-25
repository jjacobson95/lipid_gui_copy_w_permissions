"""
lipidimea/test/annotation.py
Dylan Ross (dylan.ross@pnnl.gov)

    tests for the lipidimea/annotation.py module
"""


import os
import unittest
import tempfile
import sqlite3

from lipidimea.util import create_results_db
from lipidimea.params import AnnotationParams
from lipidimea.annotation import (
    DEFAULT_SCDB_CONFIG, 
    DEFAULT_RP_RT_RANGE_CONFIG,
    DEFAULT_LITERATURE_CCS_TREND_PARAMS,
    SumCompLipidDB,
    remove_lipid_annotations, 
    annotate_lipids_sum_composition, 
    filter_annotations_by_rt_range, 
    filter_annotations_by_ccs_subclass_trend,
    update_lipid_ids_with_frag_rules,
    annotate_lipids
)


# Use the default annotation params for tests
_ANNOTATION_PARAMS = AnnotationParams.load_default()
# except, set the ionization mode to POS
_ANNOTATION_PARAMS.ionization = "POS"


class TestDefaultConfigs(unittest.TestCase):
    """ tests for built in default config files """

    def test_sum_comp_db_configs_exist(self): 
        """ ensure built in sum comp lipid DB config files (POS and NEG) exist """
        self.assertTrue(os.path.isfile(DEFAULT_SCDB_CONFIG["POS"]))
        self.assertTrue(os.path.isfile(DEFAULT_SCDB_CONFIG["NEG"]))

    def test_rt_range_config_exists(self):
        """ ensure the built in default RT ranges config file exists """
        self.assertTrue(os.path.isfile(DEFAULT_RP_RT_RANGE_CONFIG))

    def test_ccs_trend_config_exists(self):
        """ ensure the built in default CCS literature trends config file exists """
        self.assertTrue(os.path.isfile(DEFAULT_LITERATURE_CCS_TREND_PARAMS))


class TestSumCompLipidDB(unittest.TestCase):
    """ tests for the SumCompLipidDB class """

    def test_gen_sum_compositions_one_chain(self):
        """ test the sum compoisition generator with single chain """
        scdb = SumCompLipidDB()
        expected_compositions = [
            (12, 0), (12, 1), (12, 2), 
            (13, 0), (13, 1), (13, 2), 
            (14, 0), (14, 1), (14, 2),
            (15, 0), (15, 1), (15, 2),
            (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), 
            (17, 0), (17, 1), (17, 2), (17, 3), (17, 4),  
            (18, 0), (18, 1), (18, 2), (18, 3), (18, 4),  
            (19, 0), (19, 1), (19, 2), (19, 3), (19, 4),  
            (20, 0), (20, 1), (20, 2), (20, 3), (20, 4), 
            (21, 0), (21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6),
            (22, 0), (22, 1), (22, 2), (22, 3), (22, 4), (22, 5), (22, 6),
            (23, 0), (23, 1), (23, 2), (23, 3), (23, 4), (23, 5), (23, 6),
            (24, 0), (24, 1), (24, 2), (24, 3), (24, 4), (24, 5), (24, 6),
        ]
        compositions = [_ for _ in scdb.gen_sum_compositions(1, 12, 24, True)]
        # make sure all of the expected compositions are produced
        for comp in expected_compositions:
            self.assertIn(comp, compositions, f"expected composition not generated: {comp}")
        # make the comparison the other way to make sure unexpected 
        # compositions are not produced
        for comp in compositions:
            self.assertIn(comp, expected_compositions, f"genrated unexpected composition: {comp}")
    
    def test_gen_sum_compositions_two_chains(self):
        """ test the sum compoisition generator with two chains """
        scdb = SumCompLipidDB()
        expected_compositions = [
            (32, 0), (32, 1), (32, 2), (32, 3), (32, 4), (32, 5), (32, 6), (32, 7), (32, 8),
            (34, 0), (34, 1), (34, 2), (34, 3), (34, 4), (34, 5), (34, 6), (34, 7), (34, 8),
            (36, 0), (36, 1), (36, 2), (36, 3), (36, 4), (36, 5), (36, 6), (36, 7), (36, 8),
        ]
        compositions = [_ for _ in scdb.gen_sum_compositions(2, 16, 18, False)]
        # make sure all of the expected compositions are produced
        for comp in expected_compositions:
            self.assertIn(comp, compositions)
        # make the comparison the other way to make sure unexpected 
        # compositions are not produced
        for comp in compositions:
            self.assertIn(comp, expected_compositions)

    def test_gen_sum_compositions_three_chains(self):
        """ test the sum compoisition generator with three chains """
        scdb = SumCompLipidDB()
        expected_compositions = [
            (36, 0), (36, 1), (36, 2), (36, 3), (36, 4), (36, 5), (36, 6),
            (37, 0), (37, 1), (37, 2), (37, 3), (37, 4), (37, 5), (37, 6),
            (38, 0), (38, 1), (38, 2), (38, 3), (38, 4), (38, 5), (38, 6),
            (39, 0), (39, 1), (39, 2), (39, 3), (39, 4), (39, 5), (39, 6),
            (40, 0), (40, 1), (40, 2), (40, 3), (40, 4), (40, 5), (40, 6),
            (41, 0), (41, 1), (41, 2), (41, 3), (41, 4), (41, 5), (41, 6),
            (42, 0), (42, 1), (42, 2), (42, 3), (42, 4), (42, 5), (42, 6),
        ]
        compositions = [_ for _ in scdb.gen_sum_compositions(3, 12, 14, True)]
        # make sure all of the expected compositions are produced
        for comp in expected_compositions:
            self.assertIn(comp, compositions)
        # make the comparison the other way to make sure unexpected 
        # compositions are not produced
        for comp in compositions:
            self.assertIn(comp, expected_compositions)

    def test_override_max_u_method(self):
        """ test overriding the max_u static method and generating sum compositions """
        scdb = SumCompLipidDB()
        # override max_u with a different function
        def new_max_u(c):
            return 2 if c < 15 else 4
        scdb.max_u = new_max_u
        expected_compositions = [
            (12, 0), (12, 1), (12, 2), 
            (13, 0), (13, 1), (13, 2), 
            (14, 0), (14, 1), (14, 2),
            (15, 0), (15, 1), (15, 2), (15, 3), (15, 4),
            (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), 
            (17, 0), (17, 1), (17, 2), (17, 3), (17, 4),  
            (18, 0), (18, 1), (18, 2), (18, 3), (18, 4),  
            (19, 0), (19, 1), (19, 2), (19, 3), (19, 4),  
            (20, 0), (20, 1), (20, 2), (20, 3), (20, 4),
            (21, 0), (21, 1), (21, 2), (21, 3), (21, 4),
            (22, 0), (22, 1), (22, 2), (22, 3), (22, 4),
            (23, 0), (23, 1), (23, 2), (23, 3), (23, 4),
            (24, 0), (24, 1), (24, 2), (24, 3), (24, 4),
        ]
        compositions = [_ for _ in scdb.gen_sum_compositions(1, 12, 24, True)]
        # make sure all of the expected compositions are produced
        for comp in expected_compositions:
            self.assertIn(comp, compositions)
        # make the comparison the other way to make sure unexpected 
        # compositions are not produced
        for comp in compositions:
            self.assertIn(comp, expected_compositions)

    def test_fill_db_from_default_configs(self):
        """ fill the database using the built in default configs, should be no errors """
        # test both default configs, back to back
        # this also tests the ability to build up a database from multiple 
        # config files if necessary
        scdb = SumCompLipidDB()
        scdb.fill_db_from_config(DEFAULT_SCDB_CONFIG["POS"], 12, 24, False)
        scdb.fill_db_from_config(DEFAULT_SCDB_CONFIG["NEG"], 12, 24, False)

    def test_get_sum_comp_lipids(self):
        """ fill the database with built in default configs then test querying """
        scdb = SumCompLipidDB()
        scdb.fill_db_from_config(DEFAULT_SCDB_CONFIG["POS"], 12, 24, False)
        scdb.fill_db_from_config(DEFAULT_SCDB_CONFIG["NEG"], 12, 24, False)
        lipids = scdb.get_sum_comp_lipid_ids(766.5, 40)
        # there should be 1 ID for this m/z at 40 ppm 
        self.assertEqual(len(lipids), 1)


class TestRemoveLipidAnnotations(unittest.TestCase):
    """ tests for the remove_lipid_annotations function """

    def test_results_db_file_does_not_exist(self):
        """ should raise an error if the results database file does not exist """
        with self.assertRaises(FileNotFoundError, 
                               msg="expect a FileNotFoundError from nonexistent database file"):
            remove_lipid_annotations("this results database file does not exist")

    def test_empty_lipids_table(self):
        """ remove lipid annotations from database with empty Lipids table """
        with tempfile.TemporaryDirectory() as tmp_dir:
            dbf = os.path.join(tmp_dir, "results.db")
            create_results_db(dbf)  # STRICT!
            con = sqlite3.connect(dbf)
            cur = con.cursor()
            # test the function
            remove_lipid_annotations(dbf)
            # make sure there are no entries left in the Lipids table
            self.assertEqual(len([_ for _ in cur.execute("SELECT * FROM Lipids")]), 0)

    def test_non_empty_lipids_table(self):
        """ remove lipid annotations from database with non empty Lipids table """
        with tempfile.TemporaryDirectory() as tmp_dir:
            dbf = os.path.join(tmp_dir, "results.db")
            create_results_db(dbf)  # STRICT!
            con = sqlite3.connect(dbf)
            cur = con.cursor()
            # fill the db with the features
            for qdata in [
                (None, 1, "LMID prefix", "lipid", "adduct", 20., None, None, None),
                (None, 2, "LMID prefix", "lipid", "adduct", 20., None, None, None),
                (None, 3, "LMID prefix", "lipid", "adduct", 20., None, None, None),
                (None, 4, "LMID prefix", "lipid", "adduct", 20., None, None, None),
                (None, 5, "LMID prefix", "lipid", "adduct", 20., None, None, None),
            ]:
                cur.execute("INSERT INTO Lipids VALUES (?,?,?,?,?,?,?,?,?)", qdata) 
            con.commit()
            # test the function
            # entries are in the Lipids table before removing
            self.assertEqual(len([_ for _ in cur.execute("SELECT * FROM Lipids")]), 5)
            remove_lipid_annotations(dbf)
            # make sure there are no entries left in the Lipids table
            self.assertEqual(len([_ for _ in cur.execute("SELECT * FROM Lipids")]), 0)


class TestAnnotateLipidsSumComposition(unittest.TestCase):
    """ tests for the annotate_lipids_sum_composition function """

    def test_mock_features(self):
        """ annotate lipids at sum compoisition level with mocked DIA feature """
        with tempfile.TemporaryDirectory() as tmp_dir:
            dbf = os.path.join(tmp_dir, "results.db")
            create_results_db(dbf)  # STRICT!
            con = sqlite3.connect(dbf)
            cur = con.cursor()         
            dia_qdata = (
                None, None, -1, 
                766.5, 
                15.0, 0.1, 1e5, 20., 
                35., 2.5, 1e5, 10., 
                None, 0
            )
            cur.execute(
                f"INSERT INTO DiaPrecursors VALUES ({("?," * 14).rstrip(",")});",
                dia_qdata
            )
            con.commit()
            # test the function
            n_feats_annotated, n_ann = annotate_lipids_sum_composition(dbf, 
                                                                       _ANNOTATION_PARAMS)
            # there should be 1 feature annotated and more than 1 annotation
            self.assertEqual(n_feats_annotated, 1)
            self.assertGreater(n_ann, 1)
            # there should be more than 1 annotation in the Lipid table of the database
            self.assertGreater(len(cur.execute("SELECT * FROM Lipids").fetchall()), 1)

    def test_results_db_file_does_not_exist(self):
        """ should raise an error if the results database file does not exist """
        with self.assertRaises(FileNotFoundError, 
                               msg="expect a FileNotFoundError from nonexistent database file"):
            _ = annotate_lipids_sum_composition("results db file doesnt exist",
                                                _ANNOTATION_PARAMS)
    

class TestFilterAnnotationsByRtRange(unittest.TestCase):
    """ tests for the filter_annotations_by_rt_range function """

    def test_default_rt_range_config_and_mock_data(self):
        """ filter annotations with default RT range config and mock data """
        with tempfile.TemporaryDirectory() as tmp_dir:
            dbf = os.path.join(tmp_dir, "results.db")
            create_results_db(dbf)  # STRICT!
            con = sqlite3.connect(dbf)
            cur = con.cursor()
            dia_qdata = [
                (
                    None, None, -1, 
                    766.5, 
                    15.0, 0.1, 1e5, 20., 
                    35., 2.5, 1e5, 10., 
                    None, 0
                ),
                (
                    None, None, -1, 
                    766.5, 
                    20.0, 0.1, 1e5, 20., 
                    35., 2.5, 1e5, 10., 
                    None, 0
                )
            ]
            cur.executemany(
                f"INSERT INTO DiaPrecursors VALUES ({("?," * 14).rstrip(",")});",
                dia_qdata
            )
            con.commit()
            # annotate the features (there should be a couple PCs in there)
            n_feats_annotated, n_ann = annotate_lipids_sum_composition(dbf, 
                                                                       _ANNOTATION_PARAMS)
            # check the features before filtering
            # there should be 1 feature annotated and more than 1 annotation
            self.assertEqual(n_feats_annotated, 2)
            self.assertGreater(n_ann, 2)
            # there should be more than 2 annotation in the Lipid table of the database
            self.assertGreater(len(cur.execute("SELECT * FROM Lipids").fetchall()), 2)
            # test the function
            n_kept, n_filtered = filter_annotations_by_rt_range(dbf, _ANNOTATION_PARAMS)
            # check the features after filtering 
            # there should have been at least one annotation filtered out
            self.assertGreater(n_filtered, 0)
            # there should be fewer annotations after filtering than there were 
            # after initial annotation
            self.assertLess(len(cur.execute("SELECT * FROM Lipids").fetchall()), n_ann)
    
    def test_results_db_file_does_not_exist(self):
        """ should raise an error if the results database file does not exist """
        with self.assertRaises(FileNotFoundError, 
                               msg="expect a FileNotFoundError from nonexistent database file"):
            _ = filter_annotations_by_rt_range("results db file doesnt exist", 
                                               _ANNOTATION_PARAMS)


class TestFilterAnnotationsByCcsSubclassTrend(unittest.TestCase):
    """ tests for the filter_annotations_by_ccs_subclass_trend function """
    
    def test_results_db_file_does_not_exist(self):
        """ should raise an error if the results database file does not exist """
        with self.assertRaises(FileNotFoundError, 
                               msg="expect a FileNotFoundError from nonexistent database file"):
            filter_annotations_by_ccs_subclass_trend("results db file doesnt exist", _ANNOTATION_PARAMS)
        

class TestUpdateLipidIDsWithFragRules(unittest.TestCase):
    """ tests for the update_lipid_ids_with_frag_rules function """

    def test_results_db_file_does_not_exist(self):
        """ should raise an error if the results database file does not exist """
        with self.assertRaises(FileNotFoundError, 
                               msg="expect a FileNotFoundError from nonexistent database file"):
            update_lipid_ids_with_frag_rules("results db file doesnt exist", _ANNOTATION_PARAMS)
        

class TestAnnotateLipids(unittest.TestCase):
    """ tests for the annotate_lipids function """

    def test_results_db_file_does_not_exist(self):
        """ should raise an error if the results database file does not exist """
        with self.assertRaises(FileNotFoundError, 
                               msg="expect a FileNotFoundError from nonexistent database file"):
            annotate_lipids("results db file doesnt exist", _ANNOTATION_PARAMS)


# group all of the tests from this module into a TestSuite
_loader = unittest.TestLoader()
AllTestsAnnotation = unittest.TestSuite()
AllTestsAnnotation.addTests([
    _loader.loadTestsFromTestCase(TestDefaultConfigs),
    _loader.loadTestsFromTestCase(TestSumCompLipidDB),
    _loader.loadTestsFromTestCase(TestRemoveLipidAnnotations),
    _loader.loadTestsFromTestCase(TestAnnotateLipidsSumComposition),
    _loader.loadTestsFromTestCase(TestFilterAnnotationsByRtRange),
    _loader.loadTestsFromTestCase(TestFilterAnnotationsByCcsSubclassTrend),
    _loader.loadTestsFromTestCase(TestAnnotateLipids)
])


if __name__ == '__main__':
    # run all defined TestCases for only this module if invoked directly
    unittest.TextTestRunner(verbosity=2).run(AllTestsAnnotation)
