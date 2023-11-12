from scripts.utilities.helper import *
from scripts.utilities.config import *


def status_chat_luong_noi_bo_ninja_van(series, col1='delivery_success_rate', col2='is_more_than_100'):
    if series[col1] == 0:
        return 'Không có thông tin'
    elif (series[col1] >= 0.95) & series[col2]:
        return 'Ti lệ trên 95% và tổng số đơn giao hàng trên 100 đơn'
    elif (series[col1] >= 0.9) & (series[col1] < 0.95) & series[col2]:
        return 'Ti lệ trên 90% và tổng số đơn giao hàng trên 100 đơn'
    elif (series[col1] < 0.9) & series[col2]:
        return 'Ti lệ dưới 90% và tổng số đơn giao hàng trên 100 đơn'
    elif (series[col1] >= 0.95) & (~series[col2]):
        return 'Ti lệ trên 95% và tổng số đơn giao hàng dưới 100 đơn'
    elif (series[col1] >= 0.9) & (series[col1] < 0.95) & (~series[col2]):
        return 'Ti lệ trên 90% và tổng số đơn giao hàng dưới 100 đơn'
    elif (series[col1] < 0.9) & (~series[col2]):
        return 'Ti lệ dưới 90% và tổng số đơn giao hàng dưới 100 đơn'


def transform_data_chat_luong_noi_bo():

    chat_luong_noi_bo_df = pd.read_parquet('./processed_data/chat_luong_noi_bo_njv.parquet')

    chat_luong_noi_bo_df['status'] = chat_luong_noi_bo_df.apply(status_chat_luong_noi_bo_ninja_van, axis=1)
    chat_luong_noi_bo_df['score'] = (
        chat_luong_noi_bo_df['status'].map(TRONG_SO['Chất lượng nội bộ']['Phân loại']['Ninja Van'])
    )

    chat_luong_noi_bo_df = (
        chat_luong_noi_bo_df.merge(
            PROVINCE_MAPPING_DISTRICT_DF[['province', 'district']].rename(columns={
                'province': 'receiver_province',
                'district': 'receiver_district'
            }), on=['receiver_province', 'receiver_district'], how='right')
    )
    chat_luong_noi_bo_df['status'] = chat_luong_noi_bo_df['status'].fillna('Không có thông tin')
    chat_luong_noi_bo_df['score'] = chat_luong_noi_bo_df['score'].fillna(5)

    chat_luong_noi_bo_df['carrier'] = 'Ninja Van'
    chat_luong_noi_bo_df['criteria'] = 'Chất lượng nội bộ'
    chat_luong_noi_bo_df['criteria_weight'] = TRONG_SO['Chất lượng nội bộ']['Tiêu chí']

    return chat_luong_noi_bo_df[['receiver_province', 'receiver_district', 'carrier', 'status', 'score', 'criteria', 'criteria_weight']]
