import os
import shutil
import unittest

from midas.api.fnc_run import run as midas_run
from midas.util.runtime_config import RuntimeConfig

from midas_dlp.module import DLPDataModule


class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.filedir = os.path.abspath(os.path.join(__file__, ".."))
        self.rtc = RuntimeConfig()
        self.rtc.load(
            {
                "paths": {
                    "output_path": self.filedir,
                    "scenario_path": self.filedir,
                    "data_path": self.filedir,
                }
            }
        )
        # scenario_file = os.path.join(self.filedir, "dlp_test.yml")
        self.results_db = os.path.join(self.filedir, "dlp_test_results.hdf5")
        mod = DLPDataModule()
        mod.download(
            self.filedir, os.path.join(self.filedir, "tmp"), False, False
        )

        # ["run", "-c", scenario_file, ])

    def test_run_scenario(self):
        midas_run(
            "dlp_test_example",
            {},
            None,
            skip_configure=True,
            skip_download=True,
        )
        # TODO test analyze
        print(self.rtc.paths)

    def tearDown(self):
        files_to_delete = [
            os.path.join(self.filedir, "bdew_default_load_profiles.csv"),
            os.path.join(self.filedir, "dlp_test_example_auto_script.py"),
            os.path.join(self.filedir, "dlp_test_example_cfg.yml"),
            os.path.join(self.filedir, "dlp_test_results.hdf5"),
        ]
        for f in files_to_delete:
            os.remove(f)
        shutil.rmtree(os.path.join(self.filedir, "tmp"))

if __name__ == "__main__":
    unittest.main()
