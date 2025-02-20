import argparse
import logging
import kestra

from src.convert_csv_to_pq import convert_csv_to_parquet


def convert_file():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src_file_name", help="the name of the csv file without the .csv extension"
    )

    parser.add_argument(
        "--is_kestra",
        help="use this flag if this script is running in Kestra",
        required=False,
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()

    if args.is_kestra:
        logger = kestra.Kestra.logger()
    else:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

    convert_csv_to_parquet(src_file_name=args.src_file_name, logger=logger, is_kestra=args.is_kestra)


if __name__ == "__main__":
    convert_file()
