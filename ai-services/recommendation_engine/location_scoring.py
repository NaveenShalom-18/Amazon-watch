import math
from typing import Optional

RINGS = [25, 50, 100]
NATIONWIDE_KM = 5000.0
INTEREST_WEIGHT = 0.70
DISTANCE_WEIGHT = 0.30


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def distance_score(distance_km: float, ring_km: float) -> float:
    return max(0.0, 1.0 - (distance_km / ring_km))


def resolved_ring(distance_km: float) -> Optional[int]:
    for r in RINGS:
        if distance_km <= r:
            return r
    return None


def final_score(interest: float, distance: float) -> float:
    return round(INTEREST_WEIGHT * interest + DISTANCE_WEIGHT * distance, 4)


def score_distance(user_lat, user_lon, prod_lat, prod_lon):
    if None in (user_lat, user_lon, prod_lat, prod_lon):
        return None, None, 0.2

    dist   = haversine(user_lat, user_lon, prod_lat, prod_lon)
    ring   = resolved_ring(dist)
    boundary = ring if ring is not None else NATIONWIDE_KM
    dscore = distance_score(dist, boundary)
    return dist, ring, dscore
