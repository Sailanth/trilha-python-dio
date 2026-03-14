from decimal import Decimal

from src.controllers.transaction import create_transaction
from src.schemas.transaction import TransactionType
from src.services.account import deposit, withdraw


async def process_transaction(
    account_id: int,
    type: TransactionType,
    amount: Decimal,
    description: str | None,
) -> dict:
    """Processa um depósito ou saque, atualiza o saldo e registra a transação."""
    if type == TransactionType.DEPOSITO:
        await deposit(account_id, amount)
    else:
        await withdraw(account_id, amount)

    return await create_transaction(
        account_id=account_id,
        type=type.value,
        amount=amount,
        description=description,
    )
