"""
AI Services — unified FastAPI application.

Routes:
  POST /condition/analyze          → condition_analyzer
  POST /price/predict              → price_predictor
  GET  /recommendations/{userId}   → recommendation_engine
  GET  /users                      → recommendation_engine
  GET  /health                     → global health check
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Sub-module imports ────────────────────────────────────────────────────────
from condition_analyzer.analyzer import compute_condition_score
from condition_analyzer.grader import assign_grade
from price_predictor.models import PricePredictionRequest, PricePredictionResponse
from price_predictor.predictor import predict as predict_price
from recommendation_engine.data import USERS_BY_ID
from recommendation_engine.models import RecommendationResponse
from recommendation_engine.recommender import recommend

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Amazon ReMatch — AI Services",
    description=(
        "Unified AI microservice combining condition analysis, price prediction, "
        "and product recommendations."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Condition Analyzer ────────────────────────────────────────────────────────

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}


class ConditionResponse(BaseModel):
    grade: str
    label: str
    confidence: float
    condition_score: float
    details: dict


@app.post("/condition/analyze", response_model=ConditionResponse, tags=["condition"])
async def analyze_condition(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. Use JPEG, PNG, WEBP, or BMP.",
        )

    img_bytes = await file.read()
    if len(img_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        condition_score, details = compute_condition_score(img_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    result = assign_grade(condition_score)

    return ConditionResponse(
        grade=result.grade,
        label=result.label,
        confidence=result.confidence,
        condition_score=result.condition_score,
        details=details,
    )


# ── Price Predictor ───────────────────────────────────────────────────────────

@app.post("/price/predict", response_model=PricePredictionResponse, tags=["price"])
def predict_price_endpoint(request: PricePredictionRequest) -> PricePredictionResponse:
    return predict_price(request)


# ── Recommendation Engine ─────────────────────────────────────────────────────

@app.get("/recommendations/{userId}", response_model=RecommendationResponse, tags=["recommendations"])
def get_recommendations(
    userId: int,
    top: int = Query(default=10, ge=1, le=20, description="Max results to return"),
):
    user = USERS_BY_ID.get(userId)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {userId} not found")

    results = recommend(user, top_n=top)

    return RecommendationResponse(
        userId=userId,
        totalRecommendations=len(results),
        recommendations=results,
    )


@app.get("/users", summary="List all mock users", tags=["recommendations"])
def list_users():
    return [
        {"userId": u.userId, "name": u.name, "interests": u.interests}
        for u in USERS_BY_ID.values()
    ]


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "services": ["condition-analyzer", "price-predictor", "recommendation-engine"]}
