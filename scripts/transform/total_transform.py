import sys
from pathlib import Path
ROOT_PATH = str(Path(__file__).parent.parent.parent)
sys.path.append(ROOT_PATH)

from scripts.transform.chat_luong_noi_bo import transform_data_chat_luong_noi_bo
from scripts.transform.danh_gia_zns import transform_data_danh_gia_zns
from scripts.transform.kho_giao_nhan import transform_data_kho_giao_nhan
from scripts.transform.ngung_giao_nhan import transform_data_ngung_giao_nhan
from scripts.transform.thoi_gian_giao_hang_toan_trinh import transform_data_thoi_gian_giao_hang_toan_trinh
from scripts.transform.ti_le_giao_hang import transform_data_ti_le_giao_hang
from scripts.utilities.helper import *
from scripts.utilities.config import *


def total_transform(show_logs=True):

    if show_logs:
        print('1. Transform data kho giao nhận...')
    ngung_giao_nhan = transform_data_ngung_giao_nhan()
    if show_logs:
        print('Done\n')

    if show_logs:
        print('2. Transform data đánh giá ZNS...')
    danh_gia_zns = transform_data_danh_gia_zns()
    if show_logs:
        print('Done\n')

    if show_logs:
        print('3. Transform data tỉ lệ giao hàng...')
    ti_le_giao_hang = transform_data_ti_le_giao_hang()
    if show_logs:
        print('>>> Done\n')

    if show_logs:
        print('4. Transform data chất lượng nội bộ...')
    chat_luong_noi_bo = transform_data_chat_luong_noi_bo()
    if show_logs:
        print('>>> Done\n')

    if show_logs:
        print('5. Transform data thời gian giao hàng toàn trình...')
    thoi_gian_giao_hang = transform_data_thoi_gian_giao_hang_toan_trinh()
    if show_logs:
        print('>>> Done\n')

    if show_logs:
        print('6. Transform data kho giao nhận...')
    kho_giao_nhan = transform_data_kho_giao_nhan()
    if show_logs:
        print('>>> Done\n')

    return (
        ngung_giao_nhan, danh_gia_zns,
        ti_le_giao_hang, chat_luong_noi_bo,
        thoi_gian_giao_hang, kho_giao_nhan,
    )


if __name__ == '__main__':
    total_transform(show_logs=True)
