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
    # allows us to handle any unwanted NaN columns
    df_stacked = dframe[hash_columns].stack()

    # Create a string from all the info in the location columns
    series_str_concat = df_stacked.groupby(level=0).agg(";".join)
    # Create a hash of the string
    location_hash = series_str_concat.apply(
        lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()
    )
    df_copy = dframe.copy()
    df_copy["location_hash"] = location_hash

    logger.info("Added 'location_hash' to price paid data.")
    return df_copy


class PricePaidTransformer:
    def apply(self, dframe: pd.DataFrame, logger: Logger):
        return add_location_hash(dframe, logger)
