from scripts.database.database import Base
from sqlalchemy import String, Boolean, Integer, Column, Numeric, Date, TIMESTAMP


class RowAPI(Base):
    __tablename__ = "data_api"
    id = Column(Integer, primary_key=True)
    receiver_province_code = Column(String, nullable=True)
    receiver_district_code = Column(String, nullable=True)
    carrier_id = Column(Integer, nullable=False)
    order_type_id = Column(Integer, nullable=False)
    carrier_status = Column(Integer, default=False)
    carrier_status_comment = Column(String, nullable=False)
    estimate_delivery_time_details = Column(Numeric(5, 2), nullable=False)
    estimate_delivery_time = Column(String, nullable=False)
    fastest_carrier_id = Column(Integer, nullable=False)
    highest_score_carrier_id = Column(Integer, nullable=False)
    customer_best_carrier_id = Column(Integer, nullable=False)
    total_order = Column(Integer, nullable=False)
    delivery_success_rate = Column(Numeric(5, 2), nullable=False)
    score = Column(Numeric(3, 2), nullable=False)
    stars = Column(Numeric(2, 1), nullable=False)
    # import_date = Column(String, nullable=False)

    __table_args__ = {'schema': 'db_schema'}

    def __repr__(self):
        return f"<Result API from date={self.import_time}"


