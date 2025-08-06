from fastapi import FastAPI, Body, HTTPException
import asyncpg
import os

app = FastAPI()

# Fungsi helper untuk koneksi ke PostgreSQL
async def get_conn():
    return await asyncpg.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432))
    )

# Default schema class untuk dokumentasi (tidak digunakan sebagai model pydantic)
class TableSchema:
    columns: list[str] = ["id SERIAL PRIMARY KEY", "name TEXT"]

# Endpoint untuk membuat tabel baru
@app.post("/table/{tablename}/create")
async def create_table(tablename: str, schema: dict = Body(...)):
    columns = schema.get("columns")
    if not columns:
        raise HTTPException(status_code=400, detail="Missing 'columns' field")
    columns_sql = ", ".join(columns)
    conn = await get_conn()
    await conn.execute(f'CREATE TABLE IF NOT EXISTS "{tablename}" ({columns_sql})')
    await conn.close()
    return {"status": "table_created", "table": tablename, "columns": columns}

# Endpoint untuk membaca semua row dari tabel
@app.get("/table/{tablename}/rows")
async def read_rows(tablename: str):
    conn = await get_conn()
    rows = await conn.fetch(f'SELECT * FROM "{tablename}"')
    await conn.close()
    return [dict(r) for r in rows]

# Endpoint untuk menambahkan data baru ke tabel
@app.post("/table/{tablename}/rows")
async def create_row(tablename: str, payload: dict = Body(...)):
    if not payload:
        raise HTTPException(status_code=400, detail="Empty payload")
    keys = ', '.join(f'"{k}"' for k in payload.keys())
    placeholders = ', '.join(f'${i+1}' for i in range(len(payload)))
    values = list(payload.values())
    conn = await get_conn()
    await conn.execute(
        f'INSERT INTO "{tablename}" ({keys}) VALUES ({placeholders})',
        *values
    )
    await conn.close()
    return {"status": "inserted", "table": tablename, "data": payload}

