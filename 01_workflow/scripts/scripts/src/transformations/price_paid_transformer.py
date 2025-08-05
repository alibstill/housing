import pandas as pd
from logging import Logger
import hashlib


def add_location_hash(dframe: pd.DataFrame, logger: Logger):
    """
    Add location_hash column to dataframe

    Parameters
    ----------
    dframe: pandas DataFrame
        the dataframe of raw price paid data
    logger: Logger
    """
    hash_columns = [
        "postcode",
        "paon",
        "saon",
        "street",
        "locality",
        "town_city",
        "district",
        "county",
    ]
    # reorganize hash columns so that they appear like indexes. Note that if any of the
    # column values are NaN then they won't appear as a potential index. This approach
    # allows us to make a hash from only the available address data
    df_stacked = dframe[hash_columns].stack()

    # Create a string from all the info in the location columns
    series_str_concat = df_stacked.groupby(level=0).agg(";".join)
    # Create a hash of the string
    location_hash = series_str_concat.apply(
        lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()
    )
    df_copy = dframe.copy()
    df_copy["location_hash"] = location_hash

    logger.info("Successfully added 'location_hash' to price paid data.")
    return df_copy


def _check_log_drop(
    message: str, filter, dframe: pd.DataFrame, logger: Logger
) -> pd.DataFrame:
    issue_rows = dframe[filter]
    if len(issue_rows) > 0:
        logger.info(
            f"{message}. Number: %d. Transaction_uids = %s",
            len(issue_rows),
            list(issue_rows["transaction_uid"].values),
        )
        dframe = dframe.drop(issue_rows.index)
    return dframe


def clean(dframe: pd.DataFrame, logger: Logger):
    """
    Basic cleaning of data: drops any rows that have missing required fields

    Parameters
    ----------
    dframe: pandas DataFrame
        the dataframe of raw price paid data
    logger: Logger
    """
    df_rows_no_transaction_ids = dframe[dframe["transaction_uid"].isna()]
    if len(df_rows_no_transaction_ids) > 0:
        logger.info(
            "Rows with missing transaction_uid. Number: %d.",
            len(df_rows_no_transaction_ids),
        )
        dframe = dframe.drop(df_rows_no_transaction_ids.index)

    rows_missing_price_filter = dframe["price"].isna()
    dframe = _check_log_drop(
        "Rows with no 'price' data", rows_missing_price_filter, dframe, logger
    )

    rows_invalid_price_filter = dframe["price"] <= 0
    dframe = _check_log_drop(
        "Rows with 'price' set to value <= 0", rows_invalid_price_filter, dframe, logger
    )

    rows_invalid_date_of_transfer_filter = dframe["date_of_transfer"].isna()
    dframe = _check_log_drop(
        "Rows with 'date_of_transfer' not set",
        rows_invalid_date_of_transfer_filter,
        dframe,
        logger,
    )
    logger.info("Successfully cleaned data.")
    return dframe


def handle_types(dframe: pd.DataFrame, logger: Logger):
    """
    Ensure all data has the expected types

    Parameters
    ----------
    dframe: pandas DataFrame
        the dataframe of raw price paid data
    logger: Logger
    """
    dframe["date_of_transfer"] = pd.to_datetime(
        dframe["date_of_transfer"], errors="coerce"
    ).dt.date
    logger.info("Successfully handled types")
    return dframe


class PricePaidTransformer:
    def __init__(self) -> None:
        self.transform_steps = [self.handle_types, self.clean, self.add_location_hash]

    def apply(self, dframe: pd.DataFrame, logger: Logger):
        for step in self.transform_steps:
            dframe = step(dframe, logger)
        return dframe

    def add_location_hash(self, dframe: pd.DataFrame, logger: Logger):
        return add_location_hash(dframe, logger)

    def clean(self, dframe: pd.DataFrame, logger: Logger):
        return clean(dframe, logger)

    def handle_types(self, dframe: pd.DataFrame, logger: Logger):
        return handle_types(dframe, logger)
