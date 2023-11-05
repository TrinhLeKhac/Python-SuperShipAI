from scripts.transform.chat_luong_noi_bo import transform_data_chat_luong_noi_bo
from scripts.transform.danh_gia_zns import transform_data_danh_gia_zns
from scripts.transform.kho_giao_nhan import transform_data_kho_giao_nhan
from scripts.transform.ngung_giao_nhan import transform_data_ngung_giao_nhan
from scripts.transform.thoi_gian_giao_hang_toan_trinh import transform_data_thoi_gian_giao_hang_toan_trinh
from scripts.transform.ti_le_giao_hang import transform_data_ti_le_giao_hang
from scripts.transform.tien_giao_dich import transform_data_tien_giao_dich
from scripts.utilities.helper import *
from scripts.utilities.config import *


def total_transform():
    print('1. Transform data kho giao nhận...')
    ngung_giao_nhan = transform_data_ngung_giao_nhan()
    print('Done\n')

    print('2. Transform data đánh giá ZNS...')
    danh_gia_zns = transform_data_danh_gia_zns()
    print('Done\n')

    print('3. Transform data tỉ lệ giao hàng...')
    ti_le_giao_hang = transform_data_ti_le_giao_hang()
    print('>>> Done\n')

    print('4. Transform data chất lượng nội bộ...')
    chat_luong_noi_bo = transform_data_chat_luong_noi_bo()
    print('>>> Done\n')

    print('5. Transform data thời gian giao hàng toàn trình...')
    thoi_gian_giao_hang = transform_data_thoi_gian_giao_hang_toan_trinh()
    print('>>> Done\n')

    print('6. Transform data kho giao nhận...')
    kho_giao_nhan = transform_data_kho_giao_nhan()
    print('>>> Done\n')

    # print('7. Transform data tiền giao dịch...')
    # tien_giao_dich = transform_data_tien_giao_dich()
    # print('>>> Done\n')

    return (
        ngung_giao_nhan, danh_gia_zns,
        ti_le_giao_hang, chat_luong_noi_bo,
        thoi_gian_giao_hang, kho_giao_nhan,
        # tien_giao_dich
    )


if __name__ == '__main__':
    total_transform()
