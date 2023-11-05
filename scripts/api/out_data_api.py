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


def out_data_api():
    print('1. Lấy toàn bộ data')
    (
        ngung_giao_nhan, danh_gia_zns,
        ti_le_giao_hang, chat_luong_noi_bo,
        thoi_gian_giao_hang, kho_giao_nhan,
        tien_giao_dich
    ) = total_transform()

    print('2. Tính toán quận huyện quá tải')
    qua_tai1 = ngung_giao_nhan.loc[ngung_giao_nhan['score'].isin(OVERLOADING_SCORE_DICT['Ngưng giao nhận'])]
    qua_tai1 = qua_tai1[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status'})

    qua_tai2 = danh_gia_zns.loc[
        danh_gia_zns['score'].isin(OVERLOADING_SCORE_DICT['Đánh giá ZNS'])]
    qua_tai2 = qua_tai2[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status'})
    qua_tai2.loc[
        qua_tai2['carrier_status'] == 'Loại', 'carrier_status'] = 'Tổng số đánh giá ZNS 1, 2 sao >= 30% tổng đơn'

    qua_tai3 = ti_le_giao_hang.loc[
        ti_le_giao_hang['score'].isin(OVERLOADING_SCORE_DICT['Tỉ lệ hoàn hàng'])]
    qua_tai3 = qua_tai3[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status'})

    qua_tai4 = thoi_gian_giao_hang.loc[thoi_gian_giao_hang['score'].isin(OVERLOADING_SCORE_DICT['Thời gian giao hàng'])]
    qua_tai4['carrier_status'] = qua_tai4['status'] + ' (' + qua_tai4['order_type'] + ')'
    qua_tai4 = qua_tai4[['receiver_province', 'receiver_district', 'carrier', 'carrier_status']]

    qua_tai5 = kho_giao_nhan.loc[kho_giao_nhan['score'].isin(OVERLOADING_SCORE_DICT['Có kho giao nhận'])]
    qua_tai5 = qua_tai5[['receiver_province', 'receiver_district', 'carrier', 'status']].rename(
        columns={'status': 'carrier_status'})
    qua_tai = pd.concat([qua_tai1, qua_tai2, qua_tai3, qua_tai4, qua_tai5])

    qua_tai = (
        qua_tai.groupby([
            'receiver_province', 'receiver_district', 'carrier'
        ])['carrier_status'].apply(lambda x: ' + '.join(x))
            .reset_index()
    )

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
        'estimate_delivery_time'
    ] = thoi_gian_giao_hang_final['default_delivery_time']

    thoi_gian_giao_hang_final.loc[
        thoi_gian_giao_hang_final['total_order'] == 0,
        'estimate_delivery_time_details'
    ] = thoi_gian_giao_hang_final['default_delivery_time_details']

    print('4. Xủ lý score')
    score_df_list = []

    for target_df in [danh_gia_zns, ti_le_giao_hang, chat_luong_noi_bo, thoi_gian_giao_hang, kho_giao_nhan]:
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

    score_final['stars'] = 1
    score_final.loc[score_final['score'] > 0.15, 'stars'] = 2
    score_final.loc[score_final['score'] > 0.3, 'stars'] = 3
    score_final.loc[score_final['score'] > 0.5, 'stars'] = 4
    score_final.loc[score_final['score'] > 0.8, 'stars'] = 5

    # 6. Combine api data
    print('6. Combine api data')
    api_data_final = (
        thoi_gian_giao_hang_final[[
            'receiver_province', 'receiver_district', 'carrier', 'order_type',
            'estimate_delivery_time', 'estimate_delivery_time_details',
        ]].merge(score_final, on=['receiver_province', 'receiver_district', 'carrier'], how='inner')
            .merge(
            ti_le_giao_hang[[
                'receiver_province', 'receiver_district', 'carrier', 'delivery_success_rate'
            ]], on=['receiver_province', 'receiver_district', 'carrier'],
            how='inner'
        )
    )
    api_data_final['delivery_success_rate'] = np.round(api_data_final['delivery_success_rate'] * 100, 2)

    print('7. Gắn thông tin quá tải')
    api_data_final = api_data_final.merge(qua_tai, on=['receiver_province', 'receiver_district', 'carrier'], how='left')
    api_data_final['carrier_status'] = api_data_final['carrier_status'].fillna('Bình thường')

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
    api_data_final = api_data_final[[
        'receiver_province_id', 'receiver_province', 'receiver_district_id', 'receiver_district',
        'carrier_id', 'carrier', 'order_type', 'carrier_status', 'estimate_delivery_time_details',
        'estimate_delivery_time', 'delivery_success_rate', 'score', 'stars',
    ]]
    print('8. Lưu dữ liệu API')
    with open('./output/data_api.json', 'w', encoding='utf-8') as file:
        api_data_final.to_json(file, force_ascii=False)

    api_data_final.to_parquet('./output/data_api.parquet', index=False)
    print('>>> Done\n')

    print('-' * 100)


def combine_full_data():
    # Lấy toàn bộ data output API join với data giao dịch có khối lượng
    # để tunning score, check lỗi

    print('1. Đọc thông tin data API + giao dịch có khối lượng')
    api_data_final = pd.read_parquet('./output/data_api.parquet')
    _, _, _, _, _, _, tien_giao_dich = total_transform()

    full_information_df = (
        tien_giao_dich[[
            'order_id', 'receiver_province', 'receiver_district',
            'carrier', 'order_type', 'sys_order_type', 'weight', 'service_fee'
        ]].merge(
            api_data_final,
            on=['receiver_province', 'receiver_district', 'carrier', 'order_type'],
            how='left'
        )
    )
    full_information_df['carrier_id'] = full_information_df['carrier'].map(MAPPING_CARRIER_ID)
    assert len(full_information_df) == len(tien_giao_dich), 'Transform data không chính xác'

    print('2. Tính toán notification')
    # Transform này chỉ lấy được 1 dòng service_fee nhỏ nhất
    re_nhat_df = full_information_df.groupby(['order_id'])['service_fee'].min().reset_index()
    re_nhat_df['notification'] = 'Rẻ nhất'
    # Gắn ngược lại để lấy đủ row (trong trường hợp có nhiều carrier cùng mức giá
    re_nhat_df = re_nhat_df.merge(full_information_df, on=['order_id', 'service_fee'], how='inner')

    full_information_df1 = merge_left_only(full_information_df, re_nhat_df, keys=['order_id', 'service_fee'])

    nhanh_nhat_df = full_information_df1.groupby(['order_id'])['estimate_delivery_time_details'].min().reset_index()
    nhanh_nhat_df['notification'] = 'Nhanh nhất'
    nhanh_nhat_df = nhanh_nhat_df.merge(full_information_df1, on=['order_id', 'estimate_delivery_time_details'],
                                        how='inner')

    full_information_df2 = merge_left_only(full_information_df1, nhanh_nhat_df,
                                           keys=['order_id', 'estimate_delivery_time_details'])

    hieu_qua_nhat_df = full_information_df2.groupby(['order_id'])['score'].max().reset_index()
    hieu_qua_nhat_df['notification'] = 'Dịch vụ tốt'
    hieu_qua_nhat_df = hieu_qua_nhat_df.merge(full_information_df2, on=['order_id', 'score'], how='inner')

    full_information_df3 = merge_left_only(full_information_df2, hieu_qua_nhat_df, keys=['order_id', 'score'])
    full_information_df3['notification'] = 'Bình thường'

    full_information_df = pd.concat([
        re_nhat_df,
        nhanh_nhat_df,
        hieu_qua_nhat_df,
        full_information_df3
    ], ignore_index=True)

    full_information_df = full_information_df[[
        'order_id',
        'receiver_province_id', 'receiver_province', 'receiver_district_id', 'receiver_district',
        'carrier_id', 'carrier', 'order_type', 'sys_order_type',
        'weight', 'service_fee', 'carrier_status',
        'estimate_delivery_time_details', 'estimate_delivery_time', 'delivery_success_rate',
        'score', 'stars', 'notification',
    ]]

    assert full_information_df.isna().sum().all() == 0, 'Transform data không chính xác'

    print('3. Lưu thông tin')
    full_information_df.to_parquet('./output/data_full.parquet', index=False)
    print('>>> Done\n')


if __name__ == '__main__':
    out_data_api()
    combine_full_data()
