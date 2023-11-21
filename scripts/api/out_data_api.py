import sys
from pathlib import Path
ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)

from scripts.utilities.helper import *
from scripts.utilities.config import *
from scripts.transform.total_transform import total_transform

THOI_GIAN_GIAO_HANG_DEFAULT = {
    'Nội Miền': '2.0 - 2.5 ngày',
    'Cận Miền': '3.0 - 3.5 ngày',
    'Cách Miền': '4.0 - 4.5 ngày',
    'Nội Thành Tỉnh': '2.0 - 2.5 ngày',
    'Ngoại Thành Tỉnh': '2.0 - 2.5 ngày',
    'Nội Thành Tp.HCM - HN': '2.0 - 2.5 ngày',
    'Ngoại Thành Tp.HCM - HN': '2.0 - 2.5 ngày',
}


def round_value(x):
    round_05 = int(x) + 0.5
    if x < round_05:
        return '{} - {} ngày'.format(round_05, round_05 + 0.5)
    else:
        return '{} - {} ngày'.format(round_05 + 0.5, round_05 + 1)


def shop_best_carrier_old(data_api_df, threshold=15):
    df1 = data_api_df.loc[data_api_df['total_order'] > threshold]
    df2 = data_api_df.loc[(data_api_df['total_order'] >= 1) & (data_api_df['total_order'] <= threshold)]
    df3 = data_api_df.loc[data_api_df['total_order'] == 0]

    group1 = (
        df1.sort_values(['rate', 'time_data'], ascending=[False, True])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'shop_best_carrier'})
    )
    group2 = (
        df2.sort_values(['time_data', 'rate'], ascending=[True, False])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'shop_best_carrier'})
    )
    group3 = df3[['receiver_province', 'receiver_district', 'order_type']].drop_duplicates()
    group3['shop_best_carrier'] = SHOP_BEST_CARRIER_DEFAULT

    shop_best_carrier_df = pd.concat([group1, group2, group3]).drop_duplicates(
        ['receiver_province', 'receiver_district', 'order_type'], keep='first')

    return shop_best_carrier_df


def shop_best_carrier(data_api_df):
    data_api_df['combine_col'] = data_api_df[['rate', "total_order"]].apply(tuple, axis=1)
    data_api_df['rate_ranking'] = \
        data_api_df.groupby(['receiver_province_code', 'receiver_district_code', 'new_type'])["combine_col"].rank(
            method="dense", ascending=False).astype(int)
    data_api_df['wscore'] = data_api_df['speed_ranking'] * 1.4 + data_api_df['rate_ranking'] * 1.2 + \
                            data_api_df['score_ranking']
    shop_best_carrier_df = (
        data_api_df.sort_values([
            'receiver_province_code', 'receiver_district_code', 'new_type', 'wscore'
        ]).drop_duplicates(['receiver_province_code', 'receiver_district_code', 'new_type'])
        [['receiver_province_code', 'receiver_district_code', 'new_type', 'carrier']]
            .rename(columns={'carrier': 'shop_best_carrier'})
    )
    data_api_df = data_api_df.merge(shop_best_carrier_df,
                                    on=['receiver_province_code', 'receiver_district_code', 'new_type'], how='inner')
    data_api_df['for_fshop'] = data_api_df['shop_best_carrier'].map(MAPPING_CARRIER_ID)

    return data_api_df.drop(['combine_col', 'wscore'], axis=1)


def out_data_api(return_full_cols_df=False, show_logs=True):
    if show_logs:
        print('1. Transform dữ liệu...')
    (
        ngung_giao_nhan, danh_gia_zns,
        ti_le_giao_hang, chat_luong_noi_bo,
        thoi_gian_giao_hang, kho_giao_nhan,
        # tien_giao_dich
    ) = total_transform(show_logs=False)

    if show_logs:
        print('2. Tính toán quận huyện quá tải')
    qua_tai1 = ngung_giao_nhan.loc[ngung_giao_nhan['score'].isin(OVERLOADING_SCORE_DICT['Ngưng giao nhận'])]
    qua_tai1 = qua_tai1[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'description'})

    qua_tai2 = danh_gia_zns.loc[
        danh_gia_zns['score'].isin(OVERLOADING_SCORE_DICT['Đánh giá ZNS'])]
    qua_tai2 = qua_tai2[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'description'})
    qua_tai2.loc[
        qua_tai2[
            'description'] == 'Loại', 'description'] = 'Tổng số đánh giá ZNS 1, 2 sao >= 30% tổng đơn'

    qua_tai3 = ti_le_giao_hang.loc[
        ti_le_giao_hang['score'].isin(OVERLOADING_SCORE_DICT['Tỉ lệ hoàn hàng'])]
    qua_tai3 = qua_tai3[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'description'})

    qua_tai4 = thoi_gian_giao_hang.loc[thoi_gian_giao_hang['score'].isin(OVERLOADING_SCORE_DICT['Thời gian giao hàng'])]
    qua_tai4['description'] = qua_tai4['status'] + ' (' + qua_tai4['order_type'] + ')'
    qua_tai4 = qua_tai4[['receiver_province', 'receiver_district', 'carrier', 'description']]

    qua_tai5 = kho_giao_nhan.loc[kho_giao_nhan['score'].isin(OVERLOADING_SCORE_DICT['Có kho giao nhận'])]
    qua_tai5 = qua_tai5[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'description'})
    qua_tai = pd.concat([qua_tai1, qua_tai2, qua_tai3, qua_tai4, qua_tai5])

    qua_tai = (
        qua_tai.groupby([
            'receiver_province', 'receiver_district', 'carrier'
        ])['description'].apply(lambda x: ' + '.join(x))
            .reset_index()
    )

    if show_logs:
        print('3. Xử lý data thời gian giao dịch')
    thoi_gian_giao_hang = thoi_gian_giao_hang.rename(columns={'delivery_time_mean_h': 'time_data'})
    thoi_gian_giao_hang['time_data'] = np.round(
        thoi_gian_giao_hang['time_data'] / 24, 2)
    thoi_gian_giao_hang['time_display'] = thoi_gian_giao_hang['time_data'].apply(
        round_value)

    # Thời gian giao hàng default
    active_carrier_df = pd.DataFrame(data={
        'carrier': ACTIVE_CARRIER,
    })
    loai_van_chuyen_df = pd.DataFrame(THOI_GIAN_GIAO_HANG_DEFAULT.items(),
                                      columns=['order_type', 'default_delivery_time'])
    loai_van_chuyen_df['default_delivery_time_details'] = [2, 3, 4, 2, 2, 2, 2]

    thoi_gian_giao_hang_default = (
        PROVINCE_MAPPING_DISTRICT_DF[['province', 'district']].rename(columns={
            'province': 'receiver_province',
            'district': 'receiver_district',
        })
            .merge(
            active_carrier_df.merge(loai_van_chuyen_df, how='cross'),
            how='cross'
        )
    )

    thoi_gian_giao_hang_final = (
        thoi_gian_giao_hang_default.merge(
            thoi_gian_giao_hang,
            on=['receiver_province', 'receiver_district', 'carrier', 'order_type'],
            how='left'
        )
    )

    thoi_gian_giao_hang_final.loc[
        thoi_gian_giao_hang_final['total_order'] == 0,
        'time_display'
    ] = thoi_gian_giao_hang_final['default_delivery_time']

    thoi_gian_giao_hang_final.loc[
        thoi_gian_giao_hang_final['total_order'] == 0,
        'time_data'
    ] = thoi_gian_giao_hang_final['default_delivery_time_details']

    if show_logs:
        print('4. Xủ lý score')
    score_df_list = []

    for target_df in [ngung_giao_nhan, danh_gia_zns, ti_le_giao_hang, chat_luong_noi_bo, thoi_gian_giao_hang, kho_giao_nhan]:
        target_df['weight_score'] = target_df['score'] * target_df['criteria_weight']
        score_df_list.append(target_df[['receiver_province', 'receiver_district', 'carrier', 'weight_score']])

    score_df = pd.concat(score_df_list, ignore_index=False)
    score_final = score_df.groupby(['receiver_province', 'receiver_district', 'carrier'])[
        'weight_score'].mean().reset_index()
    score_final = score_final.rename(columns={'weight_score': 'score'})

    q_lower = score_final['score'].quantile(0.005)
    q_upper = score_final['score'].quantile(0.995)

    score_final.loc[score_final['score'] < q_lower, 'score'] = q_lower
    score_final.loc[score_final['score'] > q_upper, 'score'] = q_upper
    score_final['score'] = (score_final['score'] - q_lower) / (q_upper - q_lower)
    score_final['score'] = np.round(score_final['score'], 2)

    # score_final['stars'] = 1
    # score_final.loc[score_final['score'] > 0.15, 'stars'] = 2
    # score_final.loc[score_final['score'] > 0.3, 'stars'] = 3
    # score_final.loc[score_final['score'] > 0.5, 'stars'] = 4
    # score_final.loc[score_final['score'] > 0.8, 'stars'] = 5

    if show_logs:
        print('5. Combine api data')
    api_data_final = (
        thoi_gian_giao_hang_final[[
            'receiver_province', 'receiver_district', 'carrier', 'order_type',
            'time_display', 'time_data',
        ]].merge(score_final, on=['receiver_province', 'receiver_district', 'carrier'], how='inner')
            .merge(
            ti_le_giao_hang[[
                'receiver_province', 'receiver_district', 'carrier', 'total_order', 'rate'
            ]], on=['receiver_province', 'receiver_district', 'carrier'],
            how='inner'
        )
    )
    api_data_final['rate'] = np.round(api_data_final['rate'] * 100, 2)

    if show_logs:
        print('6. Gắn thông tin quá tải')
    api_data_final = api_data_final.merge(qua_tai, on=['receiver_province', 'receiver_district', 'carrier'], how='left')
    api_data_final['description'] = api_data_final['description'].fillna('Bình thường')
    api_data_final['status'] = 0
    api_data_final.loc[api_data_final['description'] == 'Quá tải', 'status'] = 1
    api_data_final.loc[~api_data_final['description'].isin(['Bình thường', 'Quá tải']), 'status'] = 2

    api_data_final['carrier_id'] = api_data_final['carrier'].map(MAPPING_CARRIER_ID)
    api_data_final = (
        api_data_final.merge(
            PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                'province': 'receiver_province',
                'district': 'receiver_district',
                'province_code': 'receiver_province_code',
                'district_code': 'receiver_district_code',
            }), on=['receiver_province', 'receiver_district'], how='left'
        )
    )
    api_data_final['new_type'] = api_data_final['order_type'].map(MAPPING_ORDER_TYPE_ID)

    if show_logs:
        print('7. Thông tin nhà vận chuyển nhanh nhất, hiệu quả nhất')
    api_data_final['speed_ranking'] = \
        api_data_final.groupby(['receiver_province_code', 'receiver_district_code', 'new_type'])[
            'time_data'].rank(method="dense", ascending=True)
    api_data_final['speed_ranking'] = api_data_final['speed_ranking'].astype(int)

    api_data_final['score_ranking'] = \
        api_data_final.groupby(['receiver_province_code', 'receiver_district_code', 'new_type'])["score"].rank(
            method="dense", ascending=False)
    api_data_final['score_ranking'] = api_data_final['score_ranking'].astype(int)

    if show_logs:
        print('8. Thông tin shop_best_carrier')
    api_data_final = shop_best_carrier(api_data_final)

    if show_logs:
        print('9. Thông tin số sao đánh giá của khách hàng')
    zns_df = pd.read_parquet(ROOT_PATH + '/processed_data/danh_gia_zns.parquet')
    zns_df = zns_df.groupby(['receiver_province', 'receiver_district', 'carrier']).agg(
        stars=('n_stars', 'mean')).reset_index()
    zns_df['stars'] = np.round(zns_df['stars'], 1)

    api_data_final = api_data_final.merge(zns_df, on=['receiver_province', 'receiver_district', 'carrier'], how='left')
    api_data_final['stars'] = api_data_final['stars'].fillna(5.0)

    if return_full_cols_df:
        api_data_final = api_data_final[[
            'receiver_province_code', 'receiver_province', 'receiver_district_code', 'receiver_district',
            'carrier_id', 'carrier', 'order_type', 'new_type', 'status', 'description',
            'time_data', 'time_display',
            'shop_best_carrier', 'for_fshop',
            'speed_ranking', 'score_ranking',
            'total_order', 'rate_ranking',
            'rate', 'score', 'stars',
        ]]
        return api_data_final
    else:
        api_data_final = api_data_final[[
            'receiver_province_code', 'receiver_district_code',
            'carrier_id', 'new_type', 'status', 'description',
            'time_data', 'time_display',
            'speed_ranking', 'score_ranking',
            'for_fshop', 'total_order', 'rate_ranking',
            'rate', 'score', 'stars',
        ]]
        if show_logs:
            print('9. Lưu dữ liệu API')
        if not os.path.exists(ROOT_PATH + '/output'):
            os.makedirs(ROOT_PATH + '/output')
        with open(ROOT_PATH + '/output/data_api.json', 'w', encoding='utf-8') as file:
            api_data_final.to_json(file, force_ascii=False)

        api_data_final.to_parquet(ROOT_PATH + '/output/data_api.parquet', index=False)
    if show_logs:
        print('>>> Done\n')


if __name__ == '__main__':
    out_data_api()
