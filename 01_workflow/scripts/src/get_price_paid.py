import argparse

from download_save_file import get_file


def get_price_paid():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", help="this is usually of the form 'pp-YYYY'")
    parser.add_argument(
        "--base_url",
        help="the part of the url before the final file_name eg. 'http://url.com/",
        required=True,
    )

    args = parser.parse_args()
    get_file(file_name=args.file_name, base_url=args.base_url)


if __name__ == "__main__":
    get_price_paid()
