"""
PDF Diagnostic Report Generation & Download API Route.
"""

import os
import io
import base64
import tempfile
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image

from src.services.report import create_diagnosis_pdf
import backend.routes.diagnosis as diag_module

router = APIRouter(prefix="/api/report", tags=["PDF Report"])


class PDFReportRequest(BaseModel):
    disease: str | None = None
    crop: str | None = None
    confidence: float | None = None
    severity: str | None = None
    symptoms: str | None = None
    fertilizer: str | None = None
    pesticide: str | None = None
    image_data_url: str | None = None


@router.post("/pdf")
def generate_pdf_report(req: PDFReportRequest):
    """Generates and streams a formal clinical PDF report."""
    latest = diag_module.LATEST_DIAGNOSIS

    disease = req.disease or (latest["disease"] if latest else None)
    if not disease:
        raise HTTPException(
            status_code=400,
            detail="No active diagnosis found. Please run a leaf diagnosis first."
        )

    crop = req.crop or (latest["crop"] if latest else "Agricultural Crop")
    conf_raw = req.confidence if req.confidence is not None else (latest["confidence"] if latest else 0.942)
    if conf_raw > 1.0:
        conf_raw = conf_raw / 100.0
    severity = req.severity or (latest["severity"] if latest else "Moderate")
    symptoms = req.symptoms or (latest["symptoms"] if latest else "")
    fertilizer = req.fertilizer or (latest["fertilizer"] if latest else "")
    pesticide = req.pesticide or (latest["pesticide"] if latest else "")

    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_img.close()

    try:
        if req.image_data_url and "," in req.image_data_url:
            b64_part = req.image_data_url.split(",", 1)[1]
            img_bytes = base64.b64decode(b64_part)
            Image.open(io.BytesIO(img_bytes)).convert("RGB").save(temp_img.name)
        elif latest and "image_np" in latest:
            Image.fromarray(latest["image_np"]).save(temp_img.name)

        pdf_path = os.path.join(tempfile.gettempdir(), f"AgriVision_Report_{disease.replace(' ', '_')}.pdf")
        create_diagnosis_pdf(
            image_path=temp_img.name,
            crop_name=crop,
            disease_name=disease,
            confidence=conf_raw,
            severity=severity,
            symptoms=symptoms,
            fertilizer=fertilizer,
            pesticide=pesticide,
            output_pdf_path=pdf_path
        )
    finally:
        try:
            os.remove(temp_img.name)
        except Exception:
            pass

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"AgriVision_Diagnosis_{disease.replace(' ', '_')}.pdf"
    )
