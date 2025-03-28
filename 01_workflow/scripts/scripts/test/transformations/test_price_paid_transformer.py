import pytest
import pandas as pd
import hashlib
import logging

from src.transformations import PricePaidTransformer


@pytest.fixture
def price_paid_dataframe():
    data = {
        "transaction_uid": ["{2ACACE8D-47C7-295E-E063-4804A8C0B0EB]"],
        "price": [114000],
        "date_of_transfer": ["2021-02-26 00:00:00"],
        "postcode": ["S63 7FR"],
        "property_type": ["S"],
        "is_new_build": ["N"],
        "tenure_duration": ["L"],
        "paon": ["28"],
        "saon": ["Flat 1"],
        "street": ["REED WALK"],
        "locality": ["WATH UPON DEARNE"],
        "town_city": ["ROTHERHAM"],
        "district": ["ROTHERHAM"],
        "county": ["SOUTH YORKSHIRE"],
        "transaction_type": ["A"],
        "record_status": ["A"],
    }
    df = pd.DataFrame(data)
    df["data_of_transfer"] = pd.to_datetime(df["date_of_transfer"])
    return df


@pytest.fixture
def test_logger():
    logger = logging.getLogger("test_logger")
    return logger


class TestPricePaidTransformer:
    def test_should_add_location_hash_all_values_present(
        self, price_paid_dataframe: pd.DataFrame, test_logger: logging.Logger
    ) -> None:
        str_to_hash = "S63 7FR;28;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE"

        expected_hash = hashlib.md5(str_to_hash.encode("utf-8")).hexdigest()

        df_result = PricePaidTransformer().apply(price_paid_dataframe, test_logger)

        assert "location_hash" in df_result.columns

        assert df_result["location_hash"].iloc[0] == expected_hash

    @pytest.mark.parametrize(
        "col_to_null, str_to_hash",
        [
            (
                "postcode",
                "28;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "paon",
                "S63 7FR;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "saon",
                "S63 7FR;28;REED WALK;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "street",
                "S63 7FR;28;Flat 1;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "locality",
                "S63 7FR;28;Flat 1;REED WALK;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "town_city",
                "S63 7FR;28;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "district",
                "S63 7FR;28;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;SOUTH YORKSHIRE",
            ),
            (
                "county",
                "S63 7FR;28;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM",
            ),
        ],
    )
    def test_should_add_location_hash_values_missing(
        self,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
        col_to_null: str,
        str_to_hash: str,
    ) -> None:
        df_with_null = price_paid_dataframe.copy()
        df_with_null[col_to_null] = None

        expected_hash = hashlib.md5(str_to_hash.encode("utf-8")).hexdigest()

        df_result = PricePaidTransformer().apply(df_with_null, test_logger)

        assert "location_hash" in df_result.columns

        assert df_result["location_hash"].iloc[0] == expected_hash
