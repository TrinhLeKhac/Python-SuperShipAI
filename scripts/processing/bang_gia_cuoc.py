from scripts.utilities.helper import *

COLUMNS_CUOC_PHI = [
    'gt', 'lt_or_eq',
    'Nội Thành Tỉnh', 'Ngoại Thành Tỉnh',
    'Nội Thành Tp.HCM - HN', 'Ngoại Thành Tp.HCM - HN',
    'Nội Miền', 'Cận Miền', 'Cách Miền',
]


def xu_ly_bang_gia_cuoc():
    # 1. Lấy thông tin bảng giá cước
    bang_gia_cuoc_df = pd.read_excel(ROOT_PATH + '/input/Bảng Cước Phí.xlsx')

    # 2.1 Tách lấy thông tin bảng giá cước Ninja Van và xử lý
    ninja_van_df = pd.concat([bang_gia_cuoc_df.iloc[1:21, :2], bang_gia_cuoc_df.iloc[1:21, 2:9]], axis=1).reset_index(
        drop=True)
    ninja_van_df.columns = COLUMNS_CUOC_PHI
    for i in range(80):
        ninja_van_df.loc[20 + i, :] = [10000 + 500 * i, 10500 + 500 * i, 70 + 9 * int(i / 2), 70 + 9 * int(i / 2),
                                       70 + 9 * int(i / 2), 70 + 9 * int(i / 2), 82 + 11 * int(i / 2),
                                       124 + 16 * int(i / 2), 124 + 16 * int(i / 2)]
    ninja_van_df['carrier'] = 'Ninja Van'
    ninja_van_df['carrier_id'] = 7

    # 2.2 Tách lấy thông tin bảng giá cước BEST Express và xử lý
    best_df = pd.concat([bang_gia_cuoc_df.iloc[1:21, :2], bang_gia_cuoc_df.iloc[1:21, 9:16]], axis=1).reset_index(
        drop=True)
    best_df.columns = COLUMNS_CUOC_PHI
    for i in range(80):
        best_df.loc[20 + i, :] = [10000 + 500 * i, 10500 + 500 * i, 38 + 2 * i, 38 + 2 * i, 38 + 2 * i, 38 + 2 * i,
                                  38 + 2 * i, 38 + 2 * i, 38 + 2 * i]
    best_df['carrier'] = 'BEST Express'
    best_df['carrier_id'] = 6

    # 2.3 Tách lấy thông tin bảng giá cước SPX Express và xử lý
    shopee_express_df = pd.concat([bang_gia_cuoc_df.iloc[1:21, :2], bang_gia_cuoc_df.iloc[1:21, 16:23]],
                                  axis=1).reset_index(drop=True)
    shopee_express_df.columns = COLUMNS_CUOC_PHI
    for i in range(80):
        shopee_express_df.loc[20 + i, :] = [10000 + 500 * i, 10500 + 500 * i, 58.5 + 2.5 * i, 58.5 + 2.5 * i, 58.5 + 2.5 * i,
                                            58.5 + 2.5 * i, 58.5 + 2.5 * i, 103 + 5 * i, 103 + 5 * i]
    shopee_express_df['carrier'] = 'SPX Express'
    shopee_express_df['carrier_id'] = 10

    # 2.4 Tách lấy thông tin bảng giá cước GHN và xử lý
    ghn_df = pd.concat([bang_gia_cuoc_df.iloc[1:21, :2], bang_gia_cuoc_df.iloc[1:21, 23:30]], axis=1).reset_index(
        drop=True)
    ghn_df.columns = COLUMNS_CUOC_PHI
    for i in range(80):
        ghn_df.loc[20 + i, :] = [10000 + 500 * i, 10500 + 500 * i, 54 + 5 * int(i / 2), 54 + 5 * int(i / 2),
                                 54 + 5 * int(i / 2), 54 + 5 * int(i / 2), 54 + 5 * int(i / 2), 54 + 5 * int(i / 2),
                                 54 + 5 * int(i / 2)]
    ghn_df['carrier'] = 'GHN'
    ghn_df['carrier_id'] = 2

    # 2.5 Tách lấy thông tin bảng giá cước Viettel Post và xử lý
    viettel_post_df = pd.concat([bang_gia_cuoc_df.iloc[1:21, :2], bang_gia_cuoc_df.iloc[1:21, 30:37]],
                                axis=1).reset_index(drop=True)
    viettel_post_df.columns = COLUMNS_CUOC_PHI
    for i in range(40):
        viettel_post_df.loc[20 + i, :] = [10000 + 500 * i, 10500 + 500 * i, 50 + 4 * int(i / 2), 50 + 4 * int(i / 2),
                                          50 + 4 * int(i / 2), 50 + 4 * int(i / 2), 63 + 5 * int(i / 2),
                                          63 + 5 * int(i / 2), 63 + 5 * int(i / 2)]
    for i in range(40):
        viettel_post_df.loc[60 + i, :] = [30000 + 500 * i, 30500 + 500 * i, 120 + 4 * int(i / 2), 120 + 4 * int(i / 2),
                                          120 + 4 * int(i / 2), 120 + 4 * int(i / 2), 150 + 5.5 * int(i / 2),
                                          150 + 5.5 * int(i / 2), 150 + 5.5 * int(i / 2)]
    viettel_post_df['carrier'] = 'Viettel Post'
    viettel_post_df['carrier_id'] = 4

    # 2.6 Tách lấy thông tin bảng giá cước GHTK và xử lý
    ghtk_df = pd.concat([bang_gia_cuoc_df.iloc[1:21, :2], bang_gia_cuoc_df.iloc[1:21, 37:44]], axis=1).reset_index(
        drop=True)
    ghtk_df.columns = COLUMNS_CUOC_PHI
    for i in range(80):
        ghtk_df.loc[20 + i, :] = [10000 + 500 * i, 10500 + 500 * i, 85 + 2.5 * i, 85 + 2.5 * i, 59.5 + 2.5 * i,
                                  67.5 + 2.5 * i, 85 + 2.5 * i, 127.5 + 2.5 * i, 127.5 + 2.5 * i]
    ghtk_df['carrier'] = 'GHTK'
    ghtk_df['carrier_id'] = 1

    # 3. Tổng hợp thông tin
    cuoc_phi_df = pd.concat([ninja_van_df, best_df, shopee_express_df, ghn_df, viettel_post_df, ghtk_df],
                            ignore_index=True)
    cuoc_phi_df = cuoc_phi_df[['carrier_id', 'carrier'] + COLUMNS_CUOC_PHI]
    cuoc_phi_df = cuoc_phi_df.set_index(['carrier_id', 'carrier', 'gt', 'lt_or_eq'])
    cuoc_phi_df = (cuoc_phi_df * 1000).astype(int).reset_index()

    cuoc_phi_df = pd.melt(
        cuoc_phi_df,
        id_vars=['carrier_id', 'carrier', 'gt', 'lt_or_eq'],
        value_vars=[
            'Nội Thành Tỉnh', 'Ngoại Thành Tỉnh',
            'Nội Thành Tp.HCM - HN', 'Ngoại Thành Tp.HCM - HN',
            'Nội Miền', 'Cận Miền', 'Cách Miền'
        ],
        var_name='order_type', value_name='price'
    )

    # 3. Check tên nhà vận chuyển đã được chuẩn hóa chưa
    set_carrier = set(cuoc_phi_df['carrier'].unique().tolist())
    set_norm_full_carrier = set(MAPPING_CARRIER_ID.keys())
    assert set_carrier - set_norm_full_carrier == set(), 'Ops, Tên nhà vận chuyển chưa được chuẩn hóa'

    # 4. Lưu thông tin đã xử lý
    cuoc_phi_df.to_parquet(ROOT_PATH + '/processed_data/cuoc_phi.parquet', index=False)
