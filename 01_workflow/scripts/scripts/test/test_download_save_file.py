import io
from pathlib import Path
from typing import Iterator
import logging

import pandas as pd
import pytest
import responses

from src.download_save_file import DownloadSaveFileException, get_file, save_file

current_dir = Path(__file__).resolve().parent


@pytest.fixture
def mocked_responses() -> Iterator[responses.RequestsMock]:
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def test_file_content(scope="session") -> bytes:
    """Return a test CSV file as a byte stream."""
    with open(current_dir / "test_data/test_raw_pp.csv", mode="rb") as test_file:
        return test_file.read()


@pytest.fixture
def test_logger():
    logger = logging.getLogger("test_logger")
    return logger


class TestDownloadSaveFile:
    def setup_class(self):
        self.base_url = "http://myurl.co.uk/"
        self.temp_folder = current_dir / "../src/temp"

    def teardown_class(self):
        """Remove files created as part of testing"""
        first_file = self.temp_folder / "my_file.csv"
        second_file = self.temp_folder / "my_saved_file.csv"
        third_file = self.temp_folder / "my_read_file.csv"
        fourth_file = self.temp_folder / "incomplete_file.csv"

        first_file.unlink(missing_ok=True)
        second_file.unlink(missing_ok=True)
        third_file.unlink(missing_ok=True)
        fourth_file.unlink(missing_ok=True)

    def test_should_call_api_with_correct_filename(
        self, mocked_responses, test_file_content, test_logger
    ):
        test_url = f"{self.base_url}my_file.csv"
        mocked_responses.get(
            test_url, body=test_file_content, auto_calculate_content_length=True
        )
        get_file(
            file_name="my_file.csv",
            base_url=self.base_url,
            logger=test_logger,
            is_kestra=False,
        )
        mocked_responses.assert_call_count(test_url, 1)

    def test_should_save_in_temp_folder(
        self, mocked_responses, test_file_content, test_logger
    ):
        # arrange
        test_url = f"{self.base_url}my_saved_file.csv"
        expected_path = self.temp_folder / "my_saved_file.csv"

        mocked_responses.get(
            test_url, body=test_file_content, auto_calculate_content_length=True
        )
        # act
        get_file(
            file_name="my_saved_file.csv",
            base_url=self.base_url,
            logger=test_logger,
            is_kestra=False,
        )

        # assert
        mocked_responses.assert_call_count(test_url, 1)

        with open(expected_path, mode="rb") as file_contents:
            assert file_contents.read() == test_file_content

    def test_can_read_saved_file(
        self, mocked_responses, test_file_content, test_logger
    ):
        # arrange
        test_url = f"{self.base_url}my_read_file.csv"
        expected_path = self.temp_folder / "my_read_file.csv"

        mocked_responses.get(
            test_url, body=test_file_content, auto_calculate_content_length=True
        )
        # act
        get_file(
            file_name="my_read_file.csv",
            base_url=self.base_url,
            logger=test_logger,
            is_kestra=False,
        )

        # assert
        mocked_responses.assert_call_count(test_url, 1)

        df = pd.read_csv(expected_path, header=None)
        assert len(df.columns) == 16
        assert len(df) == 3
        assert df.iloc[0, 0] == "{9ABCAA4F-D5E2-42D3-8B62-5ADEA1879CC8}"

    def test_should_raise_error_not_200(self, mocked_responses, test_logger):
        # arrange
        test_url = f"{self.base_url}no_file.csv"
        mocked_responses.get(test_url, body="not found", status=404)

        # act and assert
        with pytest.raises(DownloadSaveFileException) as exc_info:
            get_file(
                file_name="no_file.csv",
                base_url=self.base_url,
                logger=test_logger,
                is_kestra=False,
            )

        assert "HTTP Error encountered" in exc_info.value.args[0]
        assert "404 Client Error" in exc_info.value.args[0]

    def test_should_raise_error_if_no_content_size(self, mocked_responses, test_logger):
        test_url = f"{self.base_url}empty.csv"
        mocked_responses.get(test_url, body=None)

        # act and assert
        with pytest.raises(DownloadSaveFileException) as exc_info:
            get_file(
                file_name="empty.csv",
                base_url=self.base_url,
                logger=test_logger,
                is_kestra=False,
            )

        assert "Content-length of resource is 0" == exc_info.value.args[0]

    def test_should_raise_error_file_incomplete(self, test_file_content, test_logger):
        from requests.models import Response

        mock_response = Response()
        mock_response.status_code = 200
        # This is not strictly correct because in reality we would have a
        # stream not a file object
        # but is good enough for now
        mock_response.raw = io.BytesIO(test_file_content)

        with pytest.raises(DownloadSaveFileException) as exc_info:
            save_file(
                mock_response, "incomplete_file.csv", 864, test_logger, is_kestra=False
            )

        assert "This file had not been completed downloaded." in exc_info.value.args[0]
        assert (
            "The expected size is 864 but we have only saved 534"
            in exc_info.value.args[0]
        )
