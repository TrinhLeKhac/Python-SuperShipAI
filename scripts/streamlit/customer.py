from scripts.streamlit.streamlit_helper import *
from scripts.api.result import execute_query


def create_customer_tab():
    toggle = st.toggle('Thông tin', key='toggle_customer_tab')
    if toggle:
        st.markdown(
            """
            **Show thông tin trả về từ API**
            * Thông tin input:
                * Mã đơn hàng (Optional)
                * Tỉnh thành giao hàng
                * Quận huyện giao hàng
                * Tỉnh thành nhận hàng
                * Quận huyện nhận hàng
                * Hình thức vận chuyển
                * Khối lượng
            * Thông tin output:
                * Tiền cước vận chuyển
                * Các đánh giá liên quan tới nhà vận chuyển ở khu vực nhận hàng
        """
        )
    # Show output API
    province_district_df = st_get_province_mapping_district()
    with st.container():
        sender_province, sender_district = st.columns(2)
        receiver_province, receiver_district = st.columns(2)
        with sender_province:
            opt_sender_province = st.selectbox(
                "Chọn tỉnh thành giao hàng",
                options=(province_district_df['province'].unique().tolist()),
                key='sender_province',
            )
            sender_province_code = (
                province_district_df.loc[
                    province_district_df['province'] == opt_sender_province
                ]['province_id'].values[0]
            )
        with sender_district:
            opt_sender_district = st.selectbox(
                "Chọn quận huyện giao hàng",
                options=(
                    province_district_df.loc[
                        province_district_df['province'] == opt_sender_province]
                    ['district'].unique()),
                key='sender_district',
            )
            sender_district_code = (
                province_district_df.loc[
                    province_district_df['district'] == opt_sender_district
                ]['district_id'].values[0]
            )
        with receiver_province:
            opt_receiver_province = st.selectbox(
                "Chọn tỉnh thành nhận hàng",
                options=(province_district_df['province'].unique().tolist()),
                key='receiver_province',
            )
            receiver_province_code = (
                province_district_df.loc[
                    province_district_df['province'] == opt_receiver_province
                ]['province_id'].values[0]
            )
        with receiver_district:
            opt_receiver_district = st.selectbox(
                "Chọn quận huyện nhận hàng",
                options=(
                    province_district_df.loc[
                        province_district_df['province'] == opt_receiver_province]
                    ['district'].unique()),
                key='receiver_district',
            )
            receiver_district_code = (
                province_district_df.loc[
                    province_district_df['district'] == opt_receiver_district
                ]['district_id'].values[0]
            )

        opt_pickup, opt_weight = st.columns(2)
        with opt_pickup:
            pickup = st.selectbox(
                "Chọn loại vận chuyển",
                options=('Lấy Tận Nơi', 'Gửi Bưu Cục'),
                key='delivery_type'
            )
            if pickup == 'Lấy Tận Nơi':
                pickup = '0'
            elif pickup == 'Gửi Bưu Cục':
                pickup = '1'

        with opt_weight:
            weight = st.number_input('Nhập khối lượng đơn (<= 50,000g): ', key='weight')
        output_button = st.button('Xem kết quả', type="primary")

        if output_button:
            result_df = get_st_dataframe_from_db(
                sender_province_code, sender_district_code,
                receiver_province_code, receiver_district_code,
                weight, pickup
            )
            # print(result_df)
            if len(result_df) > 0:
                st.dataframe(
                    result_df,
                    column_config={
                        "carrier_id": "ID Nhà vận chuyển",
                        'route_type': "ID Loại vận chuyển (Hệ thống)",
                        'price': "Tiền cước",
                        'status': "Trạng thái NVC",
                        'description': "Mô tả",
                        'time_data': "Thời gian giao dự kiến",
                        'time_display': "Thời gian giao dự kiến (hiển thị)",
                        'rate': 'Tỉ lệ giao thành công',
                        'for_shop': "ID NVC tốt nhất cho Khách hàng",
                        'for_partner': "ID NVC tốt nhất cho Đối tác",
                        'price_ranking': "Ranking NVC (tiêu chí Rẻ nhất)",
                        'speed_ranking': "Ranking NVC (tiêu chí Nhanh nhất)",
                        'score_ranking': "Ranking NVC (Tiêu chí Chất lượng nhất)",
                        "score": "Score đánh giá",
                        "star": st.column_config.NumberColumn(
                            "Phân loại",
                            format="%.1f ⭐",
                        ),
                    },
                    hide_index=True,
                )
            else:
                st.error('Có lỗi xảy ra')