import sys
from pathlib import Path

ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)
from scripts.streamlit.manual import create_manual_tab
from scripts.streamlit.customer import create_customer_tab
from scripts.streamlit.partner import create_partner_tab
from scripts.output.out_data_final import *

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Tối ưu vận chuyển (SuperShipAI)")

tab1, tab2, tab3 = st.tabs(["Manual", "Customer", "Partner"])
with tab1:
    create_manual_tab()
with tab2:
    create_customer_tab()
with tab3:
    create_partner_tab()

# pages = ['Manual', 'Customer', 'Partner']
# selected_page = st.sidebar.selectbox("Select a page", pages)
#
# if selected_page == 'Manual':
#     create_manual_tab()
# elif selected_page == 'Customer':
#     create_customer_tab()
# elif selected_page == 'Partner':
#     create_partner_tab()
