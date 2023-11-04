from scripts.utilities.helper import *
from scripts.utilities.config import *


def transform_data_ngung_giao_nhan():

    # Đọc data ngưng giao nhận
    ngung_giao_nhan_df = pd.read_parquet('./processed_data/ngung_giao_nhan.parquet')

    # Chọn lấy cột cần thiết và đổi tên cột
    ngung_giao_nhan_df['status'] = ngung_giao_nhan_df['status'].fillna('Bình thường')
    ngung_giao_nhan_df['status'] = ngung_giao_nhan_df['status'].apply(
        lambda s: unidecode(' '.join(s.split()).strip().lower()))
    ngung_giao_nhan_df.loc[ngung_giao_nhan_df['status'].isin(['chuyen ngoai', 'cham tuyen']), 'status'] = 'Quá tải'
    ngung_giao_nhan_df.loc[ngung_giao_nhan_df['status'] != 'Quá tải', 'status'] = 'Bình thường'

    ngung_giao_nhan_df = (
        PROVINCE_MAPPING_DISTRICT_CROSS_NVC_DF.merge(
            ngung_giao_nhan_df, on=['receiver_province', 'receiver_district', 'nvc'], how='left'
        )
    )
    ngung_giao_nhan_df['status'] = ngung_giao_nhan_df['status'].fillna('Bình thường')
    ngung_giao_nhan_df['score'] = ngung_giao_nhan_df['status'].map(TRONG_SO['Ngưng giao nhận']['Phân loại'])
    ngung_giao_nhan_df['tieu_chi'] = 'Ngưng giao nhận'
    ngung_giao_nhan_df['trong_so'] = TRONG_SO['Ngưng giao nhận']['Tiêu chí']

    return ngung_giao_nhan_df[['receiver_province', 'receiver_district', 'nvc', 'status', 'score', 'tieu_chi', 'trong_so']]
