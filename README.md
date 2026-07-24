## Unturned S3 Backup Docker Image
This repository aims to reduce the hassle for backing up an Unturned Dedicated Server by leveraging S3 and Docker. This repository is designed to natively support the [Unturned-Docker](https://github.com/itsconnorgillespie/Unturned-Docker) image, however, it will likely work with other images by design. The Docker image is currently hosted at `ghcr.io/itsconnorgillespie/unturned-backup`.

### Quickstart Command 
The following command runs a one-off backup of a local `data/` directory to an S3 compatible bucket. Adjust the S3 credentials and endpoint to match your cloud provider.

```sh
docker run --rm \
  -v ./data:/data \
  -e SERVER_NAME=server \
  -e S3_ENDPOINT=https://s3.example.com \
  -e S3_BUCKET=backups \
  -e S3_ACCESS_KEY=key \
  -e S3_SECRET_KEY=secret \
  --name unturned-backup \
  ghcr.io/itsconnorgillespie/unturned-backup:latest
```

### Environment Variables
The following environment variables can be utilized to tailor the Docker image to your specific needs.

1. `DATA_DIRECTORY`
- Expected: string
- Default: "/data"
- Description: Define the directory containing the data to archive.

2. `TEMPORARY_DIRECTORY`
- Expected: string
- Default: "/tmp/backup"
- Description: Define the directory used for staging archives before uploading to S3.

3. `EXCLUDE_PATTERNS`
- Expected: string
- Default: "Workshop,Spy"
- Description: Provide filenames or directories to exclude from the backup separated by commas.

4. `SERVER_NAME`
- Expected: string
- Default: "server"
- Description: Define the name of the server.

5. `S3_ENDPOINT`
- Expected: string
- Default: None
- Description: Define the destination S3 compatible endpoint.

6. `S3_BUCKET`
- Expected: string
- Default: None
- Description: Define the destination S3 bucket name.

7. `S3_REGION`
- Expected: string
- Default: "auto"
- Description: Define the destination S3 region.

8. `S3_ACCESS_KEY`
- Expected: string
- Default: None
- Description: Define the S3 access key used for authentication.

9. `S3_SECRET_KEY`
- Expected: string
- Default: None
- Description: Define the S3 secret key used for authentication.
