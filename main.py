from scripts.utilities.streamlit_helper import *
from scripts.processing.total_processing import total_processing
from scripts.api.generate_data_api import *

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
                    # out_data_api_full()
                    out_data_api()
                stop = time()
                st.session_state['api_button_state'] = True
                st.success("Done")
                st.info('Thời gian xử lý: ' + convert_time_m_s(stop, start))
            except:
                st.error("Có lỗi xảy ra")
        if out_data_api_button and st.session_state['api_button_state']:
            st.info('Đã có kết quả API')

if os.path.exists('./output/data_api.json'):
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
        data_api = get_data_api()
        with st.container():
            ma_don_hang = st.text_input('Nhập mã đơn hàng: ')
            if ma_don_hang in data_api['ma_don_hang'].unique().tolist():
                st.warning('Đơn hàng cũ')
                output_data_api = data_api.loc[
                    (data_api['ma_don_hang'] == ma_don_hang)
                ]
                output_data_api['nvc'] = output_data_api['id_nvc'].map({
                    7: 'Ninja Van',
                    2: 'Giao Hàng Nhanh',
                    6: 'Best',
                    10:'Shopee Express',
                    1: 'Giao Hàng Tiết Kiệm',
                    4: 'Viettel Post',
                    12: 'Tiki Now',
                })
                output_data_api = output_data_api[
                    ['ma_don_hang', 'id_nvc', 'nvc', 'status', 'monetary', 'estimate_delivery_time', 'score', 'stars', 'notification']
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
                    output_data_api,
                    column_config={
                        'ma_don_hang': 'Mã đơn hàng',
                        "id_nvc": "ID Nhà vận chuyển",
                        "nvc": "Nhà vận chuyển",
                        "status": "Trạng thái nhà vận chuyển",
                        "monetary": "Tiền cước",
                        "estimate_delivery_time": "Thời gian giao dự kiến",
                        "score": "Score đánh giá",
                        "stars": st.column_config.NumberColumn(
                            "Phân loại",
                            format="%d ⭐",
                        ),
                        "notification": st.column_config.NumberColumn(
                            "Đánh giá NVC",
                            help="Đánh giá đặc trưng nhà vận chuyển",
                        ),
                    },
                    hide_index=True,
                )
            else:
                tinh_thanh, quan_huyen = st.columns(2)
                province_district_norm_df = get_tinh_thanh_quan_huyen_from_api()
                with tinh_thanh:
                    opt_tinh_thanh = st.selectbox(
                        "Chọn tỉnh thành giao hàng",
                        options=(province_district_norm_df['tinh_thanh'].unique().tolist()),
                        key='tinh_thanh',
                    )
                with quan_huyen:
                    opt_quan_huyen = st.selectbox(
                        "Chọn quận huyện giao hàng",
                        options=(
                            province_district_norm_df.loc[
                                province_district_norm_df['tinh_thanh'] == opt_tinh_thanh]
                            ['quan_huyen'].unique()),
                        key='quan_huyen',
                    )

                id_nvc, loai_van_chuyen = st.columns(2)
                with id_nvc:
                    option_nvc = st.multiselect(
                        "Chọn nhà vận chuyển",
                        options=( '1 (GHTK)', '2 (GHN)', '4 (VTP)', '6 (BEST)', '7 (NJV)', '10 (SPX)', '12 (TIKINOW)'),
                        key='id_nvc'
                    )
                    option_ids_nvc = [int(re.findall(r'\d+', opt)[0]) for opt in option_nvc]
                with loai_van_chuyen:
                    option_vc = st.selectbox(
                        "Chọn loại vận chuyển",
                        options=('Nội Miền', 'Cận Miền', 'Nội Thành Tỉnh', 'Ngoại Thành Tỉnh'),
                        key='loai_van_chuyen'
                    )
                khoi_luong = st.number_input('Nhập khối lượng đơn (<= 50,000g): ', key='khoi_luong')

                if ma_don_hang != '' and (khoi_luong > 0):
                    print(ma_don_hang)
                    print(khoi_luong)
                    print(opt_tinh_thanh)
                    print(opt_quan_huyen)
                    print(option_ids_nvc)
                    print(option_vc)
                    output_data_api = calculate_output_api(data_api, ma_don_hang, opt_tinh_thanh, opt_quan_huyen, option_ids_nvc, option_vc, khoi_luong)
                    output_data_api = calculate_notification(output_data_api)
                    if len(output_data_api) > 0:
                        st.dataframe(
                            output_data_api,
                            column_config={
                                "ma_don_hang": "Mã đơn hàng",
                                "id_nvc": "ID Nhà vận chuyển",
                                "nvc": "Nhà vận chuyển",
                                "status": "Trạng thái nhà vận chuyển",
                                "monetary": "Tiền cước",
                                "estimate_delivery_time": "Thời gian giao dự kiến",
                                "score": "Score đánh giá",
                                "stars": st.column_config.NumberColumn(
                                    "Phân loại",
                                    format="%d ⭐",
                                ),
                                "notification": st.column_config.NumberColumn(
                                    "Đánh giá NVC",
                                    help="Đánh giá đặc trưng nhà vận chuyển",
                                ),
                            },
                            hide_index=True,
                        )
                    else:
                        st.error('Tập dữ liệu quá khứ (dùng để tính toán) chưa có thông tin ', icon="🚨")
