"""
Model Loaders for ConvNeXt V2, RT-DETR, and SAM 2.1.
Uses functools.lru_cache for framework-agnostic singleton model caching (works in FastAPI & Streamlit).
"""

import os
import json
from functools import lru_cache
from src.config import BASE_DIR, TRAINED_DATA_DIR, DISEASE_CLASSES_PATH, TOP20_CLASSES_PATH, TOP40_CLASSES_PATH

RAW_MODEL_URLS = {
    "best_convnextv2_top20.pth": "https://github.com/Adithyan-b-raj/Agrivision/raw/main/trained%20data/best_convnextv2_top20.pth",
    "best_rtdetr_leaf_disease.pt": "https://github.com/Adithyan-b-raj/Agrivision/raw/main/trained%20data/best_rtdetr_leaf_disease.pt",
    "sam2.1_t.pt": "https://github.com/Adithyan-b-raj/Agrivision/raw/main/sam2.1_t.pt",
    "top20_disease_classes.json": "https://github.com/Adithyan-b-raj/Agrivision/raw/main/trained%20data/top20_disease_classes.json"
}

def ensure_model_file_valid(file_path: str, model_key: str):
    """
    Checks if a model file is missing or is an un-pulled Git LFS text pointer (< 1 MB).
    If so, automatically downloads the full binary weights from GitHub raw release storage.
    Ensures seamless execution even when users click 'Download ZIP' from GitHub without Git LFS.
    """
    raw_url = RAW_MODEL_URLS.get(model_key)
    if not raw_url:
        return
    
    is_pointer_or_missing = not os.path.exists(file_path) or os.path.getsize(file_path) < 1000000
    if is_pointer_or_missing:
        print(f"[*] Auto-downloading full {model_key} weights from GitHub (resolving LFS pointer)...")
        try:
            import requests
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with requests.get(raw_url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            print(f"✅ Successfully downloaded {model_key} ({os.path.getsize(file_path)} bytes)!")
        except Exception as e:
            print(f"[!] Notice: Could not auto-download {model_key}: {e}")


@lru_cache(maxsize=1)
def load_trained_convnext_model():
    """Dynamically loads ConvNeXt V2 model checkpoint (prefers Top-20 high-accuracy model from trained data/, else fallback)."""
    # Ensure Top-20 model is valid binary (auto-downloads if downloaded as GitHub ZIP)
    target_top20 = os.path.join(TRAINED_DATA_DIR, "best_convnextv2_top20.pth")
    target_json = os.path.join(TRAINED_DATA_DIR, "top20_disease_classes.json")
    ensure_model_file_valid(target_top20, "best_convnextv2_top20.pth")
    if not os.path.exists(target_json) or os.path.getsize(target_json) < 10:
        ensure_model_file_valid(target_json, "top20_disease_classes.json")

    weights_path = ""
    json_path = TOP20_CLASSES_PATH
    
    # Priority cascade: Top-20 distinct model -> Top-40 model -> All-classes model -> default
    candidates = [
        ("best_convnextv2_top20.pth", TOP20_CLASSES_PATH),
        ("best_convnextv2_top20 (1).pth", TOP20_CLASSES_PATH),
        ("best_convnextv2_top40.pth", TOP40_CLASSES_PATH),
        ("best_convnextv2_all_classes.pth", DISEASE_CLASSES_PATH),
        ("best_convnextv2.pth", DISEASE_CLASSES_PATH)
    ]
    
    # Search first in 'trained data/' directory, then root BASE_DIR
    found = False
    for s_dir in [TRAINED_DATA_DIR, BASE_DIR]:
        for candidate_w, candidate_j in candidates:
            full_w = os.path.join(s_dir, candidate_w)
            if os.path.exists(full_w):
                weights_path = full_w
                if os.path.exists(candidate_j):
                    json_path = candidate_j
                elif os.path.exists(os.path.join(s_dir, "top20_disease_classes.json")):
                    json_path = os.path.join(s_dir, "top20_disease_classes.json")
                found = True
                break
        if found:
            break

    classes_list = [
        "citrus canker", "wheat stripe rust", "wheat head scab", "grape downy mildew",
        "wheat powdery mildew", "apple scab", "soybean frog eye leaf spot", "bean rust"
    ]
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if isinstance(loaded, list) and len(loaded) > 0:
                    classes_list = loaded
        except Exception as e:
            print(f"Disease classes json notice: {e}")

    if not weights_path or not os.path.exists(weights_path):
        return None, classes_list

    try:
        import torch
        import timm
        state_dict = torch.load(weights_path, map_location=torch.device('cpu'))
        
        if 'head.fc.weight' in state_dict:
            ckpt_classes = state_dict['head.fc.weight'].shape[0]
        else:
            ckpt_classes = len(classes_list)
            
        model = timm.create_model('convnextv2_tiny', pretrained=False, num_classes=ckpt_classes)
        model.load_state_dict(state_dict)
        model.eval()
        
        if ckpt_classes == len(classes_list):
            classes = classes_list
        elif len(classes_list) >= ckpt_classes:
            classes = classes_list[:ckpt_classes]
        else:
            classes = [f"Pathology #{i+1}" for i in range(ckpt_classes)]
            
        return model, classes
    except Exception as e:
        print(f"PyTorch model load notice: {e}")
        return None, classes_list


@lru_cache(maxsize=1)
def load_rtdetr_model():
    """Loads RT-DETR (prefers fine-tuned leaf disease checkpoint from trained data/, else standard RT-DETR)."""
    target_rtdetr = os.path.join(TRAINED_DATA_DIR, "best_rtdetr_leaf_disease.pt")
    ensure_model_file_valid(target_rtdetr, "best_rtdetr_leaf_disease.pt")

    try:
        from ultralytics import RTDETR
        candidates = [
            "best_rtdetr_leaf_disease.pt",
            "best_rtdetr_leaf_disease (1).pt",
            "rtdetr_plantseg.pt",
            "rtdetr-l.pt"
        ]
        for s_dir in [TRAINED_DATA_DIR, BASE_DIR]:
            for candidate in candidates:
                p = os.path.join(s_dir, candidate)
                if os.path.exists(p):
                    return RTDETR(p), candidate
        return RTDETR("rtdetr-l.pt"), "rtdetr-l.pt"
    except Exception as e:
        print(f"RT-DETR load notice: {e}")
        return None, None


@lru_cache(maxsize=1)
def load_sam2_model():
    """Loads Segment Anything Model 2 (Meta SAM 2.1 zero-shot foundation model)."""
    target_sam = os.path.join(BASE_DIR, "sam2.1_t.pt")
    ensure_model_file_valid(target_sam, "sam2.1_t.pt")

    try:
        from ultralytics import SAM
        for s_dir in [TRAINED_DATA_DIR, BASE_DIR]:
            weights_path = os.path.join(s_dir, "sam2.1_t.pt")
            if os.path.exists(weights_path):
                return SAM(weights_path)
        return SAM("sam2.1_t.pt")
    except Exception as e:
        print(f"SAM 2 load notice: {e}")
        return None
