from uuid import uuid4
from secrets import token_hex
import fastapi
from src.homework.api.contracts import (
    CreateApplicationRequest,
    UpdateApplicationRequest,
    DeleteApplicationRequest,
    ResponseStatus,
    CreateApplicationResponse,
)
from src.homework.api.security import (
    ValidateHeader,
    MasterAccessLevel,
    issue_token,
)
import src.homework.db.crud as crud

router = fastapi.APIRouter(
    dependencies=[
        fastapi.Depends(ValidateHeader(MasterAccessLevel("MasterApp")))
    ]
)


@router.post("/application")
def create_application(
    creation_request: CreateApplicationRequest,
) -> CreateApplicationResponse | ResponseStatus:
    """
    Create a new application using MasterApp.

    Endpoint takes a CreateApplicationRequest parameter
    Endpoint returns CreateApplicationResponse if
    application was created succesfully, and
    ResponseStatus otherise.
    """

    app_id, secret = str(uuid4()), token_hex(32)

    if not crud.create_application(
        app_id=app_id,
        app_name=creation_request.application_name,
        secret=secret,
    ):
        return ResponseStatus(success=False)

    return CreateApplicationResponse(
        success=True,
        app_id=app_id,
        token=issue_token(
            app_id=app_id,
            access_level=creation_request.access_level,
            secret=secret,
        ),
    )


@router.put("/application")
def modify_application(
    update_request: UpdateApplicationRequest,
) -> ResponseStatus:
    ...


@router.delete("/application")
def delete_application(
    delete_request: DeleteApplicationRequest,
) -> ResponseStatus:
    ...
