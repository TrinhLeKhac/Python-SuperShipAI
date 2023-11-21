import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from scripts.database.database import session
from scripts.database import models
from typing import List
from scripts.api.out_data_final import *

app = FastAPI(
    title="API SUPERSHIP", description="This is an API get calculation result from history transaction of SUPERSHIP",
    docs_url="/api"
)

db = session()


class RowAPI(BaseModel):
    id: int
    receiver_province_code: str
    receiver_district_code: str
    carrier_id: int
    order_type_id: int
    carrier_status: int
    carrier_status_comment: str
    estimate_delivery_time_details: float
    estimate_delivery_time: str
    fastest_carrier_id: int
    highest_score_carrier_id: int
    customer_best_carrier_id: int
    total_order: int
    delivery_success_rate: float
    score: float
    stars: float

    # import_date: str

    class Config:
        orm_mode = True


class RowCalc(BaseModel):
    order_code: str
    carrier_id: int
    order_type_id: int
    sys_order_type_id: int
    service_fee: int
    carrier_status: int
    carrier_status_comment: str
    estimate_delivery_time_details: float
    estimate_delivery_time: str
    delivery_success_rate: float
    customer_best_carrier_id: int
    partner_best_carrier_id: int
    cheapest_carrier_id: int
    fastest_carrier_id: int
    highest_score_carrier_id: int
    score: float
    stars: float

    class Config:
        orm_mode = True


@app.get("/v1/output/", response_model=List[RowAPI], status_code=status.HTTP_200_OK)
def get_all_rows(batch: int = 100):
    rows = db.query(models.RowAPI).limit(batch).all()
    if rows is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resources Not Found")
    return rows


@app.get("/v1/output/province/", response_model=List[RowAPI], status_code=status.HTTP_200_OK)
def get_rows_by_province_code(province_code: str = '01'):
    rows = (
        db.query(models.RowAPI)
            .filter(models.RowAPI.receiver_province_code == province_code).all()
    )
    if rows is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resources Not Found")
    return rows


@app.get("/v1/calculation/", response_model=List[RowCalc], status_code=200)
def calculate(
        order_code: str, weight: int, delivery_type_id: int,
        sender_province_code: str, sender_district_code: str,
        receiver_province_code: str, receiver_district_code: str
):
    delivery_type = None
    if delivery_type_id == 0:
        delivery_type = 'Gửi Bưu Cục'
    elif delivery_type_id == 1:
        delivery_type = 'Lấy Tận Nơi'

    df_input = pd.DataFrame(data={
        'order_code': [order_code],
        'weight': [weight],
        'pickup_type': [delivery_type],
        'sender_province_code': [sender_province_code],
        'sender_district_code': [sender_district_code],
        'receiver_province_code': [receiver_province_code],
        'receiver_district_code': [receiver_district_code],
    })
    df_output = out_data_final(df_input, show_logs=False)
    df_output = df_output[[
        'order_code', 'carrier_id', 'new_type', 'route_type',
        'price', 'status', 'description',
        'time_data', 'time_display', 'rate',
        'for_fshop', 'for_partner',
        'price_ranking', 'speed_ranking', 'score_ranking',
        'score', 'stars',
    ]]
    # print(df_output)
    final_list = []
    for i in range(len(df_output)):
        result_dict = {
            'order_code': df_output.loc[i, :]['order_code'],
            'carrier_id': df_output.loc[i, :]['carrier_id'],
            'new_type': df_output.loc[i, :]['new_type'],
            'route_type': df_output.loc[i, :]['route_type'],
            'price': df_output.loc[i, :]['price'],
            'status': df_output.loc[i, :]['status'],
            'description': df_output.loc[i, :]['description'],
            'time_data': df_output.loc[i, :]['time_data'],
            'time_display': df_output.loc[i, :]['time_display'],
            'rate': df_output.loc[i, :]['rate'],
            'for_fshop': df_output.loc[i, :]['for_fshop'],
            'for_partner': df_output.loc[i, :]['for_partner'],
            'price_ranking': df_output.loc[i, :]['price_ranking'],
            'speed_ranking': df_output.loc[i, :]['speed_ranking'],
            'score_ranking': df_output.loc[i, :]['score_ranking'],
            'score': df_output.loc[i, :]['score'],
            'stars': df_output.loc[i, :]['stars'],
        }

        final_list.append(RowCalc(**result_dict))

    return final_list


def main():
    """
    Entry point for running the FastAPI application.
    Use the following command to run the application:
    uvicorn api_main:app --reload
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
