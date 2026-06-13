import argparse
from pathlib import Path
from urllib.request import urlretrieve


def download(uri: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if uri.startswith("gs://"):
        download_from_gcs(uri, destination)
        return

    if uri.startswith(("http://", "https://")):
        urlretrieve(uri, destination)
        return

    raise ValueError(f"Unsupported artifact URI: {uri}")


def download_from_gcs(uri: str, destination: Path) -> None:
    try:
        from google.cloud import storage
    except ImportError as exc:
        raise RuntimeError("Install the cloud extra to download from GCS.") from exc

    bucket_key = uri.removeprefix("gs://")
    bucket, key = bucket_key.split("/", 1)
    client = storage.Client()
    blob = client.bucket(bucket).blob(key)
    blob.download_to_filename(str(destination))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", action="store_true", help="Download MODEL_URI.")
    parser.add_argument("--test-data", action="store_true", help="Download TEST_DATA_URI.")
    parser.add_argument("--model-uri", default=None)
    parser.add_argument("--model-path", default="artifacts/model.onnx")
    parser.add_argument("--test-data-uri", default=None)
    parser.add_argument("--test-data-path", default="artifacts/test_data.json")
    args = parser.parse_args()

    if args.model:
        uri = args.model_uri or _required_env("MODEL_URI")
        download(uri, Path(args.model_path))

    if args.test_data:
        uri = args.test_data_uri or _required_env("TEST_DATA_URI")
        download(uri, Path(args.test_data_path))


def _required_env(name: str) -> str:
    import os

    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required.")
    return value


if __name__ == "__main__":
    main()
