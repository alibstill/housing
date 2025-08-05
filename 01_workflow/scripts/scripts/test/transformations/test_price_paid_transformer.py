import pytest
import pandas as pd
import hashlib
import logging
from datetime import date

from src.transformations import PricePaidTransformer
from src.metadata import metadata_mapper


def get_data(
    transaction_uid: str = "{2ACACE8D-47C7-295E-E063-4804A8C0B0EB]",
    price: int = 114000,
    date_of_transfer: str = "2021-02-26 00:00:00",
) -> dict[str, str]:
    return {
        "transaction_uid": f"{transaction_uid}",
        "price": f"{price}",
        "date_of_transfer": f"{date_of_transfer}",
        "postcode": "S63 7FR",
        "property_type": "S",
        "is_new_build": "N",
        "tenure_duration": "L",
        "paon": "28",
        "saon": "Flat 1",
        "street": "REED WALK",
        "locality": "WATH UPON DEARNE",
        "town_city": "ROTHERHAM",
        "district": "ROTHERHAM",
        "county": "SOUTH YORKSHIRE",
        "transaction_type": "A",
        "record_status": "A",
    }


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
    return df


@pytest.fixture
def test_logger():
    logger = logging.getLogger("test_logger")
    return logger


class TestPricePaidTransformer:

    def test_full_transformer(self, test_logger: logging.Logger) -> None:
        valid_a = get_data(transaction_uid="1")
        invalid_id = get_data()
        invalid_id["transaction_uid"] = None
        invalid_price = get_data(transaction_uid="2", price=0)
        missing_date = get_data(transaction_uid="3", date_of_transfer=None)
        valid_b = get_data(transaction_uid="4")
        price_paid_meta = metadata_mapper.get("price_paid")
        pp_dtypes = price_paid_meta.get_column_dtypes()

        df = pd.DataFrame(
            [valid_a, invalid_id, missing_date, invalid_price, valid_b]
        ).astype(pp_dtypes)

        result = PricePaidTransformer().apply(df, test_logger)

        assert len(result) == 2
        assert set(result["transaction_uid"].values) == {"1", "4"}
        assert "location_hash" in result.columns

    def test_add_location_hash_all_values_present(
        self, price_paid_dataframe: pd.DataFrame, test_logger: logging.Logger
    ) -> None:
        str_to_hash = "S63 7FR;28;Flat 1;REED WALK;WATH UPON DEARNE;ROTHERHAM;ROTHERHAM;SOUTH YORKSHIRE"

        expected_hash = hashlib.md5(str_to_hash.encode("utf-8")).hexdigest()

        df_result = PricePaidTransformer().add_location_hash(
            price_paid_dataframe, test_logger
        )

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
    def test_add_location_hash_values_missing(
        self,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
        col_to_null: str,
        str_to_hash: str,
    ) -> None:
        df_with_null = price_paid_dataframe.copy()
        df_with_null[col_to_null] = None

        expected_hash = hashlib.md5(str_to_hash.encode("utf-8")).hexdigest()

        df_result = PricePaidTransformer().add_location_hash(df_with_null, test_logger)

        assert "location_hash" in df_result.columns

        assert df_result["location_hash"].iloc[0] == expected_hash

    def test_handle_types_date_of_transfer_standard_format(
        self,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
    ) -> None:
        assert len(price_paid_dataframe) == 1
        assert isinstance(price_paid_dataframe["date_of_transfer"].iloc[0], str)

        df_result = PricePaidTransformer().handle_types(
            price_paid_dataframe, test_logger
        )

        assert isinstance(df_result["date_of_transfer"].iloc[0], date)

    def test_handle_types_date_of_transfer_invalid_format(
        self, test_logger: logging.Logger
    ) -> None:
        data = pd.DataFrame({"date_of_transfer": ["2023-01-01 00:00:00", "not_a_date"]})

        df_result = PricePaidTransformer().handle_types(data, test_logger)

        assert df_result["date_of_transfer"].isna().sum() == 1
        first_valid_result = df_result.loc[
            df_result["date_of_transfer"].notna(), "date_of_transfer"
        ].iloc[0]
        assert first_valid_result == date(2023, 1, 1)

    def test_clean_logs_transaction_uids_rows_missing_price(
        self,
        caplog,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
    ) -> None:
        price_paid_dataframe["price"] = None

        with caplog.at_level(logging.INFO):
            PricePaidTransformer().clean(price_paid_dataframe, test_logger)

        assert (
            "Rows with no 'price' data. Number: 1. Transaction_uids = ['{2ACACE8D-47C7-295E-E063-4804A8C0B0EB]']"
            in caplog.text
        )

    def test_clean_logs_transaction_uids_rows_invalid_price(
        self,
        caplog,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
    ) -> None:
        price_paid_dataframe["price"] = -1

        with caplog.at_level(logging.INFO):
            PricePaidTransformer().clean(price_paid_dataframe, test_logger)

        assert (
            "Rows with 'price' set to value <= 0. Number: 1. Transaction_uids = ['{2ACACE8D-47C7-295E-E063-4804A8C0B0EB]']"
            in caplog.text
        )

    def test_clean_logs_transaction_uids_rows_missing_date_of_transfer(
        self,
        caplog,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
    ) -> None:
        price_paid_dataframe["date_of_transfer"] = None

        with caplog.at_level(logging.INFO):
            PricePaidTransformer().clean(price_paid_dataframe, test_logger)

        assert (
            "Rows with 'date_of_transfer' not set. Number: 1. Transaction_uids = ['{2ACACE8D-47C7-295E-E063-4804A8C0B0EB]']"
            in caplog.text
        )

    def test_clean_logs_missing_transaction_uids(
        self,
        caplog,
        price_paid_dataframe: pd.DataFrame,
        test_logger: logging.Logger,
    ) -> None:
        price_paid_dataframe["transaction_uid"] = None

        with caplog.at_level(logging.INFO):
            PricePaidTransformer().clean(price_paid_dataframe, test_logger)

        assert "Rows with missing transaction_uid. Number: 1." in caplog.text

    def test_clean_drops_rows_where_required_field_invalid(
        self, test_logger: logging.Logger
    ) -> None:
        data = pd.DataFrame(
            {
                "price": [100, 200, -1, None, 500],
                "date_of_transfer": [
                    date(2025, 3, 3),
                    date(2025, 3, 3),
                    date(2025, 3, 4),
                    date(2025, 3, 5),
                    pd.NaT,  # missing date
                ],
                "transaction_uid": [None, "1", "2", "3", "4"],
            }
        )
        df_result = PricePaidTransformer().clean(data, test_logger)

        assert len(df_result) == 1
