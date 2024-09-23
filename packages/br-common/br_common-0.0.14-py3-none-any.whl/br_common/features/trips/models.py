from br_common.features.employee.models import HRMaster
from br_common.models import BaseModel
from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric, Text
from sqlalchemy.orm import relationship


class Trip(BaseModel):
    __tablename__ = "trips"

    emp_id = Column(String(10), ForeignKey("hr_master.emp_id"), nullable=False)
    # Timestamp for begining and ending
    begin_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=True)
    # Odometer readings for beginning and ending
    begin_reading = Column(Numeric(10, 2), nullable=False)
    end_reading = Column(Numeric(10, 2), nullable=True)
    # Image paths for begining and ending
    begin_image_path = Column(Text, nullable=False)
    end_image_path = Column(Text, nullable=True)

    employee = relationship("HRMaster", backref="trips")

    def __repr__(self):
        return f"<Trip: {[self.id if self.id else 'Unsaved']}"