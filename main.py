import os
from io import BytesIO
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Dict, Any
from classifier_node import classify_sheet_payload  # Modular import

app = FastAPI()

# 🔹 Health check route for Render
@app.get("/")
def read_root() -> Dict[str, str]:
    return {"status": "ok", "message": "LangGraph API is running"}

# 🔹 JSON payload endpoint (e.g. Excel VBA trigger)
@app.post("/excel-trigger")
async def handle_excel(request: Request) -> Dict[str, Any]:
    data = await request.json()
    return {"status": "success", "received": data}

# 🔹 Spreadsheet upload and classification
@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)) -> Dict[str, Any]:
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    classifications = classify_columns(df)

    return {
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "classification": classifications
    }

# 🔹 Direct JSON classification endpoint (LangGraph/n8n/Excel VBA)
@app.post("/classify-variables-json")
async def classify_json(request: Request) -> JSONResponse:
    payload = await request.json()
    result = classify_sheet_payload(payload)
    return JSONResponse(content=result)

# 🔹 Inline fallback classifier (used by /upload-excel)
def classify_columns(df: pd.DataFrame) -> Dict[str, str]:
    result = {}
    for col in df.columns:
        unique_vals = df[col].dropna().unique()
        dtype = df[col].dtype

        if dtype == 'object':
            result[col] = 'binary' if len(unique_vals) == 2 else 'categorical'
        elif dtype.kind in {'i', 'f'}:
            result[col] = 'continuous'
        else:
            result[col] = 'unknown'

    return result

# 🔹 Local testing entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)