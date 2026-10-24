"""
Multimodal Leaf Disease Diagnostic Pipeline API Routes.
Executes RT-DETR Detection, SAM 2 Segmentation, Grad-CAM++ Explainability, and ConvNeXt V2 Classification.
"""

import io
import time
import base64
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from PIL import Image
import numpy as np

from src.config import get_sample_image_path
from src.models.inference import predict_leaf_disease
from src.knowledge.treatments import get_treatment_for_disease
from src.services.translation import translate_text

router = APIRouter(prefix="/api/diagnose", tags=["Diagnosis"])

# In-memory store for the latest diagnosis & recent session history
LATEST_DIAGNOSIS: dict | None = None
DIAGNOSIS_HISTORY: list[dict] = []


def np_to_data_url(img_np: np.ndarray, quality: int = 92) -> str:
    """Encodes an RGB numpy array into a base64 JPEG Data URL."""
    pil_img = Image.fromarray(img_np.astype(np.uint8))
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=quality)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def run_full_diagnosis(pil_image: Image.Image, lang_code: str = "en", source_name: str = "Uploaded Specimen") -> dict:
    """Runs the 3-stage pipeline and returns a structured, UI-ready diagnostic payload."""
    global LATEST_DIAGNOSIS, DIAGNOSIS_HISTORY

    t0 = time.perf_counter()
    img_rgb = pil_image.convert("RGB")
    orig_np = np.array(img_rgb)

    det_img, seg_img, cam_img, disease, conf, top_3, severity_pct, num_boxes = predict_leaf_disease(img_rgb)
    info = get_treatment_for_disease(disease)
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)

    # Categorize severity
    if severity_pct < 0.15:
        severity_label = "Mild"
        severity_key = "mild"
        severity_desc = "Foliar surface damage is contained (<15%). Rapid canopy recovery anticipated."
    elif severity_pct < 0.35:
        severity_label = "Moderate"
        severity_key = "moderate"
        severity_desc = "Moderate infection threshold (15–35%). Prompt targeted fungicidal intervention indicated."
    else:
        severity_label = "Severe"
        severity_key = "severe"
        severity_desc = "Critical foliar necrosis (>35%). Aggressive curative intervention required immediately."

    # Compute normalized Top-3 differential probabilities
    prob_sum = sum(p for _, p in top_3) if top_3 else 1.0
    differential = []
    for cls_name, prob in top_3:
        rel_pct = (prob / prob_sum) * 100 if prob_sum > 0 else prob * 100
        cls_info = get_treatment_for_disease(cls_name)
        differential.append({
            "disease": cls_name,
            "raw_probability": round(prob * 100, 2),
            "relative_pct": round(rel_pct, 1),
            "crop": cls_info["crop"],
            "symptoms": cls_info["symptoms"]
        })

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rx_id = f"AV-{datetime.now().strftime('%Y%m%d')}-{abs(hash(disease + timestamp_str)) % 9000 + 1000}"

    # Translate clinical strings if requested language is not English
    pesticide_tr = translate_text(info["pesticide"], lang_code)
    fertilizer_tr = translate_text(info["fertilizer"], lang_code)
    symptoms_tr = translate_text(info["symptoms"], lang_code)
    market_tr = translate_text(info.get("market_impact", ""), lang_code)

    orig_b64 = np_to_data_url(orig_np)
    det_b64 = np_to_data_url(det_img)
    seg_b64 = np_to_data_url(seg_img)
    cam_b64 = np_to_data_url(cam_img)

    # Save raw detection numpy array in LATEST_DIAGNOSIS for FPDF export
    LATEST_DIAGNOSIS = {
        "rx_id": rx_id,
        "timestamp": timestamp_str,
        "disease": disease,
        "crop": info["crop"],
        "confidence": conf,
        "severity": severity_label,
        "severity_pct": round(severity_pct * 100, 1),
        "symptoms": info["symptoms"],
        "fertilizer": info["fertilizer"],
        "pesticide": info["pesticide"],
        "market_impact": info.get("market_impact", ""),
        "image_np": det_img
    }

    result_payload = {
        "rx_id": rx_id,
        "timestamp": timestamp_str,
        "source_name": source_name,
        "inference_ms": elapsed_ms,
        "disease": disease,
        "crop": info["crop"],
        "confidence": round(conf * 100, 1),
        "confidence_raw": conf,
        "num_lesions": num_boxes,
        "infected_area_pct": round(severity_pct * 100, 1),
        "severity": {
            "label": severity_label,
            "key": severity_key,
            "description": severity_desc
        },
        "differential": differential,
        "treatment": {
            "pesticide": pesticide_tr,
            "fertilizer": fertilizer_tr,
            "symptoms": symptoms_tr,
            "market_impact": market_tr,
            "raw": {
                "pesticide": info["pesticide"],
                "fertilizer": info["fertilizer"],
                "symptoms": info["symptoms"],
                "market_impact": info.get("market_impact", "")
            }
        },
        "images": {
            "original": orig_b64,
            "detection": det_b64,
            "segmentation": seg_b64,
            "gradcam": cam_b64
        }
    }

    # Prepend to history (keep last 10)
    history_entry = {
        "rx_id": rx_id,
        "timestamp": timestamp_str,
        "disease": disease,
        "crop": info["crop"],
        "confidence": round(conf * 100, 1),
        "severity": severity_label,
        "infected_area_pct": round(severity_pct * 100, 1),
        "num_lesions": num_boxes,
        "thumbnail": det_b64
    }
    DIAGNOSIS_HISTORY.insert(0, history_entry)
    DIAGNOSIS_HISTORY[:] = DIAGNOSIS_HISTORY[:10]

    return result_payload


@router.post("/analyze")
async def analyze_uploaded_leaf(
    file: UploadFile = File(...),
    lang: str = Form("en")
):
    """Runs multimodal diagnostic pipeline on an uploaded leaf image."""
    try:
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    return run_full_diagnosis(pil_img, lang_code=lang, source_name=file.filename or "Uploaded Leaf")


@router.post("/sample")
def analyze_sample_leaf(lang: str = "en"):
    """Runs multimodal diagnostic pipeline on the built-in field sample leaf."""
    sample_path = get_sample_image_path()
    try:
        pil_img = Image.open(sample_path)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Sample image not found: {str(e)}")

    return run_full_diagnosis(pil_img, lang_code=lang, source_name="Field Sample (photo_2026-10-24_01-39-50.png)")


class TranslatePrescriptionRequest(BaseModel):
    pesticide: str
    fertilizer: str
    symptoms: str
    market_impact: str = ""
    lang: str


@router.post("/translate-rx")
def translate_prescription(req: TranslatePrescriptionRequest):
    """Translates an existing prescription when the user switches language in the UI."""
    return {
        "pesticide": translate_text(req.pesticide, req.lang),
        "fertilizer": translate_text(req.fertilizer, req.lang),
        "symptoms": translate_text(req.symptoms, req.lang),
        "market_impact": translate_text(req.market_impact, req.lang)
    }


@router.get("/history")
def get_diagnosis_history():
    """Returns recent diagnostic records from the current session."""
    return {"history": DIAGNOSIS_HISTORY}
