from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func, Column, TIMESTAMP
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, uuid.UUID):
                result[column.name] = str(value)
            elif isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value

        return result

    def to_safe_dict(self, exclude: list = None):
        exclude = exclude or ["email", "phone", "address"]
        return {
            key: value
            for key, value in self.to_dict().items()
            if key not in exclude
        }

    def __repr__(self):
        values = ", ".join(
            f"{col.name}={getattr(self, col.name)!r}"
            for col in self.__table__.columns
        )
        return f"<{self.__class__.__name__}({values})>"
