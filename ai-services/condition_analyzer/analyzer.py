import cv2
import numpy as np
import torch
import torchvision.transforms as T
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
from PIL import Image
import io

# ── Model (loaded once at startup) ────────────────────────────────────────────
_weights = MobileNet_V3_Small_Weights.IMAGENET1K_V1
_model = mobilenet_v3_small(weights=_weights)
_model.eval()

_transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
])

# ── OpenCV feature extraction ─────────────────────────────────────────────────

def extract_visual_features(img_bytes: bytes) -> dict:
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur_score    = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    edges         = cv2.Canny(gray, threshold1=100, threshold2=200)
    scratch_ratio = float(np.count_nonzero(edges)) / edges.size
    brightness    = float(gray.mean())
    contrast      = float(gray.std())

    return {
        "blur_score":    blur_score,
        "scratch_ratio": scratch_ratio,
        "brightness":    brightness,
        "contrast":      contrast,
    }


# ── MobileNetV3 deep-feature confidence ───────────────────────────────────────

def model_confidence(img_bytes: bytes) -> float:
    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    tensor  = _transform(pil_img).unsqueeze(0)

    with torch.no_grad():
        logits = _model(tensor)
        probs  = torch.softmax(logits, dim=1)
        top1   = float(probs.max().item())

    return top1


# ── Combined score ────────────────────────────────────────────────────────────

def compute_condition_score(img_bytes: bytes) -> tuple[float, dict]:
    feats = extract_visual_features(img_bytes)
    conf  = model_confidence(img_bytes)

    blur_norm       = min(feats["blur_score"] / 500.0, 1.0)
    scratch_norm    = max(0.0, 1.0 - feats["scratch_ratio"] / 0.15)
    brightness_norm = _bell(feats["brightness"], target=128, spread=80)
    contrast_norm   = min(feats["contrast"] / 80.0, 1.0)

    score = (
        conf            * 0.40 +
        blur_norm       * 0.25 +
        scratch_norm    * 0.20 +
        brightness_norm * 0.10 +
        contrast_norm   * 0.05
    ) * 100.0

    details = {
        "model_confidence":  round(conf, 4),
        "blur_score":        round(feats["blur_score"], 2),
        "scratch_ratio":     round(feats["scratch_ratio"], 4),
        "brightness":        round(feats["brightness"], 2),
        "contrast":          round(feats["contrast"], 2),
    }

    return round(score, 2), details


def _bell(value: float, target: float, spread: float) -> float:
    return float(np.exp(-0.5 * ((value - target) / spread) ** 2))
