from pydantic import BaseModel, conint, constr, confloat
from scripts.auth.security import validate_token
from fastapi import Depends
from fastapi import APIRouter
from scripts.database.database import session
from scripts.database import models


class OutputModel(BaseModel):
    # id: conint(strict=True)
    receiver_province_code: constr(strict=True)
    receiver_district_code: constr(strict=True)
    carrier_id: conint(strict=True)
    new_type: constr(strict=True)
    route_type: constr(strict=True)
    status: constr(strict=True)
    description: constr(strict=True)
    time_data: confloat(strict=True)
    time_display: constr(strict=True)
    speed_ranking: conint(strict=True)
    score_ranking: conint(strict=True)
    for_shop: conint(strict=True)
    total_order: conint(strict=True)
    # rate_ranking: conint(strict=True)
    rate: confloat(strict=True)
    score: confloat(strict=True)
    star: confloat(strict=True)
    # import_date: constr(strict=True)

    class Config:
        orm_mode = True


db = session()
router = APIRouter()


@router.get("", dependencies=[Depends(validate_token)])
def get_all_rows(batch: int = 10):
    rows = db.query(models.Output29946API).limit(batch).all()
    if rows is None:
        return {
            "error": True,
            "message": "Resources not found",
            "data": [],
        }
    else:
        return {
            "error": False,
            "message": "",
            "data": rows,
        }


@router.get("/district", dependencies=[Depends(validate_token)])
def get_rows_by_district_code(district_code: str = "001"):
    rows = (
        db.query(models.Output29946API)
            .filter(models.Output29946API.receiver_district_code == district_code).all()
    )
    if rows is None:
        return {
            "error": True,
            "message": "Resources not found",
            "data": [],
        }
    else:
        return {
            "error": False,
            "message": "",
            "data": rows,
        }
