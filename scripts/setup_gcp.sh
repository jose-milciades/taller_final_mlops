#!/usr/bin/env sh
set -eu

GCP_PROJECT_ID="${GCP_PROJECT_ID:-maestriaia}"
GCP_REGION="${GCP_REGION:-us-central1}"
GCS_BUCKET="${GCS_BUCKET:-bucket_taller_mlops}"
ARTIFACT_REPOSITORY="${ARTIFACT_REPOSITORY:-taller-artifact-registry}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
GCLOUD="${GCLOUD:-${SCRIPT_DIR}/gcloud.sh}"
ENABLE_SERVICES="${ENABLE_SERVICES:-true}"

"${GCLOUD}" config set project "${GCP_PROJECT_ID}"

if [ "${ENABLE_SERVICES}" = "true" ]; then
  "${GCLOUD}" services enable \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    storage.googleapis.com
else
  echo "Skipping API enablement because ENABLE_SERVICES=${ENABLE_SERVICES}."
fi

if ! "${GCLOUD}" storage buckets describe "gs://${GCS_BUCKET}" >/dev/null 2>&1; then
  "${GCLOUD}" storage buckets create "gs://${GCS_BUCKET}" \
    --project "${GCP_PROJECT_ID}" \
    --location "${GCP_REGION}" \
    --uniform-bucket-level-access
fi

if ! "${GCLOUD}" artifacts repositories describe "${ARTIFACT_REPOSITORY}" \
  --project "${GCP_PROJECT_ID}" \
  --location "${GCP_REGION}" >/dev/null 2>&1; then
  "${GCLOUD}" artifacts repositories create "${ARTIFACT_REPOSITORY}" \
    --project "${GCP_PROJECT_ID}" \
    --location "${GCP_REGION}" \
    --repository-format docker \
    --description "Docker images for ONNX FastAPI deployments"
fi

python scripts/generate_sample_artifacts.py

"${GCLOUD}" storage cp artifacts/model.onnx "gs://${GCS_BUCKET}/model.onnx"
"${GCLOUD}" storage cp artifacts/test_data.json "gs://${GCS_BUCKET}/test_data.json"

touch /tmp/predicciones_dev.txt /tmp/predicciones_prod.txt
"${GCLOUD}" storage cp /tmp/predicciones_dev.txt "gs://${GCS_BUCKET}/predicciones_dev.txt"
"${GCLOUD}" storage cp /tmp/predicciones_prod.txt "gs://${GCS_BUCKET}/predicciones_prod.txt"

echo "GCP setup completed."
