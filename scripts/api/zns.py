from pydantic import BaseModel, conint, constr
from scripts.auth.security import validate_token
from fastapi import Depends
from fastapi import APIRouter
from typing import List
from scripts.database.helper import *


class ZNSModel(BaseModel):
    date: constr(strict=True)
    receiver_province: constr(strict=True)
    receiver_district: constr(strict=True)
    carrier_id: conint(strict=True)
    message_count: conint(strict=True)
    star: conint(ge=0, le=5, strict=True)
    feedbacks: List[constr(strict=True)]
    note: constr(strict=True)
    submitted_at: constr(strict=True)


router = APIRouter()


@router.post("", dependencies=[Depends(validate_token)])
def get_data_zns(request_data: ZNSModel):
    data = request_data.model_dump()  # invert method: ZNSModel(**data)
    insert_data_to_postgres(data=[data], schema_name="db_schema", table_name="zns")

    return {
        "error": False,
        "message": "",
        "data": {
            "count": 1,
            "zns": data,  # can show ZNSModel or dict
        },
    }
