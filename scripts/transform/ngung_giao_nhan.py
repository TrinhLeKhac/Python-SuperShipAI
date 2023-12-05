from scripts.utilities.helper import *
from scripts.utilities.config import *


def transform_data_ngung_giao_nhan():

    # Đọc data ngưng giao nhận
    ngung_giao_nhan_df = pd.read_parquet(ROOT_PATH + '/processed_data/ngung_giao_nhan.parquet')

    # Chọn lấy cột cần thiết và đổi tên cột
    ngung_giao_nhan_df['status'] = ngung_giao_nhan_df['status'].fillna('Bình thường')
    ngung_giao_nhan_df['status'] = ngung_giao_nhan_df['status'].apply(
        lambda s: unidecode(' '.join(s.split()).strip().lower()))
    ngung_giao_nhan_df.loc[ngung_giao_nhan_df['status'].isin(['chuyen ngoai', 'cham tuyen']), 'status'] = 'Quá tải'
    ngung_giao_nhan_df.loc[ngung_giao_nhan_df['status'] != 'Quá tải', 'status'] = 'Bình thường'

    ngung_giao_nhan_df = (
        PROVINCE_MAPPING_DISTRICT_CROSS_CARRIER_DF.merge(
            ngung_giao_nhan_df, on=['receiver_province', 'receiver_district', 'carrier'], how='left'
        )
    )
    ngung_giao_nhan_df['status'] = ngung_giao_nhan_df['status'].fillna('Bình thường')
    ngung_giao_nhan_df['score'] = ngung_giao_nhan_df['status'].map(TRONG_SO['Ngưng giao nhận']['Phân loại'])
    ngung_giao_nhan_df['criteria'] = 'Ngưng giao nhận'
    ngung_giao_nhan_df['criteria_weight'] = TRONG_SO['Ngưng giao nhận']['Tiêu chí']

    return ngung_giao_nhan_df[['receiver_province', 'receiver_district', 'carrier', 'status', 'score', 'criteria', 'criteria_weight']]
