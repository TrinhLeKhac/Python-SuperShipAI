from scripts.utilities.helper import *


def get_pct_ninja_van(s):
    if '<=' in s:
        return int(s.split('<=')[1].split('%')[0]) / 100
    elif '-' in s:
        first = int(s.split('-')[0].strip().split('%')[0])
        second = int(s.split('-')[1].strip().split('%')[0])
        return (first + second) / 2.0 / 100
    else:
        return 0


def xu_ly_chat_luong_noi_bo():

    # 1. Đọc data raw
    clnb_njv_df = pd.read_excel('./input/Chất Lượng Nội Bộ NJV.xlsx')
    clnb_njv_df = clnb_njv_df[1:]
    clnb_njv_df.columns = [
        'region', 'receiver_province', 'id_receiver_district', 'receiver_district',
        'short_receiver_district', 'buu_cuc', 'pct_success', 'is_more_than_100'
    ]
    clnb_njv_df = clnb_njv_df[['receiver_province', 'receiver_district', 'buu_cuc', 'pct_success', 'is_more_than_100']]

    # 2. Xử lý data
    clnb_njv_df.loc[clnb_njv_df['is_more_than_100'].isna(), 'is_more_than_100'] = False
    clnb_njv_df['is_more_than_100'] = clnb_njv_df['is_more_than_100'].astype(bool)

    # 3. Tách percentage
    clnb_njv_df['pct_success'] = clnb_njv_df['pct_success'].astype(str).apply(get_pct_ninja_van)

    # 4. Chuẩn hóa tên quận/huyện, tỉnh/thành
    clnb_njv_df = normalize_province_district(clnb_njv_df, tinh_thanh='receiver_province', quan_huyen='receiver_district')
    clnb_njv_df = clnb_njv_df.loc[clnb_njv_df['receiver_province'].notna() & clnb_njv_df['receiver_district'].notna()]

    # 5. Lưu thông tin
    clnb_njv_df.to_parquet('./processed_data/chat_luong_noi_bo_njv.parquet', index=False)