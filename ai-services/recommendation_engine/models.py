from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    userId: int
    name: str
    interests: list[str]
    browsingHistory: list[int]
    searchHistory: list[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None


class Product(BaseModel):
    id: int
    title: str
    description: str
    category: str
    conditionGrade: str
    conditionType: str
    lifeScore: int
    price: float
    originalPrice: float
    rating: float
    reviewCount: int
    imageUrl: str
    aiVerified: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None


class RecommendedProduct(BaseModel):
    product: Product
    matchScore: float
    matchReasons: list[str]
    distanceKm: Optional[float] = None
    resolvedAtKm: Optional[int] = None


class RecommendationResponse(BaseModel):
    userId: int
    totalRecommendations: int
    recommendations: list[RecommendedProduct]
    resolvedAtKm: Optional[int] = None


class NearbyUser(BaseModel):
    userId: int
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    distanceKm: Optional[float] = None
    resolvedAtKm: Optional[int] = None
    interestScore: float
    distanceScore: float
    finalScore: float
    matchScore: int
    topCategories: list[str]


class NearbyUsersResponse(BaseModel):
    productId: int
    totalUsers: int
    resolvedAtKm: Optional[int] = None
    users: list[NearbyUser]
