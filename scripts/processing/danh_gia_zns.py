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
        'Đánh Giá Lúc',
    ]]
    danh_gia_zns_df.columns = [
        'receiver_province', 'receiver_district', 'nvc',
        'n_messages' , 'n_stars', 'comment', 'time'
    ]

    # 2. Chuẩn hóa tên quận/huyện, tỉnh/thành
    danh_gia_zns_df = normalize_province_district(danh_gia_zns_df, tinh_thanh='receiver_province',
                                               quan_huyen='receiver_district')

    # 3. Check tên nhà vận chuyển đã được chuẩn hóa chưa
    danh_gia_zns_df = danh_gia_zns_df.loc[danh_gia_zns_df['nvc'] != 'SuperShip']
    danh_gia_zns_df.loc[danh_gia_zns_df['nvc'] == 'Shopee Express', 'nvc'] = 'SPX Express'

    set_nvc = set(danh_gia_zns_df['nvc'].unique().tolist())
    set_norm_full_nvc = set(MAPPING_NVC_ID.keys())
    assert set_nvc - set_norm_full_nvc == set(), 'Ops, Tên nhà vận chuyển chưa được chuẩn hóa'

    # 4. Lưu thông tin
    danh_gia_zns_df.to_parquet('./processed_data/danh_gia_zns.parquet', index=False)
