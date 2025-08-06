# poc-aug2025

FastAPI app untuk PoC:
- Create table
- Insert data ke table
- Read data dari table

### Environment Variables
Aplikasi ini membaca environment variables berikut (diatur di OpenShift DeploymentConfig atau BuildConfig):

- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_NAME`
- `DATABASE_HOST`
- `DATABASE_PORT`

### Build di OpenShift
```bash
oc new-app python:3.11~https://github.com/<user>/<repo>.git \
  --name=demo-api \
  -e DATABASE_USER=appuser \
  -e DATABASE_PASSWORD=openshift123 \
  -e DATABASE_NAME=appdb \
  -e DATABASE_HOST=demo-postgres-rw \
  -e DATABASE_PORT=5432

