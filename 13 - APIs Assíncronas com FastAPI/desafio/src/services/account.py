from decimal import Decimal

from src.database import database
from src.models import accounts
from src.exceptions import InsufficientBalanceException


async def deposit(account_id: int, amount: Decimal) -> Decimal:
    """Soma o valor ao saldo da conta e retorna o novo saldo."""
    async with database.transaction():
        row = await database.fetch_one(accounts.select().where(accounts.c.id == account_id))
        new_balance = Decimal(str(row["balance"])) + amount
        await database.execute(
            accounts.update().where(accounts.c.id == account_id).values(balance=new_balance)
        )
    return new_balance


async def withdraw(account_id: int, amount: Decimal) -> Decimal:
    """Debita o valor do saldo da conta. Levanta exceção se saldo insuficiente."""
    async with database.transaction():
        row = await database.fetch_one(accounts.select().where(accounts.c.id == account_id))
        current_balance = Decimal(str(row["balance"]))

        if current_balance < amount:
            raise InsufficientBalanceException(balance=f"{current_balance:.2f}")

        new_balance = current_balance - amount
        await database.execute(
            accounts.update().where(accounts.c.id == account_id).values(balance=new_balance)
        )
    return new_balance
