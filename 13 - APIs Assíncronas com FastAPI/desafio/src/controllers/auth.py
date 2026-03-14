from fastapi import Depends, HTTPException, status

from src.database import database
from src.models import users, accounts
from src.security import get_token_payload


async def get_user_by_username(username: str) -> dict | None:
    row = await database.fetch_one(users.select().where(users.c.username == username))
    return dict(row) if row else None


async def get_current_user(payload: dict = Depends(get_token_payload)) -> dict:
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")

    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado.")
    return user


async def get_current_account(current_user: dict = Depends(get_current_user)) -> dict:
    row = await database.fetch_one(accounts.select().where(accounts.c.user_id == current_user["id"]))
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")
    return dict(row)
