from uuid import uuid4
from secrets import token_hex
import fastapi
from src.homework.api.contracts import (
    CreateApplicationRequest,
    UpdateApplicationRequest,
    DeleteApplicationRequest,
    ResponseStatus,
    ApplicationDataResponse,
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
async def create_application(
    creation_request: CreateApplicationRequest,
) -> ApplicationDataResponse | ResponseStatus:
    """
    Create a new application using MasterApp.

    Endpoint takes a CreateApplicationRequest parameter
    Endpoint returns ApplicationDataResponse if
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

    return ApplicationDataResponse(
        success=True,
        app_id=app_id,
        token=issue_token(
            app_id=app_id,
            access_level=creation_request.access_level,
            secret=secret,
        ),
    )


@router.put("/application")
async def modify_application(
    update_request: UpdateApplicationRequest,
) -> ApplicationDataResponse | ResponseStatus:
    """
    Create another application access_level.

    Endpoint takes a UpdateApplicationRequest parameter
    Endpoint returns ApplicationDataResponse if
    application was created succesfully, and
    ResponseStatus otherise.

    Technical Note: Modification is stored only in JWT, therefore,
    endpoint is a good way to broaden the access for the application.
    """
    secret = crud.get_application_secret(update_request.app_id)
    if secret is None:
        return ResponseStatus(success=False)
    return ApplicationDataResponse(
        success=True,
        app_id=update_request.app_id,
        token=issue_token(
            app_id=update_request.app_id,
            access_level=update_request.new_access_level,
            secret=secret,
        ),
    )


@router.delete("/application")
async def delete_application(
    delete_request: DeleteApplicationRequest,
) -> ResponseStatus:
    """
    Delete an application from the database.

    Endpoint takes a DeleteApplicationRequest parameter
    Endpoint returns ResponseStatus indicating either request
    was successful or not.
    """
    if not crud.delete_application(delete_request.app_id):
        return ResponseStatus(success=False)
    return ResponseStatus(success=True)
