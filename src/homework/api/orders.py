from fastapi import APIRouter, Depends
from src.homework.api.contracts import (
    AccessLevel,
    CreateOrderRequest,
    ResponseStatus,
    DeleteOrderRequest,
)
from src.homework.api.security import ValidateHeader
import src.homework.db.crud as crud


router = APIRouter(
    dependencies=[Depends(ValidateHeader(AccessLevel("Can_Modify_Orders")))],
)


@router.post("/orders")
async def create_order(creation_request: CreateOrderRequest) -> ResponseStatus:
    """
    Insert an order into user's order history,
    update user's balance.

    Endpoint takes a CreateOrderRequest parameter
    Endpoint returns ResponseStatus indicating either request
    was successful or not.
    """

    if not crud.create_order_update_balance(
        order_id=creation_request.order_id,
        user_id=creation_request.user_id,
        total_cost=creation_request.total_cost,
        completed_at=creation_request.completed_at,
    ):
        return ResponseStatus(success=False)

    return ResponseStatus(success=True)


@router.delete("/orders")
async def delete_order(
    delete_request: DeleteOrderRequest,
) -> ResponseStatus:
    """
    Delete an order from the database.

    Endpoint takes a DeleteOrderRequest parameter
    Endpoint returns ResponseStatus indicating either request
    was successful or not.
    """
    if not crud.delete_order(delete_request.order_id):
        return ResponseStatus(success=False)
    return ResponseStatus(success=True)
