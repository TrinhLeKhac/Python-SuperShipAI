from scripts.utilities.streamlit_helper import *
from scripts.processing.total_processing import total_processing
from scripts.api.out_data_api import *
from scripts.api.out_data_final import *

st.title("Tối ưu vận chuyển (SuperShipAI)")

tab1, tab2, tab3 = st.tabs(["Manual", "Auto", "Output"])
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

        out_data_to_check_button = st.button('Xuất data kiểm tra', type="primary")
        if 'check_button_state' not in st.session_state:
            st.session_state['check_button_state'] = False
        if out_data_to_check_button and not st.session_state['check_button_state']:
            try:
                start = time()
                with st.spinner('Đang xử lý...'):
                    out_data_final(input_df=None)
                stop = time()
                st.session_state['check_button_state'] = True
                st.success("Done")
                st.info('Thời gian xử lý: ' + convert_time_m_s(stop, start))
            except:
                st.error("Có lỗi xảy ra")
        if out_data_to_check_button and st.session_state['check_button_state']:
            st.info('Đã có kết quả API')

if os.path.exists('./output/data_check_output.parquet'):
    with tab3:
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
        df_data_final = st_get_data_api_final()
        with st.container():
            order_id = st.text_input('Nhập mã đơn hàng: ')
            if order_id in df_data_final['ma_don_hang'].unique().tolist():
                st.warning('Đơn hàng cũ')
                df_st_output = df_data_final.loc[
                    (df_data_final['order_id'] == order_id)
                ]
                df_st_output = df_st_output[
                    ['order_id', 'carrier_id', 'carrier', 'status_carrier_comment', 'service_fee', 'estimate_delivery_time', 'score', 'stars']
                ]
                st.markdown("""
                <style>
                table {
                tr:first-child
                    {
                    background-color: #3944BC;
                    }
                }
                </style>
                """, unsafe_allow_html=True)

                st.dataframe(
                    df_st_output,
                    column_config={
                        'order_id': 'Mã đơn hàng',
                        "carrier_id": "ID Nhà vận chuyển",
                        "carrier": "Nhà vận chuyển",
                        "status_carrier_comment": "Trạng thái nhà vận chuyển",
                        "service_fee": "Tiền cước",
                        "estimate_delivery_time": "Thời gian giao dự kiến",
                        "score": "Score đánh giá",
                        "stars": st.column_config.NumberColumn(
                            "Phân loại",
                            format="%d ⭐",
                        ),
                    },
                    hide_index=True,
                )
            else:
                sender_province, sender_district = st.columns(2)
                receiver_province, receiver_district = st.columns(2)
                province_district_norm_df = st_get_province_mapping_district()
                with sender_province:
                    opt_sender_province = st.selectbox(
                        "Chọn tỉnh thành giao hàng (ID)",
                        options=(province_district_norm_df['province_id'].unique().tolist()),
                        key='province_id',
                    )
                with sender_district:
                    opt_sender_district = st.selectbox(
                        "Chọn quận huyện giao hàng (ID)",
                        options=(
                            province_district_norm_df.loc[
                                province_district_norm_df['province_id'] == opt_sender_province]
                            ['district_id'].unique()),
                        key='district_id',
                    )
                with receiver_province:
                    opt_receiver_province = st.selectbox(
                        "Chọn tỉnh thành giao hàng (ID)",
                        options=(province_district_norm_df['province_id'].unique().tolist()),
                        key='province_id',
                    )
                with receiver_district:
                    opt_receiver_district = st.selectbox(
                        "Chọn quận huyện giao hàng (ID)",
                        options=(
                            province_district_norm_df.loc[
                                province_district_norm_df['province_id'] == opt_receiver_province]
                            ['district_id'].unique()),
                        key='district_id',
                    )

                carrier_id, delivery_type = st.columns(2)
                with carrier_id:
                    option_carriers = st.multiselect(
                        "Chọn nhà vận chuyển",
                        options=( '1 (GHTK)', '2 (GHN)', '4 (VTP)', '6 (BEST)', '7 (NJV)', '10 (SPX)'),
                        key='carrier_id'
                    )
                    option_carriers_id = [int(re.findall(r'\d+', opt)[0]) for opt in option_carriers]
                with delivery_type:
                    option_delivery_type = st.selectbox(
                        "Chọn loại vận chuyển",
                        options=('Nội Miền', 'Cận Miền', 'Nội Thành Tỉnh', 'Ngoại Thành Tỉnh'),
                        key='delivery_type'
                    )
                weight = st.number_input('Nhập khối lượng đơn (<= 50,000g): ', key='weight')

                if order_id != '' and (weight > 0):
                    print(order_id)
                    print(weight)
                    print(opt_sender_province)
                    print(opt_sender_district)
                    print(opt_receiver_province)
                    print(opt_receiver_district)
                    print(option_carriers)
                    print(option_delivery_type)
                    df_input = pd.DataFrame(data={
                        'order_id': order_id,
                        'weight': weight,
                        'delivery_type': option_delivery_type,
                        'sender_province_id': opt_sender_province,
                        'sender_district_id': opt_sender_district,
                        'receiver_province_id': opt_receiver_province,
                        'receiver_district_id': opt_receiver_district,
                    })
                    df_st_output = out_data_final(df_input)
                    if len(df_st_output) > 0:
                        st.dataframe(
                            df_st_output,
                            column_config={
                                "order_id": "Mã đơn hàng",
                                "carrier_id": "ID Nhà vận chuyển",
                                "carrier": "Nhà vận chuyển",
                                "status_carrier_comment": "Trạng thái nhà vận chuyển",
                                "service_fee": "Tiền cước",
                                "estimate_delivery_time": "Thời gian giao dự kiến",
                                "score": "Score đánh giá",
                                "stars": st.column_config.NumberColumn(
                                    "Phân loại",
                                    format="%d ⭐",
                                ),
                            },
                            hide_index=True,
                        )
                    else:
                        st.error('Tập dữ liệu quá khứ (dùng để tính toán) chưa có thông tin ', icon="🚨")
