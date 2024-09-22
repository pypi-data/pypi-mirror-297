from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Enum as SQLEnum,
    ForeignKey,
    Boolean,
    Numeric,
    Time,
    JSON,
)
from enum import Enum
from sqlalchemy.orm import relationship
from br_common.models import BaseModel
 

class PaymentMethod(Enum):
    cash = "cash"
    partial_credit = "partial_credit"
    credit = "credit"

class Customer(BaseModel):
    __tablename__ = "customers"
    
    name = Column(String(255), nullable=False)
    mobile_number = Column(String(15), nullable=False, unique=True)
    payment_status = Column(SQLEnum(PaymentMethod, native_enum=False), nullable=False)
    image_url = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Customer: {[self.name if self.name else 'Unsaved']}"