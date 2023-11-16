from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from scripts.database.database import session
from scripts.database import models
from typing import List, Optional, Annotated
import pandas as pd
from datetime import datetime
from scripts.api.out_data_final import *

app = FastAPI(
    title="API SUPERSHIP", description="This is an API get calculation result from history transaction of SUPERSHIP",
    docs_url="/api"
)

db = session()


class RowAPI(BaseModel):
    id: int
    receiver_province_id: str
    receiver_district_id: str
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
    order_id: str
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
def get_rows_by_province_id(province_id: str = '01'):
    rows = (
        db.query(models.RowAPI)
            .filter(models.RowAPI.receiver_province_id == province_id).all()
    )
    if rows is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resources Not Found")
    return rows


@app.get("/v1/calculation/", response_model=List[RowCalc], status_code=200)
def calculate(
        order_id: str, weight: int, delivery_type_id: int,
        sender_province_id: str, sender_district_id: str,
        receiver_province_id: str, receiver_district_id: str
):
    delivery_type = None
    if delivery_type_id == 0:
        delivery_type = 'Gửi Bưu Cục'
    elif delivery_type_id == 1:
        delivery_type = 'Lấy Tận Nơi'

    df_input = pd.DataFrame(data={
        'order_id': [order_id],
        'weight': [weight],
        'delivery_type': [delivery_type],
        'sender_province_id': [sender_province_id],
        'sender_district_id': [sender_district_id],
        'receiver_province_id': [receiver_province_id],
        'receiver_district_id': [receiver_district_id],
    })
    df_output = out_data_final(df_input, show_logs=False)
    df_output = df_output[[
        'order_id', 'carrier_id', 'order_type_id', 'sys_order_type_id',
        'service_fee', 'carrier_status', 'carrier_status_comment',
        'estimate_delivery_time_details', 'estimate_delivery_time', 'delivery_success_rate',
        'customer_best_carrier_id', 'partner_best_carrier_id',
        'cheapest_carrier_id', 'fastest_carrier_id', 'highest_score_carrier_id',
        'score', 'stars',
    ]]
    # print(df_output)
    final_list = []
    for i in range(len(df_output)):
        result_dict = {
            'order_id': df_output.loc[i, :]['order_id'],
            'carrier_id': df_output.loc[i, :]['carrier_id'],
            'order_type_id': df_output.loc[i, :]['order_type_id'],
            'sys_order_type_id': df_output.loc[i, :]['sys_order_type_id'],
            'service_fee': df_output.loc[i, :]['service_fee'],
            'carrier_status': df_output.loc[i, :]['carrier_status'],
            'carrier_status_comment': df_output.loc[i, :]['carrier_status_comment'],
            'estimate_delivery_time_details': df_output.loc[i, :]['estimate_delivery_time_details'],
            'estimate_delivery_time': df_output.loc[i, :]['estimate_delivery_time'],
            'delivery_success_rate': df_output.loc[i, :]['delivery_success_rate'],
            'customer_best_carrier_id': df_output.loc[i, :]['customer_best_carrier_id'],
            'partner_best_carrier_id': df_output.loc[i, :]['partner_best_carrier_id'],
            'cheapest_carrier_id': df_output.loc[i, :]['cheapest_carrier_id'],
            'fastest_carrier_id': df_output.loc[i, :]['fastest_carrier_id'],
            'highest_score_carrier_id': df_output.loc[i, :]['highest_score_carrier_id'],
            'score': df_output.loc[i, :]['score'],
            'stars': df_output.loc[i, :]['stars'],
        }

        final_list.append(RowCalc(**result_dict))

    return final_list
