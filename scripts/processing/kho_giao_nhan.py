from scripts.utilities.helper import *


def split_buu_cuc_ninja_van(s):
    if ' - ' in s:
        return s.split(' - ')[1]
    else:
        return s


def xu_ly_kho_giao_nhan():

    print('Ninja Van')
    buu_cuc_njv_df = pd.read_excel(ROOT_PATH + '/input/Bưu Cục NJV.xlsx')
    buu_cuc_njv_df = buu_cuc_njv_df[1:]

    buu_cuc_njv_df.columns = [
        'region', 'receiver_province', 'id_receiver_district', 'receiver_district',
        'short_name', 'njv_post_office', 'delivery_success_rate', 'don_den_tram'
    ]
    buu_cuc_njv_df = buu_cuc_njv_df[['receiver_province', 'receiver_district', 'njv_post_office']]
    buu_cuc_njv_df['receiver_province'] = buu_cuc_njv_df['receiver_province'].astype(str)
    buu_cuc_njv_df['receiver_district'] = buu_cuc_njv_df['receiver_district'].astype(str)
    buu_cuc_njv_df['receiver_district_remove_accent'] = buu_cuc_njv_df['receiver_district'].apply(unidecode)
    buu_cuc_njv_df['njv_post_office_short'] = buu_cuc_njv_df['njv_post_office'].astype(str).apply(split_buu_cuc_ninja_van)
    buu_cuc_njv_df['is_right'] = buu_cuc_njv_df.apply(
        lambda s: str(s['njv_post_office_short']) in str(s['receiver_district_remove_accent']), axis=1)
    buu_cuc_njv_df = buu_cuc_njv_df.loc[buu_cuc_njv_df['is_right']]

    # Chuẩn hóa quận/huyện, tỉnh/thành
    buu_cuc_njv_df = normalize_province_district(buu_cuc_njv_df, tinh_thanh='receiver_province',
                                                 quan_huyen='receiver_district')

    # Loại bỏ thông tin rỗng
    buu_cuc_njv_df = buu_cuc_njv_df.loc[
        buu_cuc_njv_df['receiver_province'].notna() &
        buu_cuc_njv_df['receiver_district'].notna()
        ].reset_index(drop=True)

    buu_cuc_njv_df = buu_cuc_njv_df.groupby(['receiver_province', 'receiver_district'])['njv_post_office'].count().rename(
        'n_post_offices').reset_index()

    buu_cuc_njv_df.to_parquet(ROOT_PATH + '/processed_data/buu_cuc_ninja_van.parquet', index=False)
    print('-' * 100)

    #############################################################################################

    print('GHN')
    buu_cuc_ghn_df = pd.read_excel(ROOT_PATH + '/input/Bưu Cục GHN.xlsx')

    buu_cuc_ghn_df.columns = ['address', 'receiver_province', 'receiver_district']
    buu_cuc_ghn_df['receiver_province'] = buu_cuc_ghn_df['receiver_province'].astype(str)
    buu_cuc_ghn_df['receiver_district'] = buu_cuc_ghn_df['receiver_district'].astype(str)

    # Chuẩn hóa quận/huyện, tỉnh/thành
    buu_cuc_ghn_df = normalize_province_district(buu_cuc_ghn_df, tinh_thanh='receiver_province',
                                                 quan_huyen='receiver_district')

    # Loại bỏ thông tin rỗng
    buu_cuc_ghn_df = buu_cuc_ghn_df.loc[
        buu_cuc_ghn_df['receiver_province'].notna() &
        buu_cuc_ghn_df['receiver_district'].notna()
        ].reset_index(drop=True)

    buu_cuc_ghn_df = buu_cuc_ghn_df.groupby(['receiver_province', 'receiver_district'])['address'].count().rename(
        'n_post_offices').reset_index()

    buu_cuc_ghn_df.to_parquet(ROOT_PATH + '/processed_data/buu_cuc_ghn.parquet', index=False)
    print('-' * 100)

    #############################################################################################

    print('BEST Express')
    buu_cuc_best_df = pd.read_excel(ROOT_PATH + '/input/Bưu Cục Best.xlsx')

    buu_cuc_best_df.columns = ['id', 'area', 'receiver_province', 'receiver_district', 'receiver_ward', 'best_post_office']
    buu_cuc_best_df['receiver_province'] = buu_cuc_best_df['receiver_province'].astype(str)
    buu_cuc_best_df['receiver_district'] = buu_cuc_best_df['receiver_district'].astype(str)
    buu_cuc_best_df['best_post_office'] = buu_cuc_best_df['best_post_office'].str.title()

    # Chọn đúng bưu cục theo tên phường/xã
    buu_cuc_best_df['is_right'] = buu_cuc_best_df.apply(lambda s: str(s['receiver_ward']) in str(s['best_post_office']), axis=1)
    buu_cuc_best_df = buu_cuc_best_df.loc[buu_cuc_best_df['is_right']][
        ['receiver_province', 'receiver_district', 'receiver_ward', 'best_post_office']]

    # Chuẩn hóa quận/huyện, tỉnh/thành
    buu_cuc_best_df = normalize_province_district(buu_cuc_best_df, tinh_thanh='receiver_province',
                                                  quan_huyen='receiver_district')

    # Loại bỏ thông tin rỗng
    buu_cuc_best_df = buu_cuc_best_df.loc[
        buu_cuc_best_df['receiver_province'].notna() &
        buu_cuc_best_df['receiver_district'].notna()
        ].reset_index(drop=True)

    buu_cuc_best_df = buu_cuc_best_df.groupby(['receiver_province', 'receiver_district'])['best_post_office'].count().rename(
        'n_post_offices').reset_index()

    # Lưu thông tin
    buu_cuc_best_df.to_parquet(ROOT_PATH + '/processed_data/buu_cuc_best.parquet', index=False)
    print('-' * 100)

    #############################################################################################

    print('GHTK')
    buu_cuc_ghtk_df = pd.read_excel(ROOT_PATH + '/input/Bưu Cục GHTK.xlsx')

    buu_cuc_ghtk_df = buu_cuc_ghtk_df[['Tên bưu cục', 'Địa chỉ']]
    buu_cuc_ghtk_df.columns = ['ghtk_post_office', 'address']

    # Tách quận/huyện, tinh/thành
    buu_cuc_ghtk_df['receiver_province'] = buu_cuc_ghtk_df['address'].str.split(', ').str[-1].astype(str)
    buu_cuc_ghtk_df['receiver_district'] = buu_cuc_ghtk_df['address'].str.split(', ').str[-2].astype(str)

    # Chuẩn hóa quận/huyện, tỉnh/thành
    buu_cuc_ghtk_df = normalize_province_district(buu_cuc_ghtk_df, tinh_thanh='receiver_province',
                                                  quan_huyen='receiver_district')

    # Loại bỏ thông tin rỗng
    buu_cuc_ghtk_df = buu_cuc_ghtk_df.loc[
        buu_cuc_ghtk_df['receiver_province'].notna() &
        buu_cuc_ghtk_df['receiver_district'].notna()
        ].reset_index(drop=True)

    buu_cuc_ghtk_df = buu_cuc_ghtk_df.groupby(['receiver_province', 'receiver_district'])['ghtk_post_office'].count().rename(
        'n_post_offices').reset_index()

    buu_cuc_ghtk_df.to_parquet(ROOT_PATH + '/processed_data/buu_cuc_ghtk.parquet', index=False)
    print('-' * 100)
