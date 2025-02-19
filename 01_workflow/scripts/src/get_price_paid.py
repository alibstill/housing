import argparse
import logging
import kestra

from download_save_file import get_file


def get_price_paid():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", help="this is usually of the form 'pp-YYYY'")
    parser.add_argument(
        "--base_url",
        help="the part of the url before the final file_name eg. 'http://url.com/",
        required=True,
    )
    parser.add_argument(
        "--is_kestra",
        help="the part of the url before the final file_name eg. 'http://url.com/",
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

    get_file(
        file_name=args.file_name,
        base_url=args.base_url,
        logger=logger,
        is_kestra=args.is_kestra,
    )


if __name__ == "__main__":
    get_price_paid()
