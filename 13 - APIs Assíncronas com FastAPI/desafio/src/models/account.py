import sqlalchemy
from src.database import metadata

accounts = sqlalchemy.Table(
    "accounts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        unique=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "balance",
        sqlalchemy.Numeric(18, 2),
        nullable=False,
        server_default="0.00",
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
)
