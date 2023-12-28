from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from .contracts import UserBalanceResponse, UserBalanceRequest, AccessLevel
from .security import ValidateHeader
import src.homework.db.crud as crud


router = APIRouter(
    dependencies=[Depends(ValidateHeader(AccessLevel("Can_Read")))],
)


@router.get("/user")
async def get_balance(
    user_id: Annotated[UserBalanceRequest, Depends()]
) -> UserBalanceResponse:
    """
    Get user's balance.

    Endpoint takes a UserBalanceRequest URL parameter
    Endpoint returns UserBalanceResponse if
    balance was retrieved successfully, and
    raises HTTPException 404 otherwise.
    """

    balance = crud.get_user_balance_by_id(user_id.user_id)
    if balance is None:
        raise HTTPException(status_code=404)
    return UserBalanceResponse(success=True, current_balance=balance)
