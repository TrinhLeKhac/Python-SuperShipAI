from pydantic import BaseModel, conint, constr
from scripts.auth.security import validate_token
from fastapi import Depends
from fastapi import APIRouter
from scripts.database.helper import *


class OrderModel(BaseModel):
    date: constr(strict=True)
    order_code: constr(strict=True)
    created_at: constr(strict=True)
    sent_at: constr(strict=True)
    order_status: constr(strict=True)
    carrier_id: conint(strict=True)
    carrier_status: constr(strict=True)
    sender_province: constr(strict=True)
    sender_district: constr(strict=True)
    receiver_province: constr(strict=True)
    receiver_district: constr(strict=True)
    delivery_count: conint(strict=True)
    pickup: constr(strict=True)
    barter: constr(strict=True)
    carrier_delivered_at: constr(strict=True)
    picked_at: constr(strict=True)
    last_delivering_at: constr(strict=True)
    carrier_updated_at: constr(strict=True)


router = APIRouter()


@router.post("", dependencies=[Depends(validate_token)])
def get_data_order(request_data: OrderModel):
    data = request_data.model_dump()
    insert_data_to_postgres(data=[data], schema_name="db_schema", table_name="order")

    return {
        "error": False,
        "message": "",
        "data": {
            "count": 1,
            "order": data,
        },
    }
