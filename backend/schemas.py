from pydantic import BaseModel
from datetime import date

# medicine
class MedicineCreate(BaseModel):
    name: str
    price: int
    stock: int
    date_in: date
    expired_date: date

class MedicineOut(MedicineCreate):
    id_medicine: int

# customer
class CustomerCreate(BaseModel):
    name: str
    phone: str

class CustomerOut(CustomerCreate):
    id_customer: int

# transaction
class TransactionCreate(BaseModel):
    customer_id: int | None = None
    customer_name: str | None = None
    medicine_id: int
    amount: int
    date_out: date | None = None

class TransactionOut(BaseModel):
    id_transaction: int
    customer_id: int | None
    customer_name: str | None
    medicine_id: int
    amount: int
    date_out: date

# Login
class LoginRequest(BaseModel):
    username: str
    password: str