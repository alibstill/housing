from pathlib import Path

import logging
import shutil
import pyarrow.parquet as pq


import pandas as pd
import pytest

from src.process_csv import process_csv, get_schema

current_dir = Path(__file__).resolve().parent


@pytest.fixture
def test_logger():
    logger = logging.getLogger("test_logger")
    return logger


class TestProcessCsv:
    @classmethod
    def setup_class(self):
        self.temp_folder = current_dir / "../src/temp"
        self.raw_file = current_dir / "test_data/test_raw_pp.csv"
        shutil.copyfile(self.raw_file, self.temp_folder / "clean.csv")

    @classmethod
    def teardown_class(self):
        """Remove files created as part of testing"""
        first_csv = self.temp_folder / "clean.csv"
        first_parquet = self.temp_folder / "clean.parquet"

        first_csv.unlink(missing_ok=True)
        first_parquet.unlink(missing_ok=True)

    def test_price_paid_should_generate_parquet_file_with_location_hash(
        self, test_logger
    ):
        df_original = pd.read_csv(self.temp_folder / "clean.csv")
        assert len(df_original.columns) == 16
        assert "location_hash" not in df_original.columns

        process_csv(
            src_file_name="clean",
            logger=test_logger,
            is_kestra=False,
            data_title="price_paid",
        )
        # TODO: test that you're getting the parquet with the hash

        df = pd.read_parquet(self.temp_folder / "clean.parquet")

        assert len(df.columns) == 17
        parquet_file = pq.read_schema(self.temp_folder / "clean.parquet")
        expected_schema = get_schema()
        assert (
            parquet_file == expected_schema
        ), f"Expected schema: {expected_schema}, but got: {parquet_file.schema}"
