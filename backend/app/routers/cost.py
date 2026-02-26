from fastapi import APIRouter
from app.services.aws_service import get_aws_cost_data
from app.services.anomaly_service import detect_anomalies

router = APIRouter()

@router.get("/cost")
def fetch_cost(days: int = 30):
    data = get_aws_cost_data(days)
    enriched_data = detect_anomalies(data)
    return {"data": enriched_data}