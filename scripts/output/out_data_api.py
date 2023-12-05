import sys
from pathlib import Path
ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)

from scripts.utilities.helper import *
from scripts.utilities.config import *
from scripts.transform.total_transform import total_transform

API_FULL_COLS = [
    'receiver_province_id', 'receiver_province',
    'receiver_district_id', 'receiver_district',
    'carrier_id', 'carrier', 'order_type',
    'order_type_id', 'sys_order_type_id', 'carrier_status', 'carrier_status_comment',
    'estimate_delivery_time_details', 'estimate_delivery_time',
    'customer_best_carrier_id',
    'fastest_carrier_id', 'highest_score_carrier_id',
    'total_order', 'delivery_success_rate_id',
    'delivery_success_rate', 'score', 'star',
]
API_FULL_COLS_RENAMED = [
    'receiver_province_code', 'receiver_province', 
    'receiver_district_code', 'receiver_district',
    'carrier_id', 'carrier', 'order_type', 
    'new_type', 'route_type', 'status', 'description',
    'time_data', 'time_display',
    'for_shop',
    'speed_ranking', 'score_ranking',
    'total_order', 'rate_ranking',
    'rate', 'score', 'star',
]

API_COLS = [
    'receiver_province_id', 'receiver_district_id',
    'carrier_id', 'order_type_id', 'sys_order_type_id', 'carrier_status', 'carrier_status_comment',
    'estimate_delivery_time_details', 'estimate_delivery_time',
    'fastest_carrier_id', 'highest_score_carrier_id',
    'customer_best_carrier_id', 'total_order', 'delivery_success_rate_id',
    'delivery_success_rate', 'score', 'star',
]

API_COLS_RENAMED = [
    'receiver_province_code', 'receiver_district_code',
    'carrier_id', 'new_type', 'route_type', 'status', 'description',
    'time_data', 'time_display',
    'speed_ranking', 'score_ranking',
    'for_shop', 'total_order', 'rate_ranking',
    'rate', 'score', 'star',
]

THOI_GIAN_GIAO_HANG_DEFAULT = {
    'Nội Thành Tỉnh': '1.75 - 2.25 ngày',
    'Ngoại Thành Tỉnh': '1.75 - 2.25 ngày',
    'Nội Thành Tp.HCM - HN': '1.75 - 2.25 ngày',
    'Ngoại Thành Tp.HCM - HN': '1.75 - 2.25 ngày',
    'Nội Miền Tp.HCM - HN': '0.75 - 1.25 ngày',
    'Nội Miền': '1.75 - 2.25 ngày',
    'Cận Miền': '2.75 - 3.25 ngày',
    'Liên Miền Tp.HCM - HN': '2.75 - 3.25 ngày',
    'Liên Miền Đặc Biệt': '2.75 - 3.25 ngày',
    'Cách Miền': '3.75 - 4.25 ngày',
}


def round_value(x):
    th1 = round(x - 0.25, 1)
    th2 = round(x + 0.25, 1)
    return '{} - {} ngày'.format(th1, th2)


def customer_best_carrier_old(data_api_df, threshold=15):
    df1 = data_api_df.loc[data_api_df['total_order'] > threshold]
    df2 = data_api_df.loc[(data_api_df['total_order'] >= 1) & (data_api_df['total_order'] <= threshold)]
    df3 = data_api_df.loc[data_api_df['total_order'] == 0]

    group1 = (
        df1.sort_values(['delivery_success_rate', 'estimate_delivery_time_details'], ascending=[False, True])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'customer_best_carrier'})
    )
    group2 = (
        df2.sort_values(['estimate_delivery_time_details', 'delivery_success_rate'], ascending=[True, False])
            .drop_duplicates(['receiver_province', 'receiver_district', 'order_type'], keep='first')
        [['receiver_province', 'receiver_district', 'order_type', 'carrier']]
            .rename(columns={'carrier': 'customer_best_carrier'})
    )
    group3 = df3[['receiver_province', 'receiver_district', 'order_type']].drop_duplicates()
    group3['customer_best_carrier'] = CUSTOMER_BEST_CARRIER_DEFAULT

    customer_best_carrier_df = pd.concat([group1, group2, group3]).drop_duplicates(
        ['receiver_province', 'receiver_district', 'order_type'], keep='first')

    return customer_best_carrier_df


def customer_best_carrier(data_api_df):

    data_api_df['combine_col'] = data_api_df[["delivery_success_rate", "total_order"]].apply(tuple, axis=1)

    data_api_df["delivery_success_rate_id"] = \
        data_api_df.groupby(["receiver_province_id", "receiver_district_id", "order_type_id"])["combine_col"].rank(
            method="dense", ascending=False).astype(int)

    data_api_df['wscore'] = data_api_df['fastest_carrier_id'] * 1.4 + data_api_df['delivery_success_rate_id'] * 1.2 + \
                            data_api_df['highest_score_carrier_id']

    data_api_df["customer_best_carrier_id"] = \
        data_api_df.groupby(["receiver_province_id", "receiver_district_id", "order_type_id"])["wscore"].rank(
            method="dense", ascending=True).astype(int)

    return data_api_df.drop(['combine_col', 'wscore'], axis=1)


def out_data_api(return_full_cols_df=False, show_logs=True):
    if show_logs:
        print('1. Transform dữ liệu...')
    (
        ngung_giao_nhan, danh_gia_zns,
        ti_le_giao_hang, chat_luong_noi_bo,
        thoi_gian_giao_hang, kho_giao_nhan,
    ) = total_transform(show_logs=False)

    if show_logs:
        print('2. Tính toán quận huyện quá tải')
    qua_tai1 = ngung_giao_nhan.loc[ngung_giao_nhan['score'].isin(OVERLOADING_SCORE_DICT['Ngưng giao nhận'])]
    qua_tai1 = qua_tai1[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status_comment'})

    qua_tai2 = danh_gia_zns.loc[
        danh_gia_zns['score'].isin(OVERLOADING_SCORE_DICT['Đánh giá ZNS'])]
    qua_tai2 = qua_tai2[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status_comment'})
    qua_tai2.loc[
        qua_tai2[
            'carrier_status_comment'] == 'Loại', 'carrier_status_comment'] = 'Tổng số đánh giá ZNS 1, 2 sao >= 30% tổng đơn'

    qua_tai3 = ti_le_giao_hang.loc[
        ti_le_giao_hang['score'].isin(OVERLOADING_SCORE_DICT['Tỉ lệ giao hàng'])]
    qua_tai3 = qua_tai3[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status_comment'})

    qua_tai4 = chat_luong_noi_bo.loc[chat_luong_noi_bo['score'].isin(OVERLOADING_SCORE_DICT['Chất lượng nội bộ'])]
    qua_tai4['carrier_status_comment'] = qua_tai4['status'] + ' (clnb)'
    qua_tai4 = qua_tai4[['receiver_province', 'receiver_district', 'carrier', 'carrier_status_comment']]

    qua_tai5 = thoi_gian_giao_hang.loc[thoi_gian_giao_hang['score'].isin(OVERLOADING_SCORE_DICT['Thời gian giao hàng'])]
    qua_tai5['carrier_status_comment'] = qua_tai5['status'] + ' (' + qua_tai5['order_type'] + ')'
    qua_tai5 = qua_tai5[['receiver_province', 'receiver_district', 'carrier', 'carrier_status_comment']]

    qua_tai6 = kho_giao_nhan.loc[kho_giao_nhan['score'].isin(OVERLOADING_SCORE_DICT['Có kho giao nhận'])]
    qua_tai6 = qua_tai6[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status_comment'})
    qua_tai = pd.concat([qua_tai1, qua_tai2, qua_tai3, qua_tai4, qua_tai5, qua_tai6])

    qua_tai = (
        qua_tai.groupby([
            'receiver_province', 'receiver_district', 'carrier'
        ])['carrier_status_comment'].apply(lambda x: ' + '.join(x))
            .reset_index()
    )

    if show_logs:
        print('3. Xử lý data thời gian giao dịch')
    thoi_gian_giao_hang = thoi_gian_giao_hang.rename(columns={'delivery_time_mean_h': 'estimate_delivery_time_details'})
    thoi_gian_giao_hang['estimate_delivery_time_details'] = np.round(
        thoi_gian_giao_hang['estimate_delivery_time_details'] / 24, 2)
    thoi_gian_giao_hang['estimate_delivery_time'] = thoi_gian_giao_hang['estimate_delivery_time_details'].apply(
        round_value)

    # Thời gian giao hàng default
    active_carrier_df = pd.DataFrame(data={
        'carrier': ACTIVE_CARRIER,
    })
    loai_van_chuyen_df = pd.DataFrame(THOI_GIAN_GIAO_HANG_DEFAULT.items(),
                                      columns=['order_type', 'default_delivery_time'])
    loai_van_chuyen_df['default_delivery_time_details'] = [2, 2, 2, 2, 1, 2, 3, 3, 3, 4]

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
        'estimate_delivery_time'
    ] = thoi_gian_giao_hang_final['default_delivery_time']

    thoi_gian_giao_hang_final.loc[
        thoi_gian_giao_hang_final['total_order'] == 0,
        'estimate_delivery_time_details'
    ] = thoi_gian_giao_hang_final['default_delivery_time_details']

    if show_logs:
        print('4. Xủ lý score')
    score_df_list = []

    for focus_df in [ngung_giao_nhan, danh_gia_zns, ti_le_giao_hang, chat_luong_noi_bo, thoi_gian_giao_hang, kho_giao_nhan]:
        target_df = focus_df.copy()
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

    if show_logs:
        print('5. Combine api data')
    api_data_final = (
        thoi_gian_giao_hang_final[[
            'receiver_province', 'receiver_district', 'carrier', 'order_type',
            'estimate_delivery_time', 'estimate_delivery_time_details',
        ]].merge(score_final, on=['receiver_province', 'receiver_district', 'carrier'], how='inner')
            .merge(
            ti_le_giao_hang[[
                'receiver_province', 'receiver_district', 'carrier', 'total_order', 'delivery_success_rate'
            ]], on=['receiver_province', 'receiver_district', 'carrier'],
            how='inner'
        )
    )
    api_data_final['delivery_success_rate'] = np.round(api_data_final['delivery_success_rate'] * 100, 2)

    if show_logs:
        print('6. Gắn thông tin quá tải')
    api_data_final = api_data_final.merge(qua_tai, on=['receiver_province', 'receiver_district', 'carrier'], how='left')
    api_data_final.loc[api_data_final['total_order'] == 0, 'carrier_status_comment'] = 'Không có đơn hàng'
    api_data_final['carrier_status_comment'] = api_data_final['carrier_status_comment'].fillna('Bình thường')
    api_data_final['carrier_status'] = 0
    api_data_final.loc[api_data_final['carrier_status_comment'] == 'Quá tải', 'carrier_status'] = 1
    api_data_final.loc[~api_data_final['carrier_status_comment'].isin(['Bình thường', 'Quá tải', 'Không có đơn hàng']), 'carrier_status'] = 2

    api_data_final['carrier_id'] = api_data_final['carrier'].map(MAPPING_CARRIER_ID)
    api_data_final = (
        api_data_final.merge(
            PROVINCE_MAPPING_DISTRICT_DF.rename(columns={
                'province': 'receiver_province',
                'district': 'receiver_district',
                'province_id': 'receiver_province_id',
                'district_id': 'receiver_district_id',
            }), on=['receiver_province', 'receiver_district'], how='left'
        )
    )
    api_data_final['order_type_id'] = api_data_final['order_type'].map(MAPPING_ORDER_TYPE_ID)

    if show_logs:
        print('7. Thông tin nhà vận chuyển nhanh nhất, hiệu quả nhất')
    api_data_final["fastest_carrier_id"] = \
        api_data_final.groupby(["receiver_province_id", "receiver_district_id", "order_type_id"])[
            "estimate_delivery_time_details"].rank(method="dense", ascending=True)
    api_data_final["fastest_carrier_id"] = api_data_final["fastest_carrier_id"].astype(int)

    api_data_final["highest_score_carrier_id"] = \
        api_data_final.groupby(["receiver_province_id", "receiver_district_id", "order_type_id"])["score"].rank(
            method="dense", ascending=False)
    api_data_final["highest_score_carrier_id"] = api_data_final["highest_score_carrier_id"].astype(int)

    if show_logs:
        print('8. Thông tin customer_best_carrier')
    api_data_final = customer_best_carrier(api_data_final)

    if show_logs:
        print('9. Thông tin số sao đánh giá của khách hàng')
    zns_df = pd.read_parquet(ROOT_PATH + '/processed_data/danh_gia_zns.parquet')
    zns_df = zns_df.groupby(['receiver_province', 'receiver_district', 'carrier']).agg(
        star=('n_stars', 'mean')).reset_index()
    zns_df['star'] = np.round(zns_df['star'], 1)

    api_data_final = api_data_final.merge(zns_df, on=['receiver_province', 'receiver_district', 'carrier'], how='left')
    api_data_final['star'] = api_data_final['star'].fillna(5.0)
    api_data_final['sys_order_type_id'] = api_data_final['order_type_id'].map(MAPPING_ORDER_TYPE_ID_ROUTE_TYPE)
    api_data_final['carrier_status'] = api_data_final['carrier_status'].astype(str)
    api_data_final['order_type_id'] = api_data_final['order_type_id'].astype(str)
    api_data_final['sys_order_type_id'] = api_data_final['sys_order_type_id'].astype(str)

    if return_full_cols_df:
        api_data_final = api_data_final[API_FULL_COLS]
        api_data_final.columns = API_FULL_COLS_RENAMED
        return api_data_final
    else:
        api_data_final = api_data_final[API_COLS]
        api_data_final.columns = API_COLS_RENAMED
        print('Shape: ', api_data_final.shape)
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