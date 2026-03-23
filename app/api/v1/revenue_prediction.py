from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.ai.revenue_prediction import predict_deal_probability

router = APIRouter(
    prefix="/api/v1/revenue",
    tags=["Revenue Prediction"]
)


@router.post("/predict")
def predict(data: dict, user=Depends(get_current_user)):
    probability = predict_deal_probability(data)

    return {
        "success_probability": probability,
        "user": user
    }