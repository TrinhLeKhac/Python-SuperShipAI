from scripts.utilities.helper import *
from scripts.utilities.config import *


def status_kho_giao_nhan(so_buu_cuc, so_buu_cuc_trong_tinh, so_quan_huyen):
    if so_buu_cuc == 0:
        if so_buu_cuc_trong_tinh == 0:
            return 'Không có bưu cục trong tỉnh'
        elif so_buu_cuc_trong_tinh / so_quan_huyen > 0.8:
            return 'Trong tỉnh có trên 80% bưu cục/tổng quận huyện của tỉnh'
        elif so_buu_cuc_trong_tinh / so_quan_huyen > 0.5:
            return 'Trong tỉnh có trên 50% bưu cục/tổng quận huyện của tỉnh'
        elif so_buu_cuc_trong_tinh / so_quan_huyen > 0.3:
            return 'Trong tỉnh có trên 30% bưu cục/tổng quận huyện của tỉnh'
        elif so_buu_cuc_trong_tinh / so_quan_huyen <= 0.3:
            return 'Trong tỉnh có bé hơn hoặc bằng 30% bưu cục/tổng quận huyện của tỉnh'
    if so_buu_cuc >= 3:
        return 'Có từ 3 bưu cục cùng cấp quận/huyện trở lên'
    elif so_buu_cuc == 2:
        return 'Có 2 bưu cục cùng cấp quận/huyện trở lên'
    elif so_buu_cuc == 1:
        return 'Có bưu cục cùng cấp quận/huyện'


def transform_buu_cuc(buu_cuc_df, carrier='BEST Express'):

    buu_cuc_df = buu_cuc_df.merge(PROVINCE_MAPPING_DISTRICT_DF[['province', 'district']].rename(columns={
        'province': 'receiver_province',
        'district': 'receiver_district'
    }), on=['receiver_province', 'receiver_district'], how='right')
    buu_cuc_df['n_post_offices'] = buu_cuc_df['n_post_offices'].fillna(0).astype(int)

    buu_cuc_df['n_post_offices_in_province'] = (
        buu_cuc_df.groupby('receiver_province')['n_post_offices'].transform(np.sum)
    )
    buu_cuc_df['n_district'] = (
        buu_cuc_df.groupby('receiver_province')['receiver_district'].transform(pd.Series.nunique)
    )
    buu_cuc_df['status'] = buu_cuc_df.apply(
        lambda s: status_kho_giao_nhan(s['n_post_offices'], s['n_post_offices_in_province'], s['n_district']),
        axis=1)
    buu_cuc_df['score'] = buu_cuc_df['status'].map(TRONG_SO['Có kho giao nhận']['Phân loại'])
    buu_cuc_df['carrier'] = carrier
    buu_cuc_df['criteria'] = 'Có kho giao nhận'
    buu_cuc_df['criteria_weight'] = TRONG_SO['Có kho giao nhận']['Tiêu chí']

    return buu_cuc_df[['receiver_province', 'receiver_district', 'carrier', 'status', 'score', 'criteria', 'criteria_weight']]


def transform_data_kho_giao_nhan():

    # Đọc thông tin bưu cục
    buu_cuc_njv = pd.read_parquet('./processed_data/buu_cuc_ninja_van.parquet')
    buu_cuc_ghn = pd.read_parquet('./processed_data/buu_cuc_ghn.parquet')
    buu_cuc_best = pd.read_parquet('./processed_data/buu_cuc_best.parquet')
    buu_cuc_ghtk = pd.read_parquet('./processed_data/buu_cuc_ghtk.parquet')

    buu_cuc_njv = transform_buu_cuc(buu_cuc_njv, carrier='Ninja Van')
    buu_cuc_ghn = transform_buu_cuc(buu_cuc_ghn, carrier='GHN')
    buu_cuc_best = transform_buu_cuc(buu_cuc_best, carrier='BEST Express')
    buu_cuc_ghtk = transform_buu_cuc(buu_cuc_ghtk, carrier='GHTK')

    kho_giao_nhan = pd.concat([buu_cuc_njv, buu_cuc_ghn, buu_cuc_best, buu_cuc_ghtk], ignore_index=True)

    # Fill thông tin default
    kho_giao_nhan = (
        PROVINCE_MAPPING_DISTRICT_CROSS_CARRIER_DF.merge(
            kho_giao_nhan, on=['receiver_province', 'receiver_district', 'carrier'], how='left'
        )
    )
    kho_giao_nhan['status'] = kho_giao_nhan['status'].fillna('Không có thông tin')
    kho_giao_nhan['score'] = kho_giao_nhan['status'].map(TRONG_SO['Có kho giao nhận']['Phân loại'])
    kho_giao_nhan['criteria'] = 'Có kho giao nhận'
    kho_giao_nhan['criteria_weight'] = TRONG_SO['Có kho giao nhận']['Tiêu chí']

    # Kiểm tra data kho giao nhan
    assert kho_giao_nhan.isna().sum().all() == 0, 'Transform data có vấn đề'

    return kho_giao_nhan[['receiver_province', 'receiver_district', 'carrier', 'status', 'score', 'criteria', 'criteria_weight']]
