from fastapi import APIRouter, Depends

from src.controllers.auth import get_current_account
from src.controllers.transaction import get_transactions_by_account
from src.schemas.account import AccountOut
from src.schemas.transaction import StatementOut, TransactionOut

router = APIRouter(prefix="/account", tags=["Conta"])


@router.get(
    "/statement",
    response_model=StatementOut,
    summary="Extrato da conta",
    description=(
        "Retorna o extrato completo da conta do usuário autenticado.\n\n"
        "Inclui o **saldo atual** e todas as **transações** em ordem decrescente de data."
    ),
)
async def get_statement(account: dict = Depends(get_current_account)):
    txns = await get_transactions_by_account(account["id"])
    return StatementOut(
        account=AccountOut(**account),
        transactions=[TransactionOut(**t) for t in txns],
    )
