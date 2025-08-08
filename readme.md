# poc-aug2025

FastAPI app untuk PoC:
- Create table
- Insert data ke table
- Read data dari table

### Required Environment Variables (must be filled when deploying the app)

| Name        | Example Value        | Description             |
|-------------|----------------------|-------------------------|
| DB_USER     | appuser              | Database username       |
| DB_PASSWORD | openshift123         | Database password       |
| DB_NAME     | appdb                | Database name           |
| DB_HOST     | demo-postgres-rw     | Database service name   |
| DB_PORT     | 5432                 | Database port           |


### Build di OpenShift
```bash
oc new-app python:3.11~https://github.com/chrisxave/poc-aug2025.git \
  --name=demo-api \
  -e DB_USER=appuser \
  -e DB_PASSWORD=openshift123 \
  -e DB_NAME=appdb \
  -e DB_HOST=demo-postgres-rw \
  -e DB_PORT=5432

