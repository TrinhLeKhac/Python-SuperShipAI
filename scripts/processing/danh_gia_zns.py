from scripts.utilities.helper import *


def xu_ly_danh_gia_zns():
    # 1. Đọc dữ liệu
    danh_gia_zns_df = pd.read_excel('./input/Đánh Giá ZNS.xlsx')
    danh_gia_zns_df = danh_gia_zns_df[[
        'Tỉnh/Thành Phố Giao Hàng',
        'Quận/Huyện Giao Hàng',
        'Nhà Vận Chuyển',
        'Số Tin Gửi',
        'Số Sao',
        'Nhận Xét',
        'Đánh Giá',
        'Đánh Giá Lúc',
    ]]
    danh_gia_zns_df.columns = [
        'receiver_province', 'receiver_district', 'carrier',
        'n_messages', 'n_stars', 'comment', 'review', 'reviewed_at',
    ]

    # 2. Chuẩn hóa tên quận/huyện, tỉnh/thành
    danh_gia_zns_df = normalize_province_district(danh_gia_zns_df, tinh_thanh='receiver_province',
                                                  quan_huyen='receiver_district')

    # 3. Check tên nhà vận chuyển đã được chuẩn hóa chưa
    danh_gia_zns_df = danh_gia_zns_df.loc[danh_gia_zns_df['carrier'] != 'SuperShip']
    danh_gia_zns_df.loc[danh_gia_zns_df['carrier'] == 'Shopee Express', 'carrier'] = 'SPX Express'

    danh_gia_zns_df['reviewed_at'] = pd.to_datetime(danh_gia_zns_df['reviewed_at'], errors='coerce')

    set_carrier = set(danh_gia_zns_df['carrier'].unique().tolist())
    set_norm_full_carrier = set(MAPPING_CARRIER_ID.keys())
    assert set_carrier - set_norm_full_carrier == set(), 'Ops, Tên nhà vận chuyển chưa được chuẩn hóa'

    # 4. Lưu thông tin
    danh_gia_zns_df.to_parquet('./processed_data/danh_gia_zns.parquet', index=False)
