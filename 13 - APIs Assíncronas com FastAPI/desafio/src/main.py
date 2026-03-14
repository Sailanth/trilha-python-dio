from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import database
from src.views import auth, account, transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Conecta ao banco na inicialização e desconecta ao encerrar."""
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    title="API Bancária Assíncrona",
    description=(
        "API RESTful assíncrona para gerenciamento de transações bancárias.\n\n"
        "## Fluxo de uso\n"
        "1. **Registre-se** em `POST /auth/register`\n"
        "2. **Obtenha um token JWT** em `POST /auth/token`\n"
        "3. Clique em **Authorize** (🔒) e cole o token\n"
        "4. Realize **depósitos e saques** em `POST /transactions/`\n"
        "5. Consulte o **extrato** em `GET /account/statement`"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(transaction.router)


@app.get("/", tags=["Health"], summary="Health check")
async def root():
    return {"status": "ok", "message": "API Bancária funcionando!"}
