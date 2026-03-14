from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.schemas.account import AccountOut


class TransactionType(str, Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"


class TransactionCreate(BaseModel):
    type: TransactionType = Field(..., description="Tipo da transação: 'deposito' ou 'saque'")
    amount: Decimal = Field(..., description="Valor da transação (deve ser maior que zero)")
    description: Optional[str] = Field(None, max_length=255, description="Descrição opcional")

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("O valor da transação deve ser maior que zero.")
        return v


class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: TransactionType
    amount: Decimal
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class StatementOut(BaseModel):
    account: AccountOut
    transactions: list[TransactionOut]
