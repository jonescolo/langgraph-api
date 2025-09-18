from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from nodes.format_classifier_output import format_classifier_output
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/view_results", response_class=HTMLResponse)
def view_results(request: Request, payload: str = ""):
    if not payload:
        return HTMLResponse(content="<h2>Error: No payload provided</h2>", status_code=400)

    try:
        data = json.loads(payload)
        result = format_classifier_output(data)
        return templates.TemplateResponse("results.html", {"request": request, "columns": result["columns"]})
    except Exception as e:
        return HTMLResponse(content=f"<h2>Error parsing payload: {str(e)}</h2>", status_code=400)