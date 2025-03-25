import pandas as pd
from .metadata import metadata_mapper
from .transformations import transformations_mapper
from logging import Logger
from pathlib import Path


def get_file_name(src_file_name: str, is_kestra: bool) -> str:
    file_name = src_file_name.strip(".csv")
    if not is_kestra:
        dir_path = Path(__file__).parent / "temp"
        file_name = f"{dir_path}/{src_file_name}"
    return file_name


def process_csv(
    src_file_name: str, logger: Logger, is_kestra: bool, data_title: str = "price_paid"
) -> None:
    """
    Adds column names, a location hash and converts csv files to parquet

    Parameters
    ----------
    src_file_name: str
        the name of the csv file, without the ".csv" extension
    logger: Logger
    is_kestra: bool
        True if the script is running as part of a Kestra workflow
    data_title: str
        the name of the data
    """

    file_name = get_file_name(src_file_name=src_file_name, is_kestra=is_kestra)
    csv_file_path = f"{file_name}.csv"

    metadata = metadata_mapper.get(data_title)
    column_names = metadata.get_column_names()
    df = pd.read_csv(csv_file_path, names=column_names)
    logger.info(
        "Successfully read csv file: %s. Number of rows: %s", csv_file_path, len(df)
    )
    logger.info(df.info())

    price_paid_transformer = transformations_mapper.get(data_title)()

    df_transformed = price_paid_transformer.apply(df, logger)

    df_transformed.to_parquet(f"{file_name}.parquet", engine="pyarrow")
