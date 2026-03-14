from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class AccountOut(BaseModel):
    id: int
    user_id: int
    balance: Decimal = Field(..., description="Saldo atual da conta em reais")
    created_at: datetime

    model_config = {"from_attributes": True}
