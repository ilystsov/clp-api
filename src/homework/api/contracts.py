"""
Contracts described in CLP API Routes and Contracts specification.
"""

from enum import Enum
from pydantic import BaseModel, Field


class AccessLevel(Enum):
    CAN_READ = "Can_Read"
    CAN_MODIFY_ORDERS = "Can_Modify_Orders"


class CreateApplicationRequest(BaseModel):
    application_name: str = Field(max_length=30)
    access_level: AccessLevel


class UpdateApplicationRequest(BaseModel):
    app_id: str
    new_access_level: AccessLevel


class DeleteApplicationRequest(BaseModel):
    app_id: str


class UserBalanceRequest(BaseModel):
    user_id: int


class CreateOrderRequest(BaseModel):
    user_id: int
    order_id: int
    total_cost: int
    completed_at: int


class DeleteOrderRequest(BaseModel):
    order_id: int


class ResponseStatus(BaseModel):
    success: bool


class ApplicationDataResponse(ResponseStatus):
    app_id: str
    token: str


class UserBalanceResponse(ResponseStatus):
    current_balance: int
