# GitHub Environments para GCP

Configurar dos environments en GitHub: `dev` y `prod`.

## Environment `dev`

Variables:

- `GCP_PROJECT_ID`: `maestriaia`
- `GCP_REGION`: `us-central1`
- `ARTIFACT_REPOSITORY`: `taller-artifact-registry`
- `CLOUD_RUN_SERVICE`: `mlops-onnx-api-dev`
- `MODEL_URI`: `gs://bucket_taller_mlops/model.onnx`
- `TEST_DATA_URI`: `gs://bucket_taller_mlops/test_data.json`
- `PREDICTIONS_LOG_URI`: `gs://bucket_taller_mlops/predicciones_dev.txt`

Secret:

- `GCP_SA_KEY`: JSON de la service account.

## Environment `prod`

Variables:

- `GCP_PROJECT_ID`: `maestriaia`
- `GCP_REGION`: `us-central1`
- `ARTIFACT_REPOSITORY`: `taller-artifact-registry`
- `CLOUD_RUN_SERVICE`: `mlops-onnx-api-prod`
- `MODEL_URI`: `gs://bucket_taller_mlops/model.onnx`
- `TEST_DATA_URI`: `gs://bucket_taller_mlops/test_data.json`
- `PREDICTIONS_LOG_URI`: `gs://bucket_taller_mlops/predicciones_prod.txt`

Secret:

- `GCP_SA_KEY`: JSON de la service account.

## Permisos sugeridos para la service account

- `roles/serviceusage.serviceUsageAdmin` para habilitar APIs desde el script.
- `roles/storage.objectAdmin` sobre el bucket.
- `roles/artifactregistry.writer` sobre Artifact Registry.
- `roles/run.admin` sobre Cloud Run.
- `roles/iam.serviceAccountUser` si Cloud Run usa una runtime service account especifica.

Para que el script `scripts/setup_gcp.sh` pueda crear recursos desde cero, tambien necesita permisos de administracion sobre los recursos iniciales:

- `roles/storage.admin` para crear el bucket si no existe.
- `roles/artifactregistry.admin` para crear el repositorio Docker si no existe.

Si prefieres crear o habilitar recursos manualmente en la consola, puedes ejecutar:

```bash
ENABLE_SERVICES=false ./scripts/setup_gcp.sh
```
