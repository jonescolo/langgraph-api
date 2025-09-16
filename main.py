

import os
import uvicorn
from io import BytesIO
from fastapi import FastAPI, Request, File, UploadFile
import pandas as pd

app = FastAPI()

# Root route for Render health check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "LangGraph API is running"}

# Endpoint for JSON payloads from Excel VBA
@app.post("/excel-trigger")
async def handle_excel(request: Request):
    data = await request.json()
    return {"status": "success", "received": data}

# Endpoint for spreadsheet upload and analysis
@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    def classify_columns(df):
        result = {}
        for col in df.columns:
            unique_vals = df[col].dropna().unique()
            if df[col].dtype == 'object':
                result[col] = 'binary' if len(unique_vals) == 2 else 'categorical'
            elif df[col].dtype in ['int64', 'float64']:
                result[col] = 'continuous'
            else:
                result[col] = 'unknown'
        return result

    classifications = classify_columns(df)
    return {
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "classification": classifications
    }

# Entry point for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)




