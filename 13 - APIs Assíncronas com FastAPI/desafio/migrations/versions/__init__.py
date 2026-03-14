import sqlalchemy
from src.database import metadata

# Tabela de usuários (base para autenticação)
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String(100), unique=True, nullable=False, index=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
)

from src.models.account import accounts  # noqa: E402, F401
from src.models.transaction import transactions  # noqa: E402, F401
