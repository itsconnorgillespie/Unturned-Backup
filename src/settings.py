import os
import sys
from dataclasses import dataclass
from src.logger import get_logger

logger = get_logger()


@dataclass(frozen=True)
class Settings:
    DATA_DIRECTORY: str
    TEMPORARY_DIRECTORY: str
    SERVER_NAME: str
    S3_ENDPOINT: str
    S3_BUCKET: str
    S3_REGION: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_PREFIX: str

    @classmethod
    def from_env(cls) -> "Settings":
        try:
            endpoint = os.environ["S3_ENDPOINT_URL"]
            bucket = os.environ["S3_BUCKET"]
            key = os.environ["S3_ACCESS_KEY"]
            secret = os.environ["S3_SECRET_KEY"]
        except KeyError as error:
            logger.error(f"Environment variable {error} is required.")
            sys.exit(1)

        return cls(
            DATA_DIRECTORY=os.environ.get("DATA_DIRECTORY", "/data"),
            TEMPORARY_DIRECTORY=os.environ.get("TEMPORARY_DIRECTORY", "/tmp/backup"),
            SERVER_NAME=os.environ.get("SERVER_NAME", "unturned-server1"),
            S3_ENDPOINT=endpoint,
            S3_BUCKET=bucket,
            S3_REGION=os.environ.get("S3_REGION", "auto"),
            S3_ACCESS_KEY=key,
            S3_SECRET_KEY=secret,
            S3_PREFIX=os.environ.get("S3_PREFIX", ""),
        )
