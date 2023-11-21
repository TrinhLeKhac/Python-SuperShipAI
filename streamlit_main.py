import sys
from pathlib import Path
ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)

from scripts.utilities.streamlit_helper import *
from scripts.processing.total_processing import total_processing
from scripts.api.out_data_final import *

st.title("Tối ưu vận chuyển (SuperShipAI)")

tab1, tab2, tab3 = st.tabs(["Manual", "Customer", "Partner"])
with tab1:
    option = st.selectbox(
        "Lấy thông tin cần thiết cho quá trình tính toán bằng cách nào",
        ("File Excel", "API")
    )

    if 'File Excel' in option:
        toggle1 = st.toggle('Hướng dẫn')
        if toggle1:
            st.markdown(
                """
                **Import đầy đủ các files chứa các thông tin cần thiết sau**
                - Bảng cước phí
                - Đánh giá chất lượng nội bộ nhà vận chuyển
                - Đánh giá ZNS từ khách hàng
                - Thông tin bưu cục nhà vận chuyển
                - Thông tin vùng ngưng giao nhận
                - Phân vùng quận huyện theo nhà vận chuyển
                - Thông tin vận chuyển
                - Khối lượng đơn
            """
            )
        # upload_file_excel()

        with st.expander("Files cần upload"):
            cuoc_phi_file = st.file_uploader("1.Bảng Cước Phí")
            if cuoc_phi_file is not None:
                save_uploaded_file(cuoc_phi_file, "input")

            chat_lượng_noi_bo_files = st.file_uploader("2.Chất Lượng Nội Bộ", accept_multiple_files=True)
            if chat_lượng_noi_bo_files is not None:
                for file in chat_lượng_noi_bo_files:
                    save_uploaded_file(file, "input")

            zns_file = st.file_uploader("3.Đánh giá ZNS")
            if zns_file is not None:
                save_uploaded_file(zns_file, "input")

            kho_giao_nhan_files = st.file_uploader("4.Bưu Cục", accept_multiple_files=True)
            if kho_giao_nhan_files is not None:
                for file in kho_giao_nhan_files:
                    save_uploaded_file(file, "input")

            ngung_giao_nhan_file = st.file_uploader("5.Ngưng giao nhận")
            if ngung_giao_nhan_file is not None:
                save_uploaded_file(ngung_giao_nhan_file, "input")

            phan_vung_nvc_file = st.file_uploader("6.Phân Vùng Ghép SuperShip")
            if phan_vung_nvc_file is not None:
                save_uploaded_file(phan_vung_nvc_file, "input")

            giao_dich_nvc_file = st.file_uploader("7.Giao Dịch Nhà Vận Chuyển")
            if giao_dich_nvc_file is not None:
                save_uploaded_file(giao_dich_nvc_file, "input")

            don_co_khoi_luong_file = st.file_uploader("8.Đơn có khối lượng")
            if don_co_khoi_luong_file is not None:
                save_uploaded_file(don_co_khoi_luong_file, "input")

        processing_button = st.button('Xử lý dữ liệu', type="primary")
        if 'processing_button_state' not in st.session_state:
            st.session_state['processing_button_state'] = False
        if processing_button and not st.session_state['processing_button_state']:
            try:
                start_processing = time()
                with st.spinner('Đang xử lý...'):
                    total_processing()
                stop_processing = time()
                st.session_state['processing_button_state'] = True
                st.success("Done")
                st.info('Thời gian xử lý: ' + convert_time_m_s(stop_processing, start_processing))
            except:
                st.error("Có lỗi xảy ra")
        if processing_button and st.session_state['processing_button_state']:
            st.info('Đã xử lý xong dữ liệu')

        out_data_api_button = st.button('Xuất data API', type="primary")
        if 'api_button_state' not in st.session_state:
            st.session_state['api_button_state'] = False
        if out_data_api_button and not st.session_state['api_button_state']:
            try:
                start = time()
                with st.spinner('Đang xử lý...'):
                    out_data_api()
                stop = time()
                st.session_state['api_button_state'] = True
                st.success("Done")
                st.info('Thời gian xử lý: ' + convert_time_m_s(stop, start))
            except:
                st.error("Có lỗi xảy ra")
        if out_data_api_button and st.session_state['api_button_state']:
            st.info('Đã có kết quả API')

if os.path.exists(ROOT_PATH + '/output/data_api.parquet'):
    with tab2:
        toggle2 = st.toggle('Thông tin')
        if toggle2:
            st.markdown(
                """
                **Show thông tin trả về từ API**
                * Thông tin input:
                    * Tỉnh thành giao hàng
                    * Quận huyện giao hàng
                    * Mã đơn hàng
                    * ID nhà vận chuyển
                    * Khối lượng
                    * Loại vận chuyển
                * Thông tin output:
                    * Tiền cước
                    * Score đánh giá khách hàng
                    * Stars
                    * Notification
            """
            )
        # Show output API
        pro_dis_df = st_get_province_mapping_district()
        with st.container():
            order_code = st.text_input('Nhập mã đơn hàng: ')
            sender_province, sender_district = st.columns(2)
            receiver_province, receiver_district = st.columns(2)
            with sender_province:
                opt_sender_province = st.selectbox(
                    "Chọn tỉnh thành giao hàng",
                    options=(pro_dis_df['province'].unique().tolist()),
                    key='sender_province',
                )
                opt_sender_province_code = pro_dis_df.loc[pro_dis_df['province'] == opt_sender_province]['province_code'].values[0]
            with sender_district:
                opt_sender_district = st.selectbox(
                    "Chọn quận huyện giao hàng",
                    options=(
                        pro_dis_df.loc[
                            pro_dis_df['province'] == opt_sender_province]
                        ['district'].unique()),
                    key='sender_district',
                )
                opt_sender_district_code = pro_dis_df.loc[pro_dis_df['district'] == opt_sender_district]['district_code'].values[0]
            with receiver_province:
                opt_receiver_province = st.selectbox(
                    "Chọn tỉnh thành nhận hàng",
                    options=(pro_dis_df['province'].unique().tolist()),
                    key='receiver_province',
                )
                opt_receiver_province_code = pro_dis_df.loc[pro_dis_df['province'] == opt_receiver_province]['province_code'].values[0]
            with receiver_district:
                opt_receiver_district = st.selectbox(
                    "Chọn quận huyện nhận hàng",
                    options=(
                        pro_dis_df.loc[
                            pro_dis_df['province'] == opt_receiver_province]
                        ['district'].unique()),
                    key='receiver_district',
                )
                opt_receiver_district_code = pro_dis_df.loc[pro_dis_df['district'] == opt_receiver_district]['district_code'].values[0]

            carrier_id, delivery_type = st.columns(2)
            with carrier_id:
                opt_carriers = st.multiselect(
                    "Chọn nhà vận chuyển",
                    options=('GHTK', 'GHN', 'Viettel Post', 'BEST Express', 'Ninja Van', 'SPX Express'),
                    key='carrier_id'
                )
                # option_carriers_id = [int(re.findall(r'\d+', opt)[0]) for opt in opt_carriers]
            with delivery_type:
                opt_delivery_type = st.selectbox(
                    "Chọn loại vận chuyển",
                    options=('Nội Miền', 'Cận Miền', 'Cách Miền', 'Nội Thành Tỉnh', 'Ngoại Thành Tỉnh', 'Nội Thành Tp.HCM - HN', 'Ngoại Thành Tp.HCM - HN'),
                    key='pickup_type'
                )
            weight = st.number_input('Nhập khối lượng đơn (<= 50,000g): ', key='weight')

            if order_code != '' and (weight > 0):
                df_input = pd.DataFrame(data={
                    'order_code': [order_code],
                    'weight': [weight],
                    'pickup_type': [opt_delivery_type],
                    'sender_province_code': [opt_sender_province_code],
                    'sender_district_code': [opt_sender_district_code],
                    'receiver_province_code': [opt_receiver_province_code],
                    'receiver_district_code': [opt_receiver_district_code],
                })

                df_st_output = out_data_final(df_input, carriers=opt_carriers, show_logs=False)
                df_st_output['speed_ranking'] = df_st_output['time_data'].rank(
                    method="dense", ascending=True)
                df_st_output['speed_ranking'] = df_st_output['speed_ranking'].astype(int)

                df_st_output['score_ranking'] = df_st_output["score"].rank(
                    method="dense", ascending=False)
                df_st_output['score_ranking'] = df_st_output['score_ranking'].astype(int)

                customer_best_carrier_id = df_st_output['for_fshop'].values[0]

                df_st_output = df_st_output[[
                    'order_code', 'carrier_id', 'new_type', 'route_type',
                    'price', 'status', 'description',
                    'time_data', 'time_display', 'rate',
                    # 'for_fshop', 'for_partner',
                    'price_ranking', 'speed_ranking', 'score_ranking',
                    'score', 'stars',
                ]]

                if len(df_st_output) > 0:
                    st.dataframe(
                        df_st_output,
                        column_config={
                            'order_code': "Mã đơn hàng",
                            "carrier_id": "ID của Nhà vận chuyển",
                            'new_type': "ID Loại vận chuyển",
                            'route_type': "ID Loại vận chuyển (Hệ thống)",
                            'price': "Tiền cước",
                            'status': "Trạng thái nhà vận chuyển",
                            'description': "Trạng thái nhà vận chuyển (comment)",
                            'time_data': "Thời gian giao dự kiến (dạng thập phân)",
                            'time_display': "Thời gian giao dự kiến",
                            'rate': 'Tỉ lệ giao thành công',
                            # 'for_shop': "ID NVC tốt nhất cho Khách hàng",
                            # 'for_partner': "ID NVC tốt nhất cho Đối tác",
                            'price_ranking': "Ranking NVC (tiêu chí Rẻ nhất)",
                            'speed_ranking': "Ranking NVC (tiêu chí Nhanh nhất)",
                            'score_ranking': "Ranking NVC (Tiêu chí Chất lượng nhất)",
                            "score": "Score đánh giá",
                            "stars": st.column_config.NumberColumn(
                                "Phân loại",
                                format="%.1f ⭐",
                            ),
                        },
                        hide_index=True,
                    )
                else:
                    st.error('Tập dữ liệu quá khứ (dùng để tính toán) chưa có thông tin ', icon="🚨")

                st.info('Nhà vận chuyển tốt nhất: ' + MAPPING_ID_CARRIER[customer_best_carrier_id])
