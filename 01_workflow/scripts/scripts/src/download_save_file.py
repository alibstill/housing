from pathlib import Path
from logging import Logger

import requests


def save_file(
    response: requests.models.Response,
    file_name: str,
    expected_file_size: int,
    logger: Logger,
    is_kestra: bool,
) -> None:
    """
    Saves files to temporary folder

    Parameters
    ----------
    response: requests.models.Response
        the response object from the API call
    file_name : string (required)
        name of the csv to download e.g. "pp-2016.csv"
    expected_file_size : int
        the file size according to header "Content-length"
    logger: Logger
    is_kestra: bool
        True if the script is running as part of a Kestra workflow
    """
    actual_file_size = 0
    if not is_kestra:
        file_dir = Path(__file__).parent / "temp"
        file_dir.mkdir(parents=True, exist_ok=True)
        file_name = file_dir / file_name

    with open(file_name, mode="wb") as file:
        logger.info("Writing file to local directory: %s", file_name)
        for chunk in response.iter_content(chunk_size=10000000):
            logger.info("Writing chunk with size (in bytes): %d", len(chunk))
            file.write(chunk)
            actual_file_size += len(chunk)

    if actual_file_size != expected_file_size:
        raise DownloadSaveFileException(
            "This file had not been completed downloaded. "
            + f"The expected size is {expected_file_size} but "
            + f"we have only saved {actual_file_size}"
        )

    file_size = Path(file_name).stat().st_size
    logger.info(
        "File download complete and saved to %s. Size is: %d", file_name, file_size
    )


def get_file(file_name: str, base_url: str, logger: Logger, is_kestra) -> None:
    """
    Downloads file and saves to temp folder

    Parameters
    ----------
    file_name : string (required)
        name of the csv to download e.g. "pp-2016.csv"
    base_url : string
        base url of endpoint with file
    logger: Logger
    is_kestra: bool
        True if the script is running as part of a Kestra workflow
    """
    url = f"{base_url}{file_name}"
    logger.info("Retrieving %s from %s", file_name, url)

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            expected_file_size = int(response.headers.get("Content-length", 0))
            logger.info("Expected size of file is %d", expected_file_size)
            if expected_file_size == 0:
                raise DownloadSaveFileException("Content-length of resource is 0")
            save_file(response, file_name, expected_file_size, logger, is_kestra)

    except requests.exceptions.HTTPError as http_error:
        logger.info(repr(http_error))
        raise DownloadSaveFileException(
            f"HTTP Error encountered: {repr(http_error)}"
        ) from http_error


class DownloadSaveFileException(Exception):
    pass
