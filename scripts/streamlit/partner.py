from scripts.streamlit.streamlit_helper import *
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def draw_fee_error(total_analyze_df):
    st.markdown(
        """
        **Chart này mô tả tương quan giữa đường chi phí và lỗi khi thay đổi score**
        * Thông tin:
            * Đường chi phí tỉ lệ thuận với score 
            * Số lỗi phát sinh tỉ lệ nghịch với score
            * Điểm tối ưu là giao nhau giữa 2 đường chi phí và lỗi
    """
    )
    viz_df = total_analyze_df[['score', 'monetary', 'total_error']].drop_duplicates()

    # subfig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = px.line(
        viz_df,
        x='score',
        y='monetary',
        title='',
    )
    fig.update_traces(line=dict(color='seagreen'), showlegend=True)

    fig2 = px.line(viz_df, x='score', y='total_error')
    # Change the axis for fig2
    fig2.update_traces(yaxis='y2', line=dict(color='indianred'), showlegend=True)

    # Add the figs to the subplot figure
    # subfig.add_traces(fig.data + fig2.data)

    fig.add_trace(fig2.data[0])
    fig.update_layout(
        xaxis=dict(title='Score'),
        yaxis=dict(title='Tổng tiền cước'),
        yaxis2=dict(title='Tổng lỗi', overlaying='y', side='right'),
    )
    st.plotly_chart(fig)


def score_sidebar(total_analyze_df):
    st.markdown(
        """
        **Kéo thanh slidebar để chọn ngưỡng score mong muốn**
        * Thông tin:
            * Score được tính theo công thức: score = 0.5 + slidebar_value * 0.05 
    """
    )
    slider_num = st.slider("", min_value=1, max_value=100, value=100)

    _th = 0.5 + slider_num * 0.005
    st.markdown('Score: ' + str(_th)[:5])

    viz_df = total_analyze_df[total_analyze_df['score'] == _th]
    st.markdown('Tổng số đơn trên ngưỡng lọc: ' + str(viz_df['n_good_order'].values[0]))
    st.markdown('Tổng số đơn dưới ngưỡng lọc: ' + str(viz_df['n_bad_order'].values[0]))
    return _th


def error_by_score(total_analyze_df, threshold=0.75):
    viz_df = total_analyze_df[total_analyze_df['score'] == threshold]
    viz_df1 = viz_df.groupby('carrier')['n_errors'].sum().reset_index()
    fig = px.bar(viz_df1, x='carrier', y='n_errors', color='carrier', text='n_errors', template='seaborn')
    fig.update_layout(
        xaxis=dict(title='Nhà vận chuyển', categoryorder='total descending'),
        yaxis=dict(title='Tổng số lỗi'),
        legend=dict(
            orientation='h',
            y=1.12,
            x=0.15
        ),
        legend_title='',
        height=500,
        # width=800
    )
    return fig


def detail_error_by_carrier(total_analyze_df, opt_carrier, type_viz='error_type', x_legend_position=0.4,
                            threshold=0.75):
    viz_df = total_analyze_df[
        (total_analyze_df['score'] == threshold)
        & (total_analyze_df['carrier'] == opt_carrier)
        ].groupby(type_viz)['n_errors'].sum().reset_index()
    fig = px.bar(viz_df, x=type_viz, y='n_errors', color=type_viz, text='n_errors', template='seaborn')
    fig.update_layout(
        xaxis=dict(title='', tickvals=[], categoryorder='total descending'),
        yaxis=dict(title='Số lỗi theo category'),
        legend=dict(
            orientation='h',
            y=1.12,
            x=x_legend_position,
        ),
        legend_title='',
        height=500,
        # width=800,
    )
    return fig


def analyze_by_carrier(total_analyze_df, type_viz='n_orders', threshold=0.75):
    viz_df = total_analyze_df[total_analyze_df['score'] == threshold]
    categories = sorted(viz_df['carrier'].unique())
    groups = sorted(viz_df['quality'].unique())

    fig = go.Figure()
    bar_width = 0.4
    for i, group in enumerate(groups):
        group_data = viz_df[viz_df['quality'] == group]
        positions = [pos + i * bar_width for pos in range(len(categories))]
        fig.add_trace(go.Bar(x=positions, y=group_data[type_viz], name=group, width=bar_width))

    if type_viz == 'n_orders':
        y_title = 'Số đơn hàng'
    elif type_viz == 'monetary':
        y_title = 'Số tiền'

    fig.update_layout(
        xaxis=dict(tickvals=[pos + (len(groups) - 1) * bar_width / 2 for pos in range(len(categories))],
                   ticktext=categories, title='Nhà vận chuyển', categoryorder='total descending'),
        yaxis=dict(title=y_title),
        barmode='group',
        legend=dict(
            orientation='h',
            y=1.12,
            x=0.4
        ),
        legend_title='',
        height=500,
        # width=800,
    )
    return fig


def create_partner_tab():
    interactive = st.container()
    with interactive:
        # 1. Toggle thông tin
        _, toggle_div, _ = st.columns([1, 2, 1])
        with toggle_div:
            toggle = st.toggle('Thông tin', key='toggle_partner_tab')
            if toggle:
                st.markdown(
                    """
                    **Modules này hỗ trợ chọn score tối ưu vận chuyển một cách trực quan dựa vào thống kê lỗi và chi phí**
                    * Thông tin:
                        * Chart tương quan chi phí - lỗi.
                        * Chart hiển thị lỗi chi tiết của NVC.
                    * Tiêu chí chọn đơn:
                        * Nếu tồn tại ít nhất 1 NVC có điểm >= ngưỡng, chọn NVC có cước phí nhỏ nhất.
                        * Nếu tất cả các NVC có điểm < ngưỡng, chọn NVC có score cao nhất.
                """
                )

        total_analyze_df1, total_analyze_df2 = st_get_data_viz()

        # 2. Tương quan chi phí - lỗi
        _, fee_err_div, _ = st.columns([1, 2, 1])
        with fee_err_div:
            draw_fee_error(total_analyze_df1)
        st.markdown("---")

        # 3.Điều chỉnh theo score
        _, score_div, _ = st.columns([1, 4, 1])
        with score_div:
            _th = score_sidebar(total_analyze_df1)
        st.markdown("---")

        # 4. Chọn NVC
        info_err_div, _, select_div = st.columns([2, 1, 1])
        with info_err_div:
            st.markdown(
                """
                **Thống kê lỗi của NVC theo từng ngưỡng chọn score**
                * Thông tin:
                    * Chart bên trái: Tổng số lỗi của NVC.
                    * Chart bên phải: Phân bố chi tiết lỗi của 1 NVC theo loại vận chuyển hoặc category lỗi.
            """
            )
        with select_div:
            viz_df = total_analyze_df1[total_analyze_df1['score'] == _th]
            opt_carrier = st.selectbox(
                "Chọn nhà vận chuyển",
                options=list(viz_df['carrier'].unique()),
                key='carrier',
            )
            opt_type_viz = st.selectbox(
                "Thống kê theo",
                options=['Category lỗi', 'Loại vận chuyển'],
                key='type_viz',
            )

        error_by_score_div, _, detail_error_by_carrier_div = st.columns([4, 1, 5])

        fig_error_by_score = error_by_score(total_analyze_df1, threshold=_th)

        if opt_type_viz == 'Category lỗi':
            fig_detail_error_by_score = detail_error_by_carrier(
                total_analyze_df1, opt_carrier,
                type_viz='error_type', x_legend_position=0.4, threshold=_th
            )
        elif opt_type_viz == 'Loại vận chuyển':
            fig_detail_error_by_score = detail_error_by_carrier(
                total_analyze_df1, opt_carrier,
                type_viz='order_type', x_legend_position=0.2, threshold=_th)

        fig_detail_error_by_score.update_layout(yaxis=dict(anchor='x'), barmode='stack')

        # 5. Thống kê tổng lỗi NVC theo score
        with error_by_score_div:
            st.plotly_chart(fig_error_by_score)

        # 6. Thống kê lỗi chi tiết của NVC theo score
        with detail_error_by_carrier_div:
            st.plotly_chart(fig_detail_error_by_score)

        st.markdown("---")

        _, info_order_fee_div, _ = st.columns([1, 2, 1])
        with info_order_fee_div:
            st.markdown(
                """
                **Thống kê chi tiết lượng đơn hàng trên và dưới ngưỡng lọc score của từng NVC**
                * Thông tin:
                    * Chart bên trái: Phân bố đơn hàng.
                    * Chart bên phải: Phân bố cước phí.
            """
            )
        analyze_by_order_div, _, analyze_by_money_div = st.columns([4, 1, 4])

        fig_order_by_carrier = analyze_by_carrier(total_analyze_df2, type_viz='n_orders', threshold=_th)
        fig_monatary_by_carrier = analyze_by_carrier(total_analyze_df2, type_viz='monetary', threshold=_th)
        fig_monatary_by_carrier.update_layout(yaxis=dict(anchor='x'), barmode='stack')

        # 7. Thống kê đơn theo nhà vận chuyển
        with analyze_by_order_div:
            st.plotly_chart(fig_order_by_carrier)

        # 8. Thống kê tiền theo nhà vận chuyển
        with analyze_by_money_div:
            st.plotly_chart(fig_monatary_by_carrier)
