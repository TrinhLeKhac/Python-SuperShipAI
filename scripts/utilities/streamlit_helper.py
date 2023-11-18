from scripts.utilities.helper import *


@st.cache_data
def st_get_data_api_final():
    return pd.read_parquet(ROOT_PATH + '/output/data_check_output_backup.parquet')


@st.cache_data
def st_get_province_mapping_district():
    return pd.read_parquet(ROOT_PATH + '/input/province_mapping_district.parquet')


# function support streamlit render
def save_uploaded_file(uploaded_file, folder):
    with open(os.path.join(folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success("Saved File:{} to {}".format(folder, uploaded_file.name))
