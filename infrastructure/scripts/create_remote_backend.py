import uuid
from google.cloud import storage
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_remote_backend(location: str = "EUROPE-WEST2", bucket_name: str = None):
    """
    Create a new remote backend in a specific location
    """

    if not bucket_name:
        random_uuid = uuid.uuid4()

        bucket_name = f"{random_uuid}-tf-remote-backend"

    logger.info(bucket_name)

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    bucket.versioning_enabled = True
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.iam_configuration.public_access_prevention = "enforced"
    new_bucket = storage_client.create_bucket(bucket, location=location)

    logger.info(
        "Created bucket remote storage bucket in %s with storage class %s",
        new_bucket.location,
        new_bucket.storage_class,
    )

    return new_bucket


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Create Remote Backend",
        description="Create a GCS bucket to store terraform state",
    )
    parser.add_argument(
        "--location",
        help="The location of the backend bucket (the region of your project)",
        required=False,
        default="EUROPE-WEST2",
    )

    parser.add_argument(
        "--bucket_name",
        help="The name of the bucket. Must be unique across GCP e.g. 960e97d6ed3a95bd-terraform-remote-backend",
        required=False,
    )

    args = parser.parse_args()

    bucket = create_remote_backend(location=args.location, bucket_name=args.bucket_name)

    logger.info("bucket name: %s", bucket.name)
