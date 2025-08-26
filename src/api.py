from fastapi import FastAPI
from pydantic import BaseModel
import os

from .data_loader import load_all
from .recommender import RecommenderSystem

# --- Inicialización de la app ---
app = FastAPI(title="Motor de Recomendaciones - Compensar")

# --- Cargar datos y modelo al iniciar ---
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

users, products, interactions = load_all(
    os.path.join(data_dir, "users.csv"),
    os.path.join(data_dir, "products.csv"),
    os.path.join(data_dir, "interactions.csv")
)

recommender = RecommenderSystem(users, products, interactions)


# --- Modelo de respuesta ---
class RecommendationResponse(BaseModel):
    product_id: int
    name: str
    category: str
    score: float


# --- Endpoints ---
@app.get("/")
def root():
    return {"message": "API Motor de Recomendaciones activo 🚀"}


@app.get("/recommendations")
def get_recommendations(user_id: int, top_n: int = 5):
    """
    Devuelve recomendaciones personalizadas para un usuario específico.
    """
    recs = recommender.recommend_for_user(user_id, top_n)

    result = [
        RecommendationResponse(
            product_id=int(row["product_id"]),
            name=str(row["name"]),          # 🔹 acceso correcto a la columna
            category=str(row["category"]),
            score=float(row["score"])
        ).dict()
        for _, row in recs.iterrows()
    ]

    return {"user_id": user_id, "recommendations": result}


@app.get("/popular")
def get_popular(top_n: int = 5):
    """
    Devuelve los productos más populares.
    """
    recs = recommender.recommend_by_popularity(top_n)

    result = [
        {
            "product_id": int(row["product_id"]),
            "name": str(row["name"]),       # 🔹 también aquí
            "category": str(row["category"]),
            "score": float(row["score"])
        }
        for _, row in recs.iterrows()
    ]

    return {"recommendations": result}

