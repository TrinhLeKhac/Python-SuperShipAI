from scripts.utilities.helper import *

OLD_DATA_COLS = [
    'Tạo Lúc', 'Mã Đơn Hàng', 'Nhà Vận Chuyển', 'Trạng Thái Vận Đơn',
    'Tỉnh/Thành Phố Giao', 'Quận/Huyện Giao', 'Số Lần Giao',
    'Hình Thức Gửi Hàng', 'Có Hàng Đổi Trả', 'Giao lúc',
]

NEW_DATA_COLS = [
    'carrier_created_at', 'order_id', 'carrier', 'order_status',
    'receiver_province', 'receiver_district', 'n_deliveries',
    'delivery_type', 'is_returned', 'finished_at',
]


def convert_datetime_type1(s):
    try:
        result = datetime.strptime(s, "%Y-%d-%m %H:%M:%S")
    except ValueError:
        result = None
    return result


def convert_datetime_type2(s):
    try:
        result = datetime.strptime(s, "%Y-%d-%m %H:%M:%S")
    except ValueError:
        try:
            result = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            result = None
    return result


def type_of_delivery(s):
    if ((s['sender_outer_region'] == 'Miền Bắc') & (s['receiver_outer_region'] == 'Miền Nam')) \
            | ((s['sender_outer_region'] == 'Miền Nam') & (s['receiver_outer_region'] == 'Miền Bắc')):
        return 'Cách Miền'
    elif ((s['sender_outer_region'] == 'Miền Bắc') & (s['receiver_outer_region'] == 'Miền Trung')) \
            | ((s['sender_outer_region'] == 'Miền Trung') & (s['receiver_outer_region'] == 'Miền Nam')) \
            | ((s['sender_outer_region'] == 'Miền Trung') & (s['receiver_outer_region'] == 'Miền Bắc')) \
            | ((s['sender_outer_region'] == 'Miền Nam') & (s['receiver_outer_region'] == 'Miền Trung')):
        return 'Cận Miền'
    elif s['sender_province'] != s['receiver_province']:
        return 'Nội Miền'
    elif (s['receiver_inner_region'] == 'Nội Thành') \
            & (s['receiver_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Nội Thành Tp.HCM - HN'
    elif (s['receiver_inner_region'] == 'Nội Thành') \
            & (s['receiver_province'] not in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Nội Thành Tỉnh'
    elif (s['receiver_inner_region'] == 'Ngoại Thành') \
            & (s['receiver_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Ngoại Thành Tp.HCM - HN'
    elif (s['receiver_inner_region'] == 'Ngoại Thành') \
            & (s['receiver_province'] not in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']):
        return 'Ngoại Thành Tỉnh'


def type_of_system_delivery(s):
    if (s['sender_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Hà Nội']) \
            & (s['sender_province'] == s['receiver_province']):
        return 1
    elif ((s['sender_province'] == 'Thành phố Hồ Chí Minh') & (
            s['receiver_province'] in ['Thành phố Hà Nội', 'Thành phố Đà Nẵng'])) \
            | ((s['sender_province'] == 'Thành phố Hà Nội') & (
            s['receiver_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Đà Nẵng'])) \
            | ((s['receiver_province'] == 'Thành phố Hồ Chí Minh') & (
            s['sender_province'] in ['Thành phố Hà Nội', 'Thành phố Đà Nẵng'])) \
            | ((s['receiver_province'] == 'Thành phố Hà Nội') & (
            s['sender_province'] in ['Thành phố Hồ Chí Minh', 'Thành phố Đà Nẵng'])):
        return 2
    elif ((s['sender_province'] == 'Thành phố Hồ Chí Minh') & (s['receiver_outer_region'] == 'Miền Nam')) \
            | ((s['sender_province'] == 'Thành phố Hà Nội') & (s['receiver_outer_region'] == 'Miền Bắc')) \
            | ((s['receiver_province'] == 'Thành phố Hồ Chí Minh') & (s['sender_outer_region'] == 'Miền Nam')) \
            | ((s['receiver_province'] == 'Thành phố Hà Nội') & (s['sender_outer_region'] == 'Miền Bắc')):
        return 3
    elif ((s['sender_province'] == 'Thành phố Hồ Chí Minh') & (s['receiver_outer_region'] in ['Miền Bắc', 'Miền Trung'])) \
            | ((s['sender_province'] == 'Thành phố Hà Nội') & (s['receiver_outer_region'] in ['Miền Trung', 'Miền Nam'])) \
            | ((s['receiver_province'] == 'Thành phố Hồ Chí Minh') & (s['sender_outer_region'] in ['Miền Bắc', 'Miền Trung'])) \
            | ((s['receiver_province'] == 'Thành phố Hà Nội') & (s['sender_outer_region'] in ['Miền Trung', 'Miền Nam'])):
        return 4
    elif s['sender_province'] == s['receiver_province']:
        return 5
    elif s['sender_outer_region'] == s['receiver_outer_region']:
        return 6
    elif ((s['sender_outer_region'] == 'Miền Bắc') & (s['receiver_outer_region'] in ['Miền Trung', 'Miền Nam'])) \
        | ((s['sender_outer_region'] == 'Miền Trung') & (s['receiver_outer_region'] in ['Miền Bắc', 'Miền Nam'])) \
        | ((s['sender_outer_region'] == 'Miền Nam') & (s['receiver_outer_region'] in ['Miền Bắc', 'Miền Trung'])) \
        | ((s['receiver_outer_region'] == 'Miền Bắc') & (s['sender_outer_region'] in ['Miền Trung', 'Miền Nam'])) \
        | ((s['receiver_outer_region'] == 'Miền Trung') & (s['sender_outer_region'] in ['Miền Bắc', 'Miền Nam'])) \
        | ((s['receiver_outer_region'] == 'Miền Nam') & (s['sender_outer_region'] in ['Miền Bắc', 'Miền Trung'])):
        return 7


def xu_ly_giao_dich():
    print('Xử lý giao dịch BEST Express...')
    best_df = pd.read_excel('./input/Giao Dịch Nhà Vận Chuyển.xlsx', sheet_name='BEST')
    best_df = best_df[OLD_DATA_COLS]
    best_df.columns = NEW_DATA_COLS
    best_df['carrier'] = 'BEST Express'

    best_df.loc[best_df['is_returned'] == '✅', 'is_returned'] = True
    best_df['is_returned'] = best_df['is_returned'].fillna(False)
    best_df['carrier_created_at'] = pd.to_datetime(best_df['carrier_created_at'], errors='coerce')
    best_df['finished_at'] = pd.to_datetime(best_df['finished_at'], errors='coerce')

    best_df['finished_at'] = best_df['finished_at'].apply(lambda x: str(x)).apply(convert_datetime_type1)
    best_df['carrier_created_at'] = best_df['carrier_created_at'].apply(lambda x: str(x)).apply(convert_datetime_type2)

    print('Xử lý giao dịch Ninja Van...')
    njv_df = pd.read_excel('./input/Giao Dịch Nhà Vận Chuyển.xlsx', sheet_name='NJV')
    njv_df = njv_df[OLD_DATA_COLS]
    njv_df.columns = NEW_DATA_COLS
    njv_df['carrier'] = 'Ninja Van'

    njv_df.loc[njv_df['is_returned'] == '✅', 'is_returned'] = True
    njv_df['is_returned'] = njv_df['is_returned'].fillna(False)

    njv_df['carrier_created_at'] = pd.to_datetime(njv_df['carrier_created_at'], errors='coerce')
    njv_df['finished_at'] = pd.to_datetime(njv_df['finished_at'], errors='coerce')

    njv_df['finished_at'] = njv_df['finished_at'].apply(lambda x: str(x)).apply(convert_datetime_type1)

    print('Xử lý giao dịch GHN...')
    ghn_df = pd.read_excel('./input/Giao Dịch Nhà Vận Chuyển.xlsx', sheet_name='GHN')
    ghn_df = ghn_df[OLD_DATA_COLS]
    ghn_df.columns = NEW_DATA_COLS
    ghn_df['carrier'] = 'GHN'

    ghn_df.loc[ghn_df['is_returned'] == '✅', 'is_returned'] = True
    ghn_df['is_returned'] = ghn_df['is_returned'].fillna(False)

    ghn_df['carrier_created_at'] = pd.to_datetime(ghn_df['carrier_created_at'], errors='coerce')
    ghn_df['finished_at'] = pd.to_datetime(ghn_df['finished_at'], errors='coerce')

    ghn_df['finished_at'] = ghn_df['finished_at'].apply(lambda x: str(x)).apply(convert_datetime_type1)

    print('Xử lý giao dịch Viettel Post...')
    vtp_df = pd.read_excel('./input/Giao Dịch Nhà Vận Chuyển.xlsx', sheet_name='VTP')
    vtp_df = vtp_df[OLD_DATA_COLS]
    vtp_df.columns = NEW_DATA_COLS
    vtp_df['carrier'] = 'Viettel Post'

    vtp_df.loc[vtp_df['is_returned'] == '✅', 'is_returned'] = True
    vtp_df['is_returned'] = vtp_df['is_returned'].fillna(False)

    vtp_df['carrier_created_at'] = pd.to_datetime(vtp_df['carrier_created_at'], errors='coerce')
    vtp_df['finished_at'] = pd.to_datetime(vtp_df['finished_at'], errors='coerce')

    vtp_df['finished_at'] = vtp_df['finished_at'].apply(lambda x: str(x)).apply(convert_datetime_type1)

    print('Xử lý giao dịch SPX Express...')
    spx_df = pd.read_excel('./input/Giao Dịch Nhà Vận Chuyển.xlsx', sheet_name='SPX')
    spx_df = spx_df[OLD_DATA_COLS]
    spx_df.columns = NEW_DATA_COLS
    spx_df['carrier'] = 'SPX Express'

    spx_df.loc[spx_df['is_returned'] == '✅', 'is_returned'] = True
    spx_df['is_returned'] = spx_df['is_returned'].fillna(False)

    spx_df['carrier_created_at'] = pd.to_datetime(spx_df['carrier_created_at'], errors='coerce')
    spx_df['finished_at'] = pd.to_datetime(spx_df['finished_at'], errors='coerce')

    spx_df['finished_at'] = spx_df['finished_at'].apply(lambda x: str(x)).apply(convert_datetime_type1)

    print('Xử lý giao dịch GHTK...')
    ghtk_df = pd.read_excel('./input/Giao Dịch Nhà Vận Chuyển.xlsx', sheet_name='GHTK')
    ghtk_df = ghtk_df[OLD_DATA_COLS]
    ghtk_df.columns = NEW_DATA_COLS
    ghtk_df['carrier'] = 'GHTK'

    ghtk_df.loc[ghtk_df['is_returned'] == '✅', 'is_returned'] = True
    ghtk_df['is_returned'] = ghtk_df['is_returned'].fillna(False)

    ghtk_df['carrier_created_at'] = pd.to_datetime(ghtk_df['carrier_created_at'], errors='coerce')
    ghtk_df['finished_at'] = pd.to_datetime(ghtk_df['finished_at'], errors='coerce')

    ghtk_df['finished_at'] = ghtk_df['finished_at'].apply(lambda x: str(x)).apply(convert_datetime_type1)

    print('Tổng hợp giao dịch...')
    giao_dich_df = pd.concat([best_df, njv_df, ghn_df, vtp_df, spx_df, ghtk_df], ignore_index=True)

    print('Lưu thông tin...')
    giao_dich_df.to_parquet('./processed_data/giao_dich_tong.parquet', index=False)


def xu_ly_giao_dich_co_khoi_luong():
    giao_dich_co_khoi_luong_df = pd.read_excel('./input/Đơn Có Khối Lượng.xlsx', sheet_name='Combined')

    giao_dich_co_khoi_luong_df = giao_dich_co_khoi_luong_df[['Mã Đơn SuperShip', 'Khối Lượng', 'Kho Hàng']]
    giao_dich_co_khoi_luong_df.columns = ['order_id', 'weight', 'storage_address']

    print('Lưu thông tin...')
    giao_dich_co_khoi_luong_df.to_parquet('./processed_data/giao_dich_co_khoi_luong.parquet', index=False)


def tong_hop_thong_tin_giao_dich():
    print('Đọc thông tin giao dịch và giao dịch có khối lượng...')
    giao_dich_tong_df = pd.read_parquet('./processed_data/giao_dich_tong.parquet')
    giao_dich_co_khoi_luong_df = pd.read_parquet('./processed_data/giao_dich_co_khoi_luong.parquet')

    print('Combine thông tin giao dịch')
    giao_dich_valid_df = giao_dich_tong_df.merge(giao_dich_co_khoi_luong_df, on='order_id', how='inner')
    print('Số giao dịch hợp lệ: ', len(giao_dich_valid_df))

    print('Tách địa chỉ tỉnh/thành, quận/huyện lấy hàng từ kho nhận')
    giao_dich_valid_df['sender_province'] = giao_dich_valid_df['storage_address'].str.split(', ').str[-1]
    giao_dich_valid_df['sender_district'] = giao_dich_valid_df['storage_address'].str.split(', ').str[-2]

    print('Chuẩn hóa thông tin tỉnh/thành, quận/huyện lấy hàng...')
    giao_dich_valid = normalize_province_district(giao_dich_valid_df, tinh_thanh='sender_province',
                                                  quan_huyen='sender_district')

    print('Chuẩn hóa thông tin tỉnh/thành, quận/huyện giao hàng...')
    giao_dich_valid = normalize_province_district(giao_dich_valid, tinh_thanh='receiver_province',
                                                  quan_huyen='receiver_district')

    giao_dich_valid = giao_dich_valid[
        giao_dich_valid['sender_province'].notna()
        & giao_dich_valid['sender_district'].notna()
        & giao_dich_valid['receiver_province'].notna()
        & giao_dich_valid['receiver_district'].notna()
        ]
    print('Số giao dịch sau khi chuẩn hóa tỉnh/thành, quận/huyện: ', len(giao_dich_valid))

    print('Tính toán loại vận chuyển từ địa chỉ giao và nhận...')
    phan_vung_nvc = pd.read_parquet('./processed_data/phan_vung_nvc.parquet')
    giao_dich_valid = (
        giao_dich_valid.merge(
            phan_vung_nvc.rename(columns={
                'receiver_province': 'sender_province',
                'receiver_district': 'sender_district',
                'outer_region': 'sender_outer_region',
                'inner_region': 'sender_inner_region',
            }), on=['carrier', 'sender_province', 'sender_district'], how='left').merge(
            phan_vung_nvc.rename(columns={
                'outer_region': 'receiver_outer_region',
                'inner_region': 'receiver_inner_region',
            }), on=['carrier', 'receiver_province', 'receiver_district'], how='left')
    )
    giao_dich_valid['order_type'] = giao_dich_valid.apply(type_of_delivery, axis=1)
    giao_dich_valid['order_type_id'] = giao_dich_valid['order_type'].map(MAPPING_ORDER_TYPE_ID)
    giao_dich_valid['sys_order_type_id'] = giao_dich_valid.apply(type_of_system_delivery, axis=1)

    giao_dich_valid = giao_dich_valid[[
        'carrier_created_at', 'order_id', 'carrier', 'weight',
        'sender_province', 'sender_district',
        'receiver_province', 'receiver_district',
        'order_status', 'order_type', 'order_type_id', 'sys_order_type_id',
        'n_deliveries', 'delivery_type',
        'is_returned', 'finished_at',
    ]]

    set_carrier = set(giao_dich_valid['carrier'].unique().tolist())
    set_norm_full_carrier = set(MAPPING_CARRIER_ID.keys())
    assert set_carrier - set_norm_full_carrier == set(), 'Ops, Tên nhà vận chuyển chưa được chuẩn hóa'

    print('Lưu thông tin...')
    giao_dich_valid.to_parquet('./processed_data/giao_dich_combine_valid.parquet', index=False)
