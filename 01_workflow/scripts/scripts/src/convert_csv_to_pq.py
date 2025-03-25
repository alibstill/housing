from logging import Logger
from pathlib import Path

import pyarrow.parquet as pq
from pyarrow import csv

from .metadata import metadata_mapper


def get_file_name(src_file_name: str, is_kestra: bool) -> str:
    file_name = src_file_name.strip(".csv")
    if not is_kestra:
        dir_path = Path(__file__).parent / "temp"
        file_name = f"{dir_path}/{src_file_name}"
    return file_name


def convert_csv_to_parquet(
    src_file_name: str, logger: Logger, is_kestra: bool, data_title: str = "price_paid"
) -> None:
    """
    Converts csv files to parquet

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
    read_options = None

    # TODO: add error handling
    metadata = metadata_mapper.get(data_title)
    column_names = metadata.get_column_names()

    read_options = csv.ReadOptions(column_names=column_names)

    file_name = get_file_name(src_file_name=src_file_name, is_kestra=is_kestra)
    csv_file_path = f"{file_name}.csv"
    table = csv.read_csv(csv_file_path, read_options)
    logger.info(
        "Successfully read csv file: %s. Schema: %s", csv_file_path, table.schema
    )
    pq.write_table(table, f"{file_name}.parquet")
    metadata = pq.read_metadata(f"{file_name}.parquet")
    logger.info("Successfully stored parquet file: %s", metadata)
