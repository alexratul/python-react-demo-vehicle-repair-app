from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
import enum


class EstimateStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"


class Estimate(Base):
    __tablename__ = "estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(120))
    vehicle: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(500))
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(Enum(EstimateStatus), default=EstimateStatus.NEW)