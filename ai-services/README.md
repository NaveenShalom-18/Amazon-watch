# AI Services — Unified FastAPI Application

Single FastAPI app combining all three AI microservices on **one port (8000)**.

## Services included

| Service              | Routes                            |
|----------------------|-----------------------------------|
| Condition Analyzer   | `POST /condition/analyze`         |
| Price Predictor      | `POST /price/predict`             |
| Recommendation Engine| `GET  /recommendations/{userId}`  |
|                      | `GET  /users`                     |
| Health               | `GET  /health`                    |

## Setup

```bash
cd ai-services

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Interactive docs: http://localhost:8000/docs

## Folder Structure

```
ai-services/
├── condition_analyzer/
│   ├── __init__.py
│   ├── analyzer.py      # OpenCV + MobileNetV3 inference
│   └── grader.py        # Score → A/B/C/D grade
├── price_predictor/
│   ├── __init__.py
│   ├── models.py        # Pydantic request/response schemas
│   └── predictor.py     # Pricing logic
├── recommendation_engine/
│   ├── __init__.py
│   ├── data.py          # Mock product catalogue + user profiles
│   ├── engine.py        # TF-IDF vectorizer + cosine similarity
│   ├── location_scoring.py  # Haversine + ring expansion
│   ├── models.py        # Pydantic schemas
│   └── recommender.py   # Composite scoring + match reasons
├── main.py              # Unified FastAPI entry point
├── requirements.txt
└── README.md
```

## Spring Boot integration

Update `application.properties` (already done):

```properties
condition-analyzer.base-url=http://localhost:8000
price-predictor.base-url=http://localhost:8000
```

Both services now share the same base URL. No other backend changes needed.
