from pydantic import BaseModel, Field
from typing import Optional, Literal


Status = Literal["NEW","IN_PROGRESS","APPROVED","REJECTED","COMPLETED"]


class EstimateCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    vehicle: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    amount: float = Field(..., ge=0)


class EstimateOut(BaseModel):
    id: int
    customer_name: str
    vehicle: str
    description: str
    amount: float
    status: Status


class Config:
    from_attributes = True


class StatusUpdate(BaseModel):
    status: Status


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"