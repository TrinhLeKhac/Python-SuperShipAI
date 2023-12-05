import sys
from pathlib import Path

ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)

from scripts.utilities.helper import *
from scripts.utilities.config import *


def out_data_order_type(show_logs=True):
    if show_logs:
        print('1. Xử lý data phân vùng nhà vận chuyển...')
    phan_vung_nvc = pd.read_parquet(ROOT_PATH + '/processed_data/phan_vung_nvc.parquet')
    phan_vung_nvc = phan_vung_nvc[
        ['carrier_id', 'receiver_province_id', 'receiver_district_id', 'outer_region_id', 'inner_region_id']]

    if show_logs:
        print('2. Mapping 713 * 713 tỉnh thành, quận huyện gửi/nhận...')
    carrier_id_df = pd.DataFrame(data={'carrier_id': [MAPPING_CARRIER_ID[v] for v in ACTIVE_CARRIER]})

    sender_df = PROVINCE_MAPPING_DISTRICT_DF[['province_id', 'district_id']]
    sender_df.columns = ['sender_province_id', 'sender_district_id']

    receiver_df = PROVINCE_MAPPING_DISTRICT_DF[['province_id', 'district_id']]
    receiver_df.columns = ['receiver_province_id', 'receiver_district_id']

    input_df = carrier_id_df.merge(sender_df, how='cross').merge(receiver_df, how='cross')
    input_df = (
        input_df.merge(
            phan_vung_nvc.rename(columns={
                'receiver_province_id': 'sender_province_id',
                'receiver_district_id': 'sender_district_id',
                'outer_region_id': 'sender_outer_region_id',
                'inner_region_id': 'sender_inner_region_id',
            }), on=['carrier_id', 'sender_province_id', 'sender_district_id'], how='left')
            .merge(
            phan_vung_nvc.rename(columns={
                'outer_region_id': 'receiver_outer_region_id',
                'inner_region_id': 'receiver_inner_region_id',
            }), on=['carrier_id', 'receiver_province_id', 'receiver_district_id'], how='left')
    )
    if show_logs:
        print('3. Mapping order_type...')

    input_df['order_type_id'] = -1
    input_df.loc[
        (((input_df['sender_province_id'] == '79') & (
            input_df['receiver_province_id'].isin(['01', '48']))) | ((input_df['sender_province_id'] == '01') & (
            input_df['receiver_province_id'].isin(['79', '48']))) | ((input_df['receiver_province_id'] == '79') & (
            input_df['sender_province_id'].isin(['01', '48']))) | ((input_df['receiver_province_id'] == '01') & (
            input_df['sender_province_id'].isin(['79', '48']))))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 10

    input_df.loc[
        (((input_df['sender_province_id'] == '79') & (
            input_df['receiver_outer_region_id'].isin([0, 1])))
         | (
                 (input_df['sender_province_id'] == '01') & (input_df['receiver_outer_region_id'].isin([1, 2])))
         | ((input_df['receiver_province_id'] == '79') & (
                    input_df['sender_outer_region_id'].isin([0, 1])))
         | (
                 (input_df['receiver_province_id'] == '01') & (input_df['sender_outer_region_id'].isin([1, 2]))))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 9

    input_df.loc[
        (((input_df['sender_outer_region_id'] == 0) & (input_df['receiver_outer_region_id'] == 2))
         | ((input_df['sender_outer_region_id'] == 2) & (input_df['receiver_outer_region_id'] == 0)))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 7

    input_df.loc[
        (((input_df['sender_outer_region_id'] == 0) & (input_df['receiver_outer_region_id'] == 1))
         | ((input_df['sender_outer_region_id'] == 1) & (input_df['receiver_outer_region_id'] == 2))
         | ((input_df['sender_outer_region_id'] == 1) & (input_df['receiver_outer_region_id'] == 0))
         | ((input_df['sender_outer_region_id'] == 2) & (input_df['receiver_outer_region_id'] == 1)))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 6

    input_df.loc[
        (input_df['sender_province_id'] != input_df['receiver_province_id'])
        & (input_df['sender_province_id'].isin(['01', '79'])
           | input_df['receiver_province_id'].isin(['01', '79']))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 8

    input_df.loc[
        (input_df['sender_province_id'] != input_df['receiver_province_id'])
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 5

    input_df.loc[
        (input_df['receiver_inner_region_id'] == 0) \
        & (input_df['receiver_province_id'].isin(['79', '01']))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 3

    input_df.loc[
        (input_df['receiver_inner_region_id'] == 0) \
        & (~input_df['receiver_province_id'].isin(['79', '01']))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 1

    input_df.loc[
        (input_df['receiver_inner_region_id'] == 1) \
        & (input_df['receiver_province_id'].isin(['79', '01']))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 4

    input_df.loc[
        (input_df['receiver_inner_region_id'] == 1) \
        & (~input_df['receiver_province_id'].isin(['79', '01']))
        & (input_df['order_type_id'] == -1),
        'order_type_id'
    ] = 2

    if show_logs:
        print('4. Mapping system_order_type...')
    # input_df['sys_order_type_id'] = -1
    # input_df.loc[
    #     (input_df['sender_province_id'].isin(['79', '01'])) \
    #     & (input_df['sender_province_id'] == input_df['receiver_province_id'])
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 1
    # input_df.loc[
    #     (((input_df['sender_province_id'] == '79') & (
    #         input_df['receiver_province_id'].isin(['01', '48'])))
    #      | ((input_df['sender_province_id'] == '01') & (
    #                 input_df['receiver_province_id'].isin(['79', '48'])))
    #      | ((input_df['receiver_province_id'] == '79') & (
    #                 input_df['sender_province_id'].isin(['01', '48'])))
    #      | ((input_df['receiver_province_id'] == '01') & (
    #                 input_df['sender_province_id'].isin(['79', '48']))))
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 2
    # input_df.loc[
    #     (((input_df['sender_province_id'] == '79') & (input_df['receiver_outer_region_id'] == 2)) | ((input_df['sender_province_id'] == '01') & (input_df['receiver_outer_region_id'] == 0)) | ((input_df['receiver_province_id'] == '79') & (input_df['sender_outer_region_id'] == 2)) | ((input_df['receiver_province_id'] == '01') & (input_df['sender_outer_region_id'] == 0)))
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 3
    # input_df.loc[
    #     (((input_df['sender_province_id'] == '79') & (
    #         input_df['receiver_outer_region_id'].isin([0, 1])))
    #      | (
    #              (input_df['sender_province_id'] == '01') & (input_df['receiver_outer_region_id'].isin([1, 2])))
    #      | ((input_df['receiver_province_id'] == '79') & (
    #                 input_df['sender_outer_region_id'].isin([0, 1])))
    #      | (
    #              (input_df['receiver_province_id'] == '01') & (input_df['sender_outer_region_id'].isin([1, 2]))))
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 4
    # input_df.loc[
    #     (input_df['sender_province_id'] == input_df['receiver_province_id'])
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 5
    # input_df.loc[
    #     (input_df['sender_outer_region_id'] == input_df['receiver_outer_region_id'])
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 6
    # input_df.loc[
    #     (((input_df['sender_outer_region_id'] == 0) & (input_df['receiver_outer_region_id'].isin([1, 2])))
    #      | ((input_df['sender_outer_region_id'] == 1) & (input_df['receiver_outer_region_id'].isin([0, 2])))
    #      | ((input_df['sender_outer_region_id'] == 2) & (input_df['receiver_outer_region_id'].isin([0, 1])))
    #      | ((input_df['receiver_outer_region_id'] == 0) & (input_df['sender_outer_region_id'].isin([1, 2])))
    #      | ((input_df['receiver_outer_region_id'] == 1) & (input_df['sender_outer_region_id'].isin([0, 2])))
    #      | ((input_df['receiver_outer_region_id'] == 2) & (input_df['sender_outer_region_id'].isin([0, 1]))))
    #     & (input_df['sys_order_type_id'] == -1),
    #     'sys_order_type_id'
    # ] = 7
    input_df['sys_order_type_id'] = input_df['order_type_id'].map(MAPPING_ORDER_TYPE_ID_ROUTE_TYPE)
    if show_logs:
        print('5. Transform data final...')
    input_df = input_df.rename(columns={'order_type_id': 'new_type', 'sys_order_type_id': 'route_type'})
    input_df = input_df.reset_index().rename(columns={"index": "id"})
    input_df['new_type'] = input_df['new_type'].astype(str)
    input_df['route_type'] = input_df['route_type'].astype(str)
    order_type_df = input_df[[
        'id', 'carrier_id', 'sender_province_id', 'sender_district_id',
        'receiver_province_id', 'receiver_district_id',
        'new_type', 'route_type']]
    order_type_df.columns = ['id', 'carrier_id', 'sender_province_code', 'sender_district_code',
                             'receiver_province_code', 'receiver_district_code', 'new_type', 'route_type']
    if show_logs:
        print('6. Saving data...')
    order_type_df.to_parquet(ROOT_PATH + "/output/data_order_type.parquet", index=False)


def out_data_service_fee(show_logs=True):
    print('Xử lý data service_fee...')
    cuoc_phi_df = pd.read_parquet(ROOT_PATH + '/processed_data/cuoc_phi.parquet')
    cuoc_phi_df['order_type_id'] = cuoc_phi_df['order_type'].map(MAPPING_ORDER_TYPE_ID)

    cuoc_phi_df = cuoc_phi_df[['carrier_id', 'lt_or_eq', 'order_type_id', 'service_fee']].rename(
        columns={'lt_or_eq': 'weight', 'order_type_id': 'new_type', 'service_fee': 'price'})
    cuoc_phi_df['new_type'] = cuoc_phi_df['new_type'].astype(str)

    # Add fee lấy tận nơi, gửi bưu cục
    service_fee_df1 = cuoc_phi_df.copy()
    service_fee_df1['pickup'] = '0'

    service_fee_df2 = cuoc_phi_df.copy()
    service_fee_df2['pickup'] = '1'

    service_fee_df = pd.concat([service_fee_df1, service_fee_df2], ignore_index=True)
    service_fee_df.loc[(service_fee_df['pickup'] == '1') & (service_fee_df['carrier_id'] == 7), 'price'] = \
        service_fee_df['price'] + 1500
    service_fee_df.loc[(service_fee_df['pickup'] == '1') & (service_fee_df['carrier_id'] == 2), 'price'] = \
        service_fee_df['price'] + 1000

    service_fee_df = service_fee_df[['carrier_id', 'new_type', 'pickup', 'weight', 'price']]
    service_fee_df.to_parquet(ROOT_PATH + '/output/service_fee.parquet', index=False)


if __name__ == '__main__':
    out_data_order_type()
    out_data_service_fee()
