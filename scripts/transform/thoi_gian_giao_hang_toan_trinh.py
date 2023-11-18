from scripts.utilities.helper import *
from scripts.utilities.config import *


def score_thoi_gian_giao_hang(tong_don, thoi_gian_giao_tb, loai_van_chuyen):
    if tong_don == -1:
        return 'Không có thông tin'
    # group 1 (Cách Miền)
    if loai_van_chuyen == 'Cách Miền':
        # thời gian giao trung bình < 96h
        if (tong_don > 20) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # thời gian giao trung bình < 120h
        elif (tong_don > 30) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 30 đơn'
        elif (tong_don > 20) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # trễ
        elif (tong_don > 3) and (thoi_gian_giao_tb < 144):
            return 'Trung bình dưới 144h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 144):
            return 'Trung bình dưới 144h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif (tong_don > 3) and (thoi_gian_giao_tb < 168):
            return 'Trung bình dưới 168h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 168):
            return 'Trung bình dưới 168h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif thoi_gian_giao_tb >= 168:
            return 'Trung bình thời gian giao hàng lớn hơn hoặc bằng 168h'
    # group 1 (Cận Miền)
    if loai_van_chuyen == 'Cận Miền':
        # thời gian giao trung bình < 72h
        if (tong_don > 20) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # thời gian giao trung bình < 96h
        elif (tong_don > 30) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 30 đơn'
        elif (tong_don > 20) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # trễ
        elif (tong_don > 3) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif (tong_don > 3) and (thoi_gian_giao_tb < 144):
            return 'Trung bình dưới 144h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 144):
            return 'Trung bình dưới 144h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif thoi_gian_giao_tb >= 144:
            return 'Trung bình thời gian giao hàng lớn hơn hoặc bằng 144h'

    # group 2 (Nội Miền)
    if loai_van_chuyen == 'Nội Miền':
        # thời gian giao trung bình < 48h
        if (tong_don > 20) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # thời gian giao trung bình < 72h
        elif (tong_don > 30) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn'
        elif (tong_don > 20) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # trễ
        elif (tong_don > 3) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif (tong_don > 3) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 120):
            return 'Trung bình dưới 120h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif thoi_gian_giao_tb >= 120:
            return 'Trung bình thời gian giao hàng lớn hơn hoặc bằng 120h'

    # group 3 (Nội Tỉnh)
    if loai_van_chuyen in ['Nội Thành Tỉnh', 'Ngoại Thành Tỉnh', 'Nội Thành Tp.HCM - HN', 'Ngoại Thành Tp.HCM - HN']:
        # thời gian giao trung bình < 48h
        if (tong_don > 30) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 30 đơn'
        elif (tong_don > 20) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 48):
            return 'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # thời gian giao trung bình < 72h
        elif (tong_don > 30) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn'
        elif (tong_don > 20) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn'
        elif (tong_don > 10) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn'
        elif (tong_don > 5) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn'
        elif (tong_don <= 5) and (thoi_gian_giao_tb < 72):
            return 'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn'
        # trễ
        elif (tong_don > 3) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn'
        elif (tong_don <= 3) and (thoi_gian_giao_tb < 96):
            return 'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn'
        elif thoi_gian_giao_tb >= 96:
            return 'Trung bình thời gian giao hàng lớn hơn hoặc bằng 96h'


def transform_data_thoi_gian_giao_hang_toan_trinh():
    # Đọc thông tin giao dịch valid
    giao_dich_valid = pd.read_parquet(ROOT_PATH + '/processed_data/giao_dich_combine_valid.parquet')

    # Xử lý data
    giao_dich_thanh_cong = giao_dich_valid[giao_dich_valid['order_status'].isin([
        'Giao hàng thành công',
        'Đã hoàn thành',
        'Delivered | Giao hàng thành công',
        'Thành công - Phát thành công',
        'Đã giao hàng/Chưa đối soát',
        'Đã đối soát',
    ])]

    giao_dich_thanh_cong = giao_dich_thanh_cong.loc[
        giao_dich_thanh_cong['finished_at'].notna() & giao_dich_thanh_cong['carrier_created_at'].notna()]
    giao_dich_thanh_cong['delivery_time_h'] = (giao_dich_thanh_cong['finished_at'] - giao_dich_thanh_cong[
        'carrier_created_at']).dt.total_seconds() / 60 / 60

    # Transform bảng
    giao_dich_thanh_cong_agg = (
        giao_dich_thanh_cong
        .groupby(['receiver_province', 'receiver_district', 'carrier', 'order_type'])
        .agg(total_order=('delivery_time_h', 'count'), delivery_time_mean_h=('delivery_time_h', 'mean'))
        .reset_index()
    )

    giao_dich_thanh_cong_agg['status'] = (
        giao_dich_thanh_cong_agg.apply(
            lambda x: score_thoi_gian_giao_hang(x['total_order'], x['delivery_time_mean_h'], x['order_type']), axis=1
        )
    )

    cross_df = (
        PROVINCE_MAPPING_DISTRICT_CROSS_CARRIER_DF.merge(
            pd.DataFrame(
                data={'order_type': [
                    'Nội Thành Tỉnh', 'Ngoại Thành Tỉnh',
                    'Nội Thành Tp.HCM - HN', 'Ngoại Thành Tp.HCM - HN',
                    'Nội Miền', 'Cận Miền', 'Cách Miền'
                ]}
            ), how='cross'
        )
    )
    giao_dich_thanh_cong_agg = (
        cross_df.merge(
            giao_dich_thanh_cong_agg,
            on=['receiver_province', 'receiver_district', 'carrier', 'order_type'], how='left'
        )
    )

    giao_dich_thanh_cong_agg['total_order'] = giao_dich_thanh_cong_agg['total_order'].fillna(0).astype(int)
    giao_dich_thanh_cong_agg['delivery_time_mean_h'] = np.round(giao_dich_thanh_cong_agg['delivery_time_mean_h'].fillna(0), 2)
    giao_dich_thanh_cong_agg['status'] = giao_dich_thanh_cong_agg['status'].fillna('Không có thông tin')

    giao_dich_thanh_cong_agg['score'] = (
        giao_dich_thanh_cong_agg.apply(
            lambda x: TRONG_SO['Thời gian giao hàng']['Phân loại'][x['order_type']][x['status']], axis=1
        )
    )
    giao_dich_thanh_cong_agg['criteria'] = 'Thời gian giao hàng'
    giao_dich_thanh_cong_agg['criteria_weight'] = TRONG_SO['Thời gian giao hàng']['Tiêu chí']

    giao_dich_thanh_cong_agg = giao_dich_thanh_cong_agg[[
        'receiver_province', 'receiver_district', 'carrier', 'order_type',
        'total_order', 'delivery_time_mean_h', 'status',
        'score', 'criteria', 'criteria_weight',
    ]]

    # Check data thời gian giao hàng toàn trình
    assert giao_dich_thanh_cong_agg.isna().sum().all() == 0, 'Transform data không chính xác'

    return giao_dich_thanh_cong_agg
