from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/excel-trigger")
async def handle_excel(request: Request):
    data = await request.json()
    # Process data here (e.g., LangGraph logic)
    return {"status": "success", "received": data}
