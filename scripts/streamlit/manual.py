from scripts.output.out_data_api import out_data_api
from scripts.processing.total_processing import total_processing
from scripts.streamlit.streamlit_helper import *


def create_manual_tab():
    option = st.selectbox(
        "Lấy thông tin cần thiết cho quá trình tính toán bằng cách nào",
        ("File Excel", "API")
    )

    if 'File Excel' in option:
        toggle = st.toggle('Hướng dẫn', key='toggle_manual_tab')
        if toggle:
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

        with st.expander("Files cần upload"):
            cuoc_phi_file = st.file_uploader("1.Bảng Cước Phí")
            if cuoc_phi_file is not None:
                save_uploaded_file(cuoc_phi_file, "input")

            chat_luong_noi_bo_files = st.file_uploader("2.Chất Lượng Nội Bộ", accept_multiple_files=True)
            if chat_luong_noi_bo_files is not None:
                for file in chat_luong_noi_bo_files:
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