from typing import Optional
from recommendation_engine.models import Product, UserProfile, RecommendedProduct
from recommendation_engine.engine import build_tfidf_matrix, build_user_query, compute_similarity_scores
from recommendation_engine.data import PRODUCTS, PRODUCTS_BY_ID
from recommendation_engine import location_scoring as loc

_vectorizer, _product_matrix = build_tfidf_matrix(PRODUCTS)

_GRADE_WEIGHT = {"A": 1.0, "B": 0.80, "C": 0.60, "D": 0.40}


def recommend(user: UserProfile, top_n: int = 10) -> list[RecommendedProduct]:
    query  = build_user_query(user, PRODUCTS_BY_ID)
    scores = compute_similarity_scores(query, _vectorizer, _product_matrix)

    results: list[RecommendedProduct] = []

    for idx, product in enumerate(PRODUCTS):
        if product.id in user.browsingHistory:
            continue

        tfidf_score    = float(scores[idx])
        grade_factor   = _GRADE_WEIGHT.get(product.conditionGrade, 0.5)
        life_factor    = product.lifeScore / 100.0
        rating_factor  = product.rating / 5.0
        verified_bonus = 0.05 if product.aiVerified else 0.0

        interest = min(
            tfidf_score  * 0.55 +
            life_factor  * 0.15 +
            grade_factor * 0.15 +
            rating_factor* 0.10 +
            verified_bonus,
            1.0
        )

        dist_km, ring, d_score = loc.score_distance(
            user.latitude, user.longitude,
            product.latitude, product.longitude
        )

        final       = loc.final_score(interest, d_score)
        match_score = round(min(final * 100, 100.0), 1)
        reasons     = _build_reasons(user, product, tfidf_score, dist_km, ring)

        results.append(RecommendedProduct(
            product=product,
            matchScore=match_score,
            matchReasons=reasons,
            distanceKm=round(dist_km, 1) if dist_km is not None else None,
            resolvedAtKm=ring,
        ))

    results.sort(key=lambda r: r.matchScore, reverse=True)
    return results[:top_n]


def _build_reasons(user: UserProfile, product: Product,
                   tfidf_score: float, dist_km: Optional[float],
                   ring: Optional[int]) -> list[str]:
    reasons: list[str] = []

    browsed_in_cat = [
        pid for pid in user.browsingHistory
        if PRODUCTS_BY_ID.get(pid) and PRODUCTS_BY_ID[pid].category == product.category
    ]
    browse_count = len(browsed_in_cat)
    search_match = any(
        any(w in product.title.lower() for w in term.lower().split())
        for term in user.searchHistory
    )

    if product.category in user.interests and browse_count >= 3:
        reasons.append(f"Recommended because you frequently browse {product.category}")
    elif product.category in user.interests and browse_count > 0:
        reasons.append(f"Recommended because you browsed {product.category} items recently")
    elif search_match:
        reasons.append("Recommended because you searched for items like this")
    elif product.category in user.interests:
        reasons.append(f"Matches your interest in {product.category}")
    else:
        reasons.append(f"Expanding recommendations to {product.category}")

    purchased_signal = any(
        any(w in product.category.lower() for w in term.lower().split())
        for term in user.searchHistory
    )
    if purchased_signal and browse_count == 0:
        reasons.append("Recommended because you purchased similar products")

    if dist_km is not None:
        if ring is not None:
            reasons.append(f"Recommended because this item is available {dist_km:.0f} km away")
        else:
            reasons.append(f"Nationwide match — item is {dist_km:.0f} km away")
    else:
        reasons.append("Available nationwide")

    if product.conditionGrade == "A":
        reasons.append("Grade A condition — like new quality")
    if product.lifeScore >= 90:
        reasons.append(f"High Life Score of {product.lifeScore}/100")
    if product.aiVerified:
        reasons.append("AI-verified condition")
    if product.rating >= 4.5:
        reasons.append(f"Highly rated at {product.rating}★")

    discount = round((1 - product.price / product.originalPrice) * 100)
    if discount >= 30:
        reasons.append(f"{discount}% off original price")

    if not reasons:
        reasons.append("Recommended based on your profile")

    return reasons[:4]
