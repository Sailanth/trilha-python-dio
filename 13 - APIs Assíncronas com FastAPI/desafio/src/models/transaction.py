import sqlalchemy
from src.database import metadata

transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column(
        "account_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("accounts.id"),
        nullable=False,
        index=True,
    ),
    sqlalchemy.Column("type", sqlalchemy.String(10), nullable=False),  # "deposito" | "saque"
    sqlalchemy.Column("amount", sqlalchemy.Numeric(18, 2), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(255), nullable=True),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
)
