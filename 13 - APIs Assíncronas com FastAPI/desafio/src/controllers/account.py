from src.database import database
from src.models import accounts


async def get_account_by_user_id(user_id: int) -> dict | None:
    row = await database.fetch_one(accounts.select().where(accounts.c.user_id == user_id))
    return dict(row) if row else None


async def create_account(user_id: int) -> int:
    return await database.execute(accounts.insert().values(user_id=user_id, balance=0))
