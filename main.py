import os
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/excel-trigger")
async def handle_excel(request: Request):
    data = await request.json()
    return {"status": "success", "received": data}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

