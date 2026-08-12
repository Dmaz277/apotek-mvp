from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Medicine(Base):
    __tablename__ = "medicine"
    id_medicine = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Integer)
    stock = Column(Integer)
    date_in = Column(Date)
    expired_date = Column(Date)

class Customer(Base):
    __tablename__ = "customer"
    id_customer = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(String(15))

class TransactionLog(Base):
    __tablename__ = "transactionlog"
    id_transaction = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id_customer"), nullable=True)
    customer_name = Column(String(100), nullable=True)
    medicine_id = Column(Integer, ForeignKey("medicine.id_medicine"))
    amount = Column(Integer)
    date_out = Column(Date)
