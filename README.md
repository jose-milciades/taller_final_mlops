# ONNX FastAPI Deployment

Base para el proyecto de despliegue automatico de modelos ONNX con FastAPI, Docker y GitHub Actions.

## Estructura

- `app/`: API FastAPI para inferencia.
- `scripts/`: descarga de modelo y datos de prueba desde URL o Google Cloud Storage.
- `tests/`: pruebas unitarias del modelo y la API.
- `.github/workflows/ci-cd.yml`: pipeline para ramas `dev` y `prod`.

## Variables principales

- `APP_ENV`: `dev` o `prod`.
- `MODEL_PATH`: ruta local del modelo ONNX. Por defecto `artifacts/model.onnx`.
- `MODEL_URI`: origen del modelo para CI/CD. Puede ser `https://...` o `gs://bucket/key`.
- `TEST_DATA_URI`: origen de los datos de prueba para CI/CD.
- `PREDICTIONS_LOG_PATH`: archivo local de predicciones.
- `PREDICTIONS_LOG_URI`: destino remoto opcional para predicciones, por ejemplo `gs://bucket/predicciones_dev.txt`.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test,cloud]"
python scripts/generate_sample_artifacts.py
pytest
uvicorn app.main:app --reload
```

El modelo ONNX no debe versionarse en el repositorio. En local puede generarse para pruebas o descargarse con:

```bash
MODEL_URI="https://example.com/model.onnx" python scripts/download_artifacts.py --model
```

## Endpoint

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"inputs":[[1,2,3,4]]}'
```

Endpoints desplegados:

- Dev: `https://mlops-onnx-api-dev-to5xh2n5qq-uc.a.run.app`
- Prod: `https://mlops-onnx-api-prod-to5xh2n5qq-uc.a.run.app`

## Evidencia de entrega

Repositorio:

- `https://github.com/jose-milciades/taller_final_mlops`

Ramas:

- `dev`
- `prod`

Pipeline:

- Workflow: `.github/workflows/ci-cd.yml`
- Trigger: `push` a `dev` y `prod`
- Etapas: `test` y `build-promote`

Corridas exitosas de GitHub Actions:

- Dev por `push`: `https://github.com/jose-milciades/taller_final_mlops/actions/runs/27455239829`
- Prod por `push`: `https://github.com/jose-milciades/taller_final_mlops/actions/runs/27455330904`

Artefactos externos al repositorio:

- Modelo ONNX: `gs://bucket_taller_mlops/model.onnx`
- Datos de prueba: `gs://bucket_taller_mlops/test_data.json`
- Predicciones dev: `gs://bucket_taller_mlops/predicciones_dev.txt`
- Predicciones prod: `gs://bucket_taller_mlops/predicciones_prod.txt`

Contenedores:

- Registry: `us-central1-docker.pkg.dev/maestriaia/taller-artifact-registry`
- Servicio Cloud Run dev: `mlops-onnx-api-dev`
- Servicio Cloud Run prod: `mlops-onnx-api-prod`

Pruebas de endpoints:

```bash
curl https://mlops-onnx-api-dev-to5xh2n5qq-uc.a.run.app/health
curl https://mlops-onnx-api-prod-to5xh2n5qq-uc.a.run.app/health
```

Respuestas verificadas:

```json
{"status":"ok","environment":"dev"}
{"status":"ok","environment":"prod"}
```

Prueba de prediccion:

```bash
curl -X POST https://mlops-onnx-api-dev-to5xh2n5qq-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"inputs":[[1,2,3,4]]}'

curl -X POST https://mlops-onnx-api-prod-to5xh2n5qq-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"inputs":[[1,2,3,4]]}'
```

Respuesta verificada:

```json
{"environment":"dev","prediction":[[3.3000001907348633]]}
{"environment":"prod","prediction":[[3.3000001907348633]]}
```

Ejemplo de linea registrada en los archivos TXT de monitoreo:

```json
{"timestamp": "2026-06-13T03:23:55.341472+00:00", "environment": "dev", "payload": {"inputs": [[1.0, 2.0, 3.0, 4.0]]}, "prediction": [[3.3000001907348633]]}
```

## Variables para GitHub Actions en GCP

Crear estas variables por ambiente (`dev` y `prod`) en GitHub Environments:

- `GCP_PROJECT_ID`: `maestriaia`.
- `GCP_REGION`: `us-central1`.
- `ARTIFACT_REPOSITORY`: `taller-artifact-registry`.
- `CLOUD_RUN_SERVICE`: `mlops-onnx-api-dev` para `dev` y `mlops-onnx-api-prod` para `prod`.
- `MODEL_URI`: ruta `gs://bucket_taller_mlops/model.onnx`.
- `TEST_DATA_URI`: ruta `gs://bucket_taller_mlops/test_data.json`.
- `PREDICTIONS_LOG_URI`: `gs://bucket_taller_mlops/predicciones_dev.txt` o `gs://bucket_taller_mlops/predicciones_prod.txt`.

Crear este secreto por ambiente:

- `GCP_SA_KEY`: JSON de una service account con permisos sobre GCS, Artifact Registry y Cloud Run.

La API key de GCP no debe guardarse en el repositorio. Para este workflow se recomienda usar una service account y guardar su JSON como secreto `GCP_SA_KEY`.

## Preparar GCP

Con `gcloud` autenticado:

```bash
./scripts/gcloud.sh auth activate-service-account --key-file service-account.json
./scripts/setup_gcp.sh
```

El script crea o verifica el bucket, Artifact Registry y sube `model.onnx`, `test_data.json`, `predicciones_dev.txt` y `predicciones_prod.txt`.
