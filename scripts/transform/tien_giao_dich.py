from scripts.utilities.helper import *
from scripts.utilities.config import *


def transform_data_tien_giao_dich():
    # 1. Thông tin giao dịch
    giao_dich_valid = pd.read_parquet('./processed_data/giao_dich_combine_valid.parquet')
    giao_dich_valid = giao_dich_valid[giao_dich_valid['order_status'].isin([
        'Giao hàng thành công',
        'Đã hoàn thành',
        'Delivered | Giao hàng thành công',
        'Đã giao hàng/Chưa đối soát'
    ])]

    cuoc_phi_giao_dich = giao_dich_valid[[
        'order_id', 'receiver_province', 'receiver_district', 'carrier',
        'weight', 'delivery_type', 'order_type', 'order_type_id', 'sys_order_type_id',
    ]]

    # 2. Cước phí nhà vận chuyển
    cuoc_phi_df = pd.read_parquet('./processed_data/cuoc_phi.parquet')
    cuoc_phi_df = cuoc_phi_df[['carrier', 'order_type', 'gt', 'lt_or_eq', 'service_fee']]

    # 3. Tổng hợp
    cuoc_phi_giao_dich_full = cuoc_phi_giao_dich.merge(cuoc_phi_df, on=['carrier', 'order_type'], how='inner')
    cuoc_phi_giao_dich_full = cuoc_phi_giao_dich_full.loc[
        (cuoc_phi_giao_dich_full['weight'] > cuoc_phi_giao_dich_full['gt']) &
        (cuoc_phi_giao_dich_full['weight'] <= cuoc_phi_giao_dich_full['lt_or_eq'])
        ]

    # Ninja Van lấy tận nơi cộng cước phí 1,500
    cuoc_phi_giao_dich_full.loc[
        cuoc_phi_giao_dich_full['carrier'].isin(['Ninja Van']) &
        cuoc_phi_giao_dich_full['delivery_type'].isin(['Lấy Tận Nơi']),
        'service_fee'
    ] = cuoc_phi_giao_dich_full['service_fee'] + 1500

    # GHN lấy tận nơi cộng cước phí 1,000
    cuoc_phi_giao_dich_full.loc[
        cuoc_phi_giao_dich_full['carrier'].isin(['GHN']) &
        cuoc_phi_giao_dich_full['delivery_type'].isin(['Lấy Tận Nơi']),
        'service_fee'
    ] = cuoc_phi_giao_dich_full['service_fee'] + 1000

    return cuoc_phi_giao_dich_full
