from datetime import date
import json
import os
from typing import Optional
from dapla_suv_tools.pagination import PaginationInfo
from datetime import date, datetime

from ssb_altinn3_util.models.skjemadata.skjemadata_request_models import (
    UtsendingRequestModel,
)

from dapla_suv_tools._internals.integration.api_client import SuvApiClient
from dapla_suv_tools._internals.integration import user_tools
from dapla_suv_tools._internals.util import constants
from dapla_suv_tools._internals.util.decorators import result_to_dict
from dapla_suv_tools._internals.util.operation_result import OperationResult
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util.validators import (
    pulje_id_validator,
    periode_id_validator
)



END_USER_API_BASE_URL = os.getenv("SUV_END_USER_API_URL", "")

client = SuvApiClient(base_url=END_USER_API_BASE_URL)



@result_to_dict
@SuvOperationContext(validator=pulje_id_validator)
def create_utsending(
    self,
    *,
    pulje_id: int,
    utsendingstype_id: int | None = None,
    utsendingstype_navn: str | None = None,
    trigger: str | None = "Manuell",
    test: bool | None = False,
    altinn_uts_tidspunkt: datetime | None = None,
    context: SuvOperationContext,
) -> OperationResult:

    """
    Creates a new pulje with the specified details.

    Parameters:
    ------------
    skjema_id: int
        The skjema_id associated with the new period.
    periode_type: Optional[str]
        Periode type of the new periode.
    periode_aar: Optional[int]
        Year of the new periode.
    context: SuvOperationContext
        Operation context for logging and error handling. This is injected by the underlying pipeline.

    Returns:
    --------
    OperationResult:
        An object containing the ID of the created period, or an error message if the creation fails.

    Example:
    ---------
    result = create_periode(
        skjema_id=456, periode_type="KVRT", periode_aar=2023, periode_nr=1
    )
    """    

    
    user = user_tools.get_current_user(context)

    model = UtsendingRequestModel(
        pulje_id=pulje_id,
        utsendingstype_navn=utsendingstype_navn,
        utsendingstype_id=utsendingstype_id,
        trigger=trigger,
        test=test,
        altinn_uts_tidspunkt=altinn_uts_tidspunkt,
        endret_av=user
    )

    try:
        body = model.model_dump_json()
        content: str = client.post(
            path=constants.UTSENDING_PATH, body_json=body, context=context
        )
        new_id = json.loads(content)["id"]
        context.log(message="Created 'utsending' with id '{new_id}'")
        return OperationResult(value={"id": new_id}, log=context.logs())
    except Exception as e:
        context.set_error(
            f"Failed to create utsending for pulje_id '{pulje_id}'",
            e,
        )
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )
