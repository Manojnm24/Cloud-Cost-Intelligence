from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cost_model import Cost
from app.services.aws_service import get_aws_cost_data
from app.services.anomaly_service import detect_anomalies
from app.schemas.cost_schema import CostResponse

router = APIRouter()


@router.get("/cost", response_model=list[CostResponse])
def fetch_cost(days: int = 30, db: Session = Depends(get_db)):

    # Step 1: Fetch AWS data
    data = get_aws_cost_data(days)

    # Step 2: Detect anomalies + explanations
    enriched_data = detect_anomalies(data)

    # Step 3: Clear old stored data
    db.query(Cost).delete()

    # Step 4: Store fresh data
    for item in enriched_data:
        cost_entry = Cost(
            date=item["date"],
            total_cost=item["total_cost"],
            anomaly=item["anomaly"]
        )
        db.add(cost_entry)

    db.commit()

    # Step 5: Return enriched response directly
    return [
        CostResponse(
            id=index,
            date=item["date"],
            total_cost=item["total_cost"],
            services=item["services"],
            anomaly=item["anomaly"],
            explanation=item.get("explanation"),
            severity=item.get("severity")
        )
        for index, item in enumerate(enriched_data)
    ]