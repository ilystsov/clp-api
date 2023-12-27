from fastapi import APIRouter
import src.homework.api.contracts as contracts

router = APIRouter()


@router.post("/")
def create_application(
    creation_request: contracts.CreateApplicationRequest,
) -> contracts.CreateApplicationResponse:
    ...


@router.put("/")
def modify_application(
    update_request: contracts.UpdateApplicationRequest,
) -> contracts.ResponseStatus:
    ...


@router.delete("/")
def delete_application(
    delete_request: contracts.DeleteApplicationRequest,
) -> contracts.ResponseStatus:
    ...
