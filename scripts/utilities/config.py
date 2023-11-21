from pathlib import Path
ROOT_PATH = str(Path(__file__).parent.parent.parent)

TRONG_SO = {
    'Ngưng giao nhận': {
        'Tiêu chí': 15,
        'Phân loại': {
            'Bình thường': 1,
            'Quá tải': -10,
        },
    },
    'Đánh giá ZNS': {
        'Tiêu chí': 4,
        'Phân loại': {
            'Loại': -10,
            '1 sao & Nhân viên không nhiệt tình': -8,
            'Nhiều hơn 1 lần đánh giá 1 sao': -6,
            'Đánh giá 5 sao trên 95% đơn': 10,
            'Không phát sinh đánh giá 1, 2, 3 sao': 6,
            'Bình thường': 5,
            'Không có thông tin': 5,
        },
    },
    'Tỉ lệ giao hàng': {
        'Tiêu chí': 8,
        'Phân loại': {
            'Tổng đơn hàng từ 30 đơn trở lên và có tỷ lệ giao hàng thành công trên 95%': 10,
            'Tổng đơn hàng từ 20 đơn trở lên và có tỷ lệ giao hàng thành công trên 95%': 9,
            'Tổng đơn hàng từ 10 đơn trở lên và có tỷ lệ giao hàng thành công trên 95%': 8,
            'Tổng đơn hàng từ 30 đơn trở lên và có tỷ lệ giao hàng thành công trên 90%': 8,
            'Tổng đơn hàng từ 20 đơn trở lên và có tỷ lệ giao hàng thành công trên 90%': 7,
            'Tổng đơn hàng từ 10 đơn trở lên và có tỷ lệ giao hàng thành công trên 90%': 6,
            'Tổng đơn hàng từ 5 đơn trở lên và có tỷ lệ giao hàng thành công trên 95%': 5,
            'Tổng đơn hàng từ 5 đơn trở lên và có tỷ lệ giao hàng thành công trên 90%': 4,
            'Tổng đơn hàng từ 5 đơn trở lên và có tỷ lệ giao hàng thành công trên 85%': 3,
            'Tổng đơn hàng từ 5 đơn trở lên và có tỷ lệ giao hàng thành công trên 75%': 2,
            'Tổng đơn hàng từ 5 đơn trở lên và có tỷ lệ giao hàng thành công trên 50%': 1,
            'Tổng đơn hàng từ 10 đơn trở lên và có tỷ lệ hoàn từ 25% trở lên': -10,
            'Tổng đơn hàng từ 4 đơn trở lên và có tỷ lệ hoàn từ 50% trở lên': -10,
            'TOP 10 KHU VỰC có số lượng đơn hàng từ 3 đơn trở lên và có tỷ lệ hoàn hơn 20%': -6,
            'Không có thông tin': 5,
            'Trường hợp khác': 5,
        },
    },
    'Chất lượng nội bộ': {
        'Tiêu chí': 3,
        'Phân loại': {
            'Ninja Van': {
                'Ti lệ trên 95% và tổng số đơn giao hàng trên 100 đơn': 10,
                'Ti lệ trên 95% và tổng số đơn giao hàng dưới 100 đơn': 9,
                'Ti lệ trên 90% và tổng số đơn giao hàng trên 100 đơn': 8,
                'Ti lệ trên 90% và tổng số đơn giao hàng dưới 100 đơn': 7,
                'Ti lệ dưới 90% và tổng số đơn giao hàng dưới 100 đơn': -2,
                'Ti lệ dưới 90% và tổng số đơn giao hàng trên 100 đơn': -6,
                'Không có thông tin': 5,
            },
        }
    },
    'Thời gian giao hàng': {
        'Tiêu chí': 12,
        'Phân loại': {
            'Cách Miền': {
                # 96h
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 20 đơn': 10,
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 10 đơn': 9,
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 5 đơn': 8,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 6,
                # 120h
                'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 120h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # trễ
                'Trung bình dưới 144h và tổng số đơn giao hàng lớn hơn 3 đơn': -2,
                'Trung bình dưới 144h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -1,
                'Trung bình dưới 168h và tổng số đơn giao hàng lớn hơn 3 đơn': -6,
                'Trung bình dưới 168h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -4,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 168h': -10,
                'Không có thông tin': 5,
            },
            'Cận Miền': {
                # 72h
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn': 10,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn': 9,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn': 8,
                'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 6,
                # 96h
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # trễ
                'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 3 đơn': -2,
                'Trung bình dưới 120h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -1,
                'Trung bình dưới 144h và tổng số đơn giao hàng lớn hơn 3 đơn': -6,
                'Trung bình dưới 144h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -4,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 144h': -10,
                'Không có thông tin': 5,
            },
            'Nội Miền': {
                # 48h
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn': 10,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn': 9,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn': 8,
                'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 6,
                # 72h
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # trễ
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn': -2,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -1,
                'Trung bình dưới 120h và tổng số đơn giao hàng lớn hơn 3 đơn': -6,
                'Trung bình dưới 120h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -4,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 120h': -10,
                'Không có thông tin': 5,
            },
            'Nội Thành Tỉnh': {
                # 48h
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # 72h
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn': 9,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn': 8,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn': 6,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn': 4,
                'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 3,
                # trễ
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn': -4,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -2,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 96h': -10,
                'Không có thông tin': 5,
            },
            'Nội Thành Tp.HCM - HN': {
                # 48h
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # 72h
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn': 9,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn': 8,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn': 6,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn': 4,
                'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 3,
                # trễ
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn': -4,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -2,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 96h': -10,
                'Không có thông tin': 5,
            },
            'Ngoại Thành Tỉnh': {
                # 48h
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # 72h
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn': 9,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn': 8,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn': 6,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn': 4,
                'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 3,
                # trễ
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn': -4,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -2,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 96h': -10,
                'Không có thông tin': 5,
            },
            'Ngoại Thành Tp.HCM - HN': {
                # 48h
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 30 đơn': 10,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 20 đơn': 9,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 10 đơn': 8,
                'Trung bình dưới 48h và tổng số đơn giao hàng lớn hơn 5 đơn': 6,
                'Trung bình dưới 48h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 4,
                # 72h
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 30 đơn': 9,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 20 đơn': 8,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 10 đơn': 6,
                'Trung bình dưới 72h và tổng số đơn giao hàng lớn hơn 5 đơn': 4,
                'Trung bình dưới 72h và tổng số đơn giao hàng bé hơn hoặc bằng 5 đơn': 3,
                # trễ
                'Trung bình dưới 96h và tổng số đơn giao hàng lớn hơn 3 đơn': -4,
                'Trung bình dưới 96h và tổng số đơn giao hàng bé hơn hoặc bằng 3 đơn': -2,
                'Trung bình thời gian giao hàng lớn hơn hoặc bằng 96h': -10,
                'Không có thông tin': 5,
            },
        }
    },
    'Có kho giao nhận': {
        'Tiêu chí': 4,
        'Phân loại': {
            'Có từ 3 bưu cục cùng cấp quận/huyện trở lên': 10,
            'Có 2 bưu cục cùng cấp quận/huyện trở lên': 9,
            'Có bưu cục cùng cấp quận/huyện': 8,
            'Trong tỉnh có trên 80% bưu cục/tổng quận huyện của tỉnh': 6,
            'Trong tỉnh có trên 50% bưu cục/tổng quận huyện của tỉnh': 4,
            'Trong tỉnh có trên 30% bưu cục/tổng quận huyện của tỉnh': 2,
            'Trong tỉnh có bé hơn hoặc bằng 30% bưu cục/tổng quận huyện của tỉnh': 1,
            'Không có thông tin': 5,
            'Không có bưu cục trong tỉnh': -10
        }
    },
}

MAPPING_TIEU_CHI_ID = {
    'Ngưng giao nhận': 1, 
    'Đánh giá ZNS': 2, 
    'Tỉ lệ hoàn hàng': 3,
    'Chất lượng nội bộ': 4,
    'Thời gian giao hàng': 5,
    'Có kho giao nhận': 6,  
}

MAPPING_ORDER_TYPE_ID = {
    'Nội Thành Tỉnh': 1,
    'Ngoại Thành Tỉnh': 2,
    'Nội Thành Tp.HCM - HN': 3,
    'Ngoại Thành Tp.HCM - HN': 4,
    'Nội Miền': 5,
    'Cận Miền': 6,
    'Cách Miền': 7,
}

OVERLOADING_SCORE_DICT = {
    'Ngưng giao nhận': [-10],
    'Đánh giá ZNS': [-8, -10],
    'Tỉ lệ hoàn hàng': [-10],
    'Thời gian giao hàng': [-10],
    'Có kho giao nhận': [-10]
}

ACTIVE_CARRIER = ['GHTK', 'GHN', 'Viettel Post', 'BEST Express', 'Ninja Van', 'SPX Express']
MAPPING_CARRIER_ID = {
    'GHTK': 1,
    'GHN': 2,
    'J&T Express': 3,
    'Viettel Post': 4,
    'VNPost':  5,
    'BEST Express': 6,
    'Ninja Van': 7,
    'Snappy Express': 8,
    'ZTO Express': 9,
    'SPX Express': 10,
    'NETCO Post': 11,
    'TikiNOW Smart Logistics': 12,
}

MAPPING_ID_CARRIER = {}
for carrier, id in MAPPING_CARRIER_ID.items():
    MAPPING_ID_CARRIER[id] = carrier

SHOP_BEST_CARRIER_DEFAULT = 'BEST Express'
PARTNER_BEST_CARRIER_DEFAULT = 'BEST Express'
