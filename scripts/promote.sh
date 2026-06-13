#!/usr/bin/env sh
set -eu

if [ -z "${GCP_PROJECT_ID:-}" ] || [ -z "${GCP_REGION:-}" ] || [ -z "${CLOUD_RUN_SERVICE:-}" ]; then
  echo "GCP_PROJECT_ID, GCP_REGION and CLOUD_RUN_SERVICE are required."
  exit 1
fi

if [ -z "${IMAGE_URI:-}" ]; then
  echo "IMAGE_URI is required."
  exit 1
fi

gcloud run deploy "${CLOUD_RUN_SERVICE}" \
  --image "${IMAGE_URI}" \
  --project "${GCP_PROJECT_ID}" \
  --region "${GCP_REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "APP_ENV=${APP_ENV},PREDICTIONS_LOG_URI=${PREDICTIONS_LOG_URI:-},PREDICTIONS_LOG_PATH=/app/artifacts/predicciones_${APP_ENV}.txt"
