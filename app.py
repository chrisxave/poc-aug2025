from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os

app = FastAPI()

# ✅ Tambahin ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa diganti dengan frontend URL kalau mau lebih aman
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Config
DB_USER = os.getenv("DB_USER", "devuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "openshift123")
DB_NAME = os.getenv("DB_NAME", "pocdb")
DB_HOST = os.getenv("DB_HOST", "postgresql")
DB_PORT = int(os.getenv("DB_PORT", 5432))


async def get_conn():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )


class TableSchema:
    columns: list[str] = ["id SERIAL PRIMARY KEY", "name TEXT"]


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


@app.get("/table/{tablename}/rows")
async def read_rows(tablename: str):
    conn = await get_conn()
    try:
        rows = await conn.fetch(f'SELECT * FROM "{tablename}"')
    except asyncpg.exceptions.UndefinedTableError:
        await conn.close()
        raise HTTPException(status_code=404, detail=f"Table '{tablename}' not found")
    await conn.close()
    return [dict(r) for r in rows]


@app.post("/table/{tablename}/rows")
async def create_row(tablename: str, payload: dict = Body(...)):
    if not payload:
        raise HTTPException(status_code=400, detail="Empty payload")
    keys = ', '.join(f'"{k}"' for k in payload.keys())
    placeholders = ', '.join(f'${i+1}' for i in range(len(payload)))
    values = list(payload.values())
    conn = await get_conn()
    try:
        await conn.execute(
            f'INSERT INTO "{tablename}" ({keys}) VALUES ({placeholders})',
            *values
        )
    except asyncpg.exceptions.UndefinedTableError:
        await conn.close()
        raise HTTPException(status_code=404, detail=f"Table '{tablename}' not found")
    await conn.close()
    return {"status": "inserted", "table": tablename, "data": payload}


if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=PORT)
