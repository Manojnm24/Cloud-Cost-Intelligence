from pydantic import BaseModel
from typing import List
from typing import Optional

class ServiceCost(BaseModel):
    name: str
    cost: float


class CostResponse(BaseModel):
    id: int
    date: str
    total_cost: float
    services: List[ServiceCost]
    anomaly: bool
    explanation: Optional[str] = None
    severity: Optional[str] = None