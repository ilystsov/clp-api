import fastapi
import src.homework.api.contracts as contracts
from src.homework.api.security import ValidateHeader, MasterAccessLevel

router = fastapi.APIRouter(
    dependencies=[
        fastapi.Depends(ValidateHeader(MasterAccessLevel("MasterApp")))
    ]
)


@router.post("/application")
def create_application(
    creation_request: contracts.CreateApplicationRequest,
) -> contracts.CreateApplicationResponse:
    ...


@router.put("/application")
def modify_application(
    update_request: contracts.UpdateApplicationRequest,
) -> contracts.ResponseStatus:
    ...


@router.delete("/application")
def delete_application(
    delete_request: contracts.DeleteApplicationRequest,
) -> contracts.ResponseStatus:
    ...
