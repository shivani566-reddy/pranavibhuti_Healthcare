# app/models/pharmacy.py
"""
Pharmacy tables — owned by Vaishnavi.
"""
import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DECIMAL, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class OrderStatus(str, enum.Enum):
    PLACED    = "placed"
    CONFIRMED = "confirmed"
    PACKED    = "packed"
    SHIPPED   = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Medicine(TimestampMixin, Base):
    __tablename__ = "medicines"

    id               = Column(Integer, primary_key=True, index=True)
    name             = Column(String(200), nullable=False)
    generic_name     = Column(String(200))
    brand            = Column(String(150))
    category         = Column(String(100))
    description      = Column(Text)
    price            = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity   = Column(Integer, default=0)
    requires_prescription = Column(Boolean, default=False)
    image_url        = Column(String(500))
    is_active        = Column(Boolean, default=True)


class MedicineOrder(TimestampMixin, Base):
    __tablename__ = "medicine_orders"

    id             = Column(Integer, primary_key=True, index=True)
    patient_id     = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status         = Column(SAEnum(OrderStatus), default=OrderStatus.PLACED)
    total_amount   = Column(DECIMAL(10, 2), nullable=False)
    delivery_address = Column(Text)
    prescription_url = Column(String(500))
    payment_id     = Column(String(200), nullable=True)

    items = relationship("MedicineOrderItem", back_populates="order", cascade="all, delete-orphan")


class MedicineOrderItem(Base):
    __tablename__ = "medicine_order_items"

    id          = Column(Integer, primary_key=True, index=True)
    order_id    = Column(Integer, ForeignKey("medicine_orders.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity    = Column(Integer, nullable=False)
    unit_price  = Column(DECIMAL(10, 2), nullable=False)

    order    = relationship("MedicineOrder", back_populates="items")
    medicine = relationship("Medicine")
