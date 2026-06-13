# Manejo de secretos

El archivo `service-account.json` es una llave privada de service account. No debe subirse al repositorio.

## GitHub Actions

El workflow espera un secreto llamado `GCP_SA_KEY` en los environments `dev` y `prod`.

Con GitHub CLI:

```bash
gh secret set GCP_SA_KEY \
  --env dev \
  --body-file service-account.json

gh secret set GCP_SA_KEY \
  --env prod \
  --body-file service-account.json
```

Desde la interfaz de GitHub:

1. Ir a `Settings` > `Environments`.
2. Crear o abrir `dev`.
3. Agregar secret `GCP_SA_KEY` con el contenido completo del JSON.
4. Repetir para `prod`.

## Uso local con gcloud

```bash
./scripts/gcloud.sh auth activate-service-account \
  --key-file service-account.json

./scripts/gcloud.sh config set project maestriaia
```

## Seguridad

Si la llave privada fue compartida por chat, correo, capturas o logs, conviene rotarla desde IAM:

1. Crear una llave nueva para la misma service account.
2. Reemplazar el secreto `GCP_SA_KEY` en GitHub.
3. Eliminar la llave anterior.
