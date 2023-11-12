import streamlit as st
import os
import pandas as pd


@st.cache_data
def st_get_data_api_final():
    return pd.read_parquet('./output/data_check_output_backup.parquet')


@st.cache_data
def st_get_province_mapping_district():
    return pd.read_parquet('./processed_data/province_mapping_district.parquet')


# function support streamlit render
def save_uploaded_file(uploaded_file, folder):
    with open(os.path.join(folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success("Saved File:{} to {}".format(folder, uploaded_file.name))


@st.cache_data(experimental_allow_widgets=True)
def upload_file_excel():
    with st.expander("File cần upload"):
        cuoc_phi_file = st.file_uploader("1.Bảng Cước Phí")
        if cuoc_phi_file is not None:
            print('OK')
            save_uploaded_file(cuoc_phi_file, "input")
        else:
            print('Not OK')

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
