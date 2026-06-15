import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation_engine.models import Product, UserProfile


def _build_product_corpus(products: list[Product]) -> list[str]:
    docs = []
    for p in products:
        doc = " ".join([
            p.title,
            p.description,
            p.category * 3,
            p.conditionType,
            p.conditionGrade * 2,
        ])
        docs.append(doc.lower())
    return docs


def build_tfidf_matrix(products: list[Product]):
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        max_features=500,
    )
    corpus = _build_product_corpus(products)
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix


def build_user_query(user: UserProfile, products_by_id: dict[int, Product]) -> str:
    parts: list[str] = []
    for interest in user.interests:
        parts.extend([interest] * 3)
    parts.extend(user.searchHistory)
    for pid in user.browsingHistory:
        p = products_by_id.get(pid)
        if p:
            parts.append(p.title)
            parts.append(p.category)
    return " ".join(parts).lower()


def compute_similarity_scores(user_query: str, vectorizer: TfidfVectorizer, product_matrix) -> np.ndarray:
    user_vec = vectorizer.transform([user_query])
    return cosine_similarity(user_vec, product_matrix).flatten()
