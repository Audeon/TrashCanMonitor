import os
import unittest
from os import path
from app.functions.config_init import Config

class TestConfig(unittest.TestCase):

    config_dir = path.join("config_tests", "config_files")
    # config_dir = ""

    def rm_created_dir(self, path):
        if os.path.isdir(path):
            try:
                os.rmdir(path)
            except Exception as err:
                raise Exception(err)

    def test_initalize_with_full_config_file(self):
        perfect_config = path.join(self.config_dir, "test_full_config.json")
        config = Config(config_path=perfect_config)

        self.assertEqual(config.log_level, 20, "config.log_level, was unset.")
        self.assertIn("\logging",config.log_path, "config.log_path, was unset.")
        self.assertEqual(config.log_format, "%(asctime)s %(name)s : %(message)s", "config.log_format, was unset.")
        self.assertEqual(config.log_encoding, "ascii", "config.log_encoding, was unset.")

        self.assertEqual(config.sleep_time, 30, "config.sleep_time, was unset.")
        self.assertEqual(config.target_gateway_url, "http://192.168.12.1", "config.target_gateway_url, was unset.")
        self.assertEqual(config.transport, "sqlalchemy", "config.transport, was unset.")
        self.assertEqual(config.mongodb_uri, "mongodb://tc_usr:trashcan@tcmongodb:27017/tcresults",
                         "config.mongodb_uri, was unset.")
        self.assertEqual(config.results_db, "tcresults", "config.results_db, was unset.")
        self.assertEqual(config.db_collection, "modem_results", "config.db_collection, was unset.")

        self.rm_created_dir(config.log_path)

    def test_initalize_with_kwargs(self):
        config = Config(
            no_config_file=True,
            log_level=20,
            log_path="./logging/",
            log_format="%(asctime)s %(name)s : %(message)s",
            log_encoding="ascii",
            log2console=False,
            sleep_time=30,
            target_gateway_url="http://192.168.12.1",
            transport="sqlalchemy",
            mongodb_uri="mongodb://tc_usr:trashcan@tcmongodb:27017/tcresults",
            results_db="tcresults",
            db_collection="modem_results"
        )

        self.assertEqual(config.log_level, 20, "config.log_level, was unset.")
        self.assertIn("\logging",config.log_path, "config.log_path, was unset.")
        self.assertEqual(config.log_format, "%(asctime)s %(name)s : %(message)s", "config.log_format, was unset.")
        self.assertEqual(config.log_encoding, "ascii", "config.log_encoding, was unset.")

        self.assertEqual(config.sleep_time, 30, "config.sleep_time, was unset.")
        self.assertEqual(config.target_gateway_url, "http://192.168.12.1", "config.target_gateway_url, was unset.")
        self.assertEqual(config.transport, "sqlalchemy", "config.transport, was unset.")
        self.assertEqual(config.mongodb_uri, "mongodb://tc_usr:trashcan@tcmongodb:27017/tcresults", "config.mongodb_uri, was unset.")
        self.assertEqual(config.results_db, "tcresults", "config.results_db, was unset.")
        self.assertEqual(config.db_collection, "modem_results", "config.db_collection, was unset.")

    def test_initalize_config_file_kwargs_overide(self):
        perfect_config = path.join(self.config_dir, "test_full_config.json")
        config = Config(
            config_path=perfect_config,
            log_level=10,
            log_path="./logs/",
            log_format="%(asctime)s %(name)s : %(message)s",
            log_encoding="utf-8",
            log2console=False,
            sleep_time=50,
            target_gateway_url="http://192.168.12.1",
            transport="mongodbs",
            mongodb_uri="mongodb://tc_usr:trashcan@tcmongodb:27017/tcresultstest",
            results_db="tcresults1",
            db_collection="results"
        )

        self.assertEqual(config.log_level, 10, "config.log_level, was unset.")
        self.assertIn("\logs", config.log_path, "config.log_path, was unset.")
        self.assertEqual(config.log_format, "%(asctime)s %(name)s : %(message)s", "config.log_format, was unset.")
        self.assertEqual(config.log_encoding, "utf-8", "config.log_encoding, was unset.")

        self.assertEqual(config.sleep_time, 50, "config.sleep_time, was unset.")
        self.assertEqual(config.target_gateway_url, "http://192.168.12.1", "config.target_gateway_url, was unset.")
        self.assertEqual(config.transport, "mongodbs", "config.transport, was unset.")
        self.assertEqual(config.mongodb_uri, "mongodb://tc_usr:trashcan@tcmongodb:27017/tcresultstest",
                         "config.mongodb_uri, was unset.")
        self.assertEqual(config.results_db, "tcresults1", "config.results_db, was unset.")
        self.assertEqual(config.db_collection, "results", "config.db_collection, was unset.")

    def test_initalize_defaults(self):

        config = Config(no_config_file=True)

        self.assertEqual(config.log_level, 10, "config.log_level, was unset.")
        self.assertIn("\logs", config.log_path, "config.log_path, was unset.")
        self.assertEqual(config.log_format, "%(asctime)s %(name)s %(levelname)s %(message)s", "config.log_format, was unset.")
        self.assertEqual(config.log_encoding, "utf-8", "config.log_encoding, was unset.")

        self.assertEqual(config.sleep_time, 60, "config.sleep_time, was unset.")
        self.assertEqual(config.target_gateway_url, "http://192.168.12.1", "config.target_gateway_url, was unset.")
        self.assertEqual(config.transport, "mongodb", "config.transport, was unset.")
        self.assertEqual(config.mongodb_uri, "mongodb://tc_usr:trashcan@tcmongodb:27017/tcresults",
                         "config.mongodb_uri, was unset.")
        self.assertEqual(config.results_db, "tcresults", "config.results_db, was unset.")
        self.assertEqual(config.db_collection, "results", "config.db_collection, was unset.")



    if __name__ == '__main__':
        unittest.main()