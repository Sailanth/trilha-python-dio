from src.database import database
from src.models import transactions


async def get_transactions_by_account(account_id: int) -> list[dict]:
    rows = await database.fetch_all(
        transactions.select()
        .where(transactions.c.account_id == account_id)
        .order_by(transactions.c.created_at.desc())
    )
    return [dict(r) for r in rows]


async def create_transaction(account_id: int, type: str, amount, description: str | None) -> dict:
    txn_id = await database.execute(
        transactions.insert().values(
            account_id=account_id,
            type=type,
            amount=amount,
            description=description,
        )
    )
    row = await database.fetch_one(transactions.select().where(transactions.c.id == txn_id))
    return dict(row)
