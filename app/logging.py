from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


def append_prediction(
    log_path: Path,
    payload: dict,
    prediction: list,
    app_env: str,
    remote_uri: str | None = None,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": app_env,
        "payload": payload,
        "prediction": prediction,
    }
    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=True) + "\n")

    if remote_uri:
        append_remote_prediction(record, remote_uri)


def append_remote_prediction(record: dict, remote_uri: str) -> None:
    if remote_uri.startswith("gs://"):
        append_to_gcs(record, remote_uri)
        return

    raise ValueError(f"Unsupported PREDICTIONS_LOG_URI: {remote_uri}")


def append_to_gcs(record: dict, remote_uri: str) -> None:
    try:
        from google.cloud import storage
        from google.api_core.exceptions import NotFound
    except ImportError as exc:
        raise RuntimeError("Install the cloud extra to upload logs to GCS.") from exc

    bucket_key = remote_uri.removeprefix("gs://")
    bucket, key = bucket_key.split("/", 1)

    client = storage.Client()
    blob = client.bucket(bucket).blob(key)
    try:
        existing_content = blob.download_as_text(encoding="utf-8")
    except NotFound:
        existing_content = ""

    new_line = json.dumps(record, ensure_ascii=True) + "\n"
    with NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp:
        temp.write(existing_content + new_line)
        temp_path = Path(temp.name)

    try:
        blob.upload_from_filename(str(temp_path))
    finally:
        temp_path.unlink(missing_ok=True)
