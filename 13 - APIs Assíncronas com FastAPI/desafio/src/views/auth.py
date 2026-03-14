from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.controllers.account import create_account
from src.controllers.auth import get_user_by_username
from src.database import database
from src.models import users
from src.schemas.auth import Token, UserCreate, UserOut
from src.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description=(
        "Cria um novo usuário com username e senha. "
        "Uma conta corrente com saldo zero é criada automaticamente."
    ),
)
async def register(payload: UserCreate):
    existing = await get_user_by_username(payload.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nome de usuário já está em uso.",
        )

    async with database.transaction():
        user_id = await database.execute(
            users.insert().values(
                username=payload.username,
                hashed_password=hash_password(payload.password),
            )
        )
        await create_account(user_id)

    row = await database.fetch_one(users.select().where(users.c.id == user_id))
    return dict(row)


@router.post(
    "/token",
    response_model=Token,
    summary="Obter token JWT",
    description=(
        "Autentica com username e senha. "
        "Retorna um token JWT Bearer para uso nos endpoints protegidos."
    ),
)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_username(form.username)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user["username"]})
    return Token(access_token=token)
