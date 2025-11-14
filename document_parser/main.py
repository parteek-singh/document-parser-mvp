# main.py
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile

from extractor import extract_pdf_text
from market_announcement import extract_market_announcement, MarketAnnouncement
# from kpi_extractor import KpiDefinition, KpiValue, extract_kpis_with_llm
from dividend_extractor import extract_dividend_info, DividendInfo


from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="Document Parser API",
    version="1.0.0",
    description="PDF text extraction, sections, tables, market announcements & KPI extraction"
)
templates = Jinja2Templates(directory="templates")


# ---------- Models for KPI endpoint ----------

# class KpiExtractionRequest(BaseModel):
#     text: str
#     kpis: List[KpiDefinition]


# class KpiExtractionResponse(BaseModel):
#     kpis: List[KpiValue]


# ---------- PDF extraction endpoints ----------

@app.post("/extract")
async def extract_from_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF → get full text + per page text + sections + tables.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        result = extract_pdf_text(tmp_path)

        return JSONResponse({
            "filename": file.filename,
            "page_count": result["page_count"],
            "full_text": result["full_text"],
            "pages": result["pages"],
            "sections": result["sections"],
            "tables": result["tables"]
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/extract/market-announcement", response_model=MarketAnnouncement)
async def extract_market_announcement_from_pdf(file: UploadFile = File(...)):
    """
    Upload a market announcement PDF → get structured announcement fields.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        result = extract_pdf_text(tmp_path)
        announcement = extract_market_announcement(
            full_text=result["full_text"],
            sections=result["sections"]
        )

        return announcement

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ---------- KPI extraction endpoint (LLM-based) ----------

# @app.post("/extract/kpis", response_model=KpiExtractionResponse)
# async def extract_kpis(req: KpiExtractionRequest):
#     """
#     LLM-based KPI extraction.
#     Client provides text + KPI definitions, service returns structured KPI values.
#     """
#     try:
#         values = extract_kpis_with_llm(req.text, req.kpis)
#         return KpiExtractionResponse(kpis=values)
#     except Exception as e:
#         return JSONResponse({"error": str(e)}, status_code=500)


# ---------- Dividend extraction endpoint ----------
@app.post("/extract/dividend", response_model=DividendInfo)
async def extract_dividend_from_pdf(file: UploadFile = File(...)):
    """
    Upload an Appendix 3A.1 style dividend PDF → get structured dividend info.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Reuse our existing PDF extractor to get text
        result = extract_pdf_text(tmp_path)
        div_info = extract_dividend_info(result["full_text"])
        return div_info

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    


# ---------- Web UI endpoints ----------

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    """
    Render the upload page.
    """
    return templates.TemplateResponse(
        "upload.html",
        {
            "request": request,
            "result": None,
            "mode": None,
            "error": None
        }
    )


@app.post("/ui/upload", response_class=HTMLResponse)
async def handle_upload(
    request: Request,
    file: UploadFile = File(...),
    mode: str = Form("full")
):
    """
    Handle file upload from the web form and render the result on the page.
    mode: 'full' | 'dividend' | 'market'
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        if mode == "dividend":
            parsed = extract_pdf_text(tmp_path)
            div_info = extract_dividend_info(parsed["full_text"])
            result = div_info.dict()

        elif mode == "market":
            parsed = extract_pdf_text(tmp_path)
            ann = extract_market_announcement(
                full_text=parsed["full_text"],
                sections=parsed["sections"]
            )
            result = ann.dict()

        else:  # full
            parsed = extract_pdf_text(tmp_path)
            result = {
                "filename": file.filename,
                "page_count": parsed["page_count"],
                "sections": parsed["sections"],
                "tables": parsed["tables"],
                # "full_text": parsed["full_text"],  # uncomment if you want to see text
            }

        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "result": result,
                "mode": mode,
                "error": None
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "result": None,
                "mode": mode,
                "error": str(e)
            }
        )