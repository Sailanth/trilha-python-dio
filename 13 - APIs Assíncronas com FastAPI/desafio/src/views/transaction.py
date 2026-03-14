from fastapi import APIRouter, Depends, status

from src.controllers.auth import get_current_account
from src.schemas.transaction import TransactionCreate, TransactionOut
from src.services.transaction import process_transaction

router = APIRouter(prefix="/transactions", tags=["Transações"])


@router.post(
    "/",
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar transação",
    description=(
        "Registra um **depósito** ou **saque** na conta do usuário autenticado.\n\n"
        "- **Depósito:** soma o valor ao saldo da conta.\n"
        "- **Saque:** debita o valor — bloqueado se saldo insuficiente.\n"
        "- Valores negativos ou zero são **rejeitados**."
    ),
)
async def create_transaction(
    payload: TransactionCreate,
    account: dict = Depends(get_current_account),
):
    txn = await process_transaction(
        account_id=account["id"],
        type=payload.type,
        amount=payload.amount,
        description=payload.description,
    )
    return txn
