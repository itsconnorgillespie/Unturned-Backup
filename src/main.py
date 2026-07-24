import os
import pathlib
import sys
import zipfile
from zipfile import ZipFile
from datetime import datetime, timezone
from src.logger import get_logger
from src.settings import Settings
from src.storage import get_s3_client, upload_s3_file

logger = get_logger()


def get_filename(server_name: str) -> str:
    """ Build the filename using current UTC time and server name. """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{server_name}-{timestamp}.zip"


def create_zip(source_directory: str, destination_directory: str) -> None:
    """ Creates a lossless zip archive of the provided source directory in the provided destination directory. """
    source = pathlib.Path(source_directory)
    if not source.is_dir():
        logger.error(f"Source directory {source} does not exist.")
        sys.exit(1)

    files = 0
    with ZipFile(destination_directory, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in source.rglob("*"):
            if path.is_file():
                filename = path.relative_to(source)
                archive.write(str(path), filename)
                files += 1

    if files == 0:
        logger.error(f"Source directory {source} does not contain any files.")
        sys.exit(1)

    megabytes = os.path.getsize(destination_directory) / (1024 * 1024)
    logger.info(f"Zipped a total of {files} files with a size of {megabytes:.1f} MiB.")


def main() -> None:
    settings = Settings.from_env()
    os.makedirs(settings.TEMPORARY_DIRECTORY, exist_ok=True)

    filename = get_filename(settings.SERVER_NAME)
    path = os.path.join(settings.TEMPORARY_DIRECTORY, filename)

    logger.info(f"Zipping {settings.DATA_DIRECTORY} to {settings.TEMPORARY_DIRECTORY}")
    create_zip(settings.DATA_DIRECTORY, path)

    client = get_s3_client(settings)
    key = f"{settings.S3_PREFIX}{filename}"
    if not upload_s3_file(client, settings, path, key):
        os.remove(path)
        sys.exit(1)

    os.remove(path)
    logger.info("Finished.")


if __name__ == "__main__":
    main()
