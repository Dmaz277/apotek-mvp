import models
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import schemas
from auth import verify_token
import os
from dotenv import load_dotenv
from auth import verify_password, create_access_token
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Medicine
@app.post("/medicine", response_model= schemas.MedicineOut)
def create_medicine(medicine: schemas.MedicineCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    new_medicine = models.Medicine(name=medicine.name, price=medicine.price, stock=medicine.stock, date_in=medicine.date_in, expired_date=medicine.expired_date)
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine

@app.get("/medicine", response_model=list[schemas.MedicineOut])
def get_all_medicine(db: Session = Depends(get_db), user=Depends(verify_token)):
    return db.query(models.Medicine).all()

@app.get("/medicine/{id}", response_model=schemas.MedicineOut)
def get_medicine(id: int, db:Session = Depends(get_db), user = Depends(verify_token)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id_medicine == id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="medicine not found")
    else:
        return medicine

@app.put("/medicine/{id}", response_model=schemas.MedicineOut)
def update_medicine(id:int,update:schemas.MedicineCreate, db: Session = Depends(get_db), user = Depends(verify_token)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id_medicine == id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="medicine not found")
    else:
        medicine.name = update.name
        medicine.price = update.price
        medicine.stock = update.stock
        medicine.date_in = update.date_in
        medicine.expired_date = update.expired_date
        db.commit()
        db.refresh(medicine)
        return medicine

@app.delete("/medicine/{id}")
def delete_medicine(id: int, db:Session = Depends(get_db), user = Depends(verify_token)):
    medicine = db.query(models.Medicine).filter(models.Medicine.id_medicine == id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail= " medicine not found")
    else:
        db.delete(medicine)
        db.commit()
        return {"message" : "medicine deleted sucessfully"}

# Customer
@app.post("/customer", response_model= schemas.CustomerOut)
def create_customer(customer: schemas.CustomerCreate, db: Session =Depends(get_db), user=Depends(verify_token)):
    new_customer = models.Customer(name=customer.name, phone=customer.phone)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.get("/customer", response_model=list[schemas.CustomerOut])
def get_all_customer(db: Session = Depends(get_db), user = Depends(verify_token)):
    return db.query(models.Customer).all()

@app.get("/customer/{id}", response_model=schemas.CustomerOut)
def get_customer(id: int, db: Session = Depends(get_db), user= Depends(verify_token)):
    customer = db.query(models.Customer).filter(models.Customer.id_customer == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail= "customer not found")
    else:
        return customer

@app.put("/customer/{id}", response_model=schemas.CustomerOut)
def update_customer(id: int, update:schemas.CustomerCreate, db: Session = Depends(get_db), user= Depends(verify_token)):
    customer = db.query(models.Customer).filter(models.Customer.id_customer == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")
    else:
        customer.name = update.name
        customer.phone = update.phone
        db.commit()
        db.refresh(customer)
        return customer

@app.delete("/customer/{id}")
def delete_customer(id: int, db: Session = Depends(get_db), user= Depends(verify_token)):
    customer = db.query(models.Customer).filter(models.Customer.id_customer == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=" customer not found")
    else:
        db.delete(customer)
        db.commit()
        return {"message" : "customer deleted sucessfully"}

# Transaction
@app.post("/transaction", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    from datetime import date
    
    # 1. Cek apakah medicine ada
    medicine = db.query(models.Medicine).filter(models.Medicine.id_medicine == transaction.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="medicine not found")
    
    # 2. Cek apakah obat sudah expired
    if medicine.expired_date < date.today():
        raise HTTPException(status_code=400, detail="medicine already expired, cannot sell")
    
    # 3. Cek apakah stock cukup
    if medicine.stock < transaction.amount:
        raise HTTPException(status_code=400, detail=f"insufficient stock, available: {medicine.stock}, requested: {transaction.amount}")
    
    # 4. Validasi customer (opsional)
    customer_id = None
    customer_name = None
    if transaction.customer_id:
        customer = db.query(models.Customer).filter(models.Customer.id_customer == transaction.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="customer not found")
        customer_id = transaction.customer_id
    elif transaction.customer_name:
        customer_name = transaction.customer_name
    
    # 5. Auto-deduct stock
    medicine.stock -= transaction.amount
    
    # 6. Simpan transaction ke database
    new_transaction = models.TransactionLog(
        customer_id=customer_id,
        customer_name=customer_name,
        medicine_id=transaction.medicine_id, 
        amount=transaction.amount, 
        date_out=transaction.date_out or date.today()
    )
    
    # 7. Commit semua perubahan (stock + transaction)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction

@app.get("/transaction", response_model=list[schemas.TransactionOut])
def get_all_transaction(db: Session = Depends(get_db), user= Depends(verify_token)):
    return db.query(models.TransactionLog).all()

@app.get("/transaction/{id}", response_model= schemas.TransactionOut)
def get_transaction(id: int, db: Session = Depends(get_db), user= Depends(verify_token)):
    transaction = db.query(models.TransactionLog).filter(models.TransactionLog.id_transaction == id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="transaction not found")
    else:
        return transaction

# Login
@app.post("/login")
def create_login(login: schemas.LoginRequest):
    if login.username == ADMIN_USERNAME and verify_password(login.password, ADMIN_PASSWORD_HASH):
        return {"access_token": create_access_token({"sub": login.username}), "token_type": "bearer"}
    else:
        raise HTTPException(401, "Invalid credentials")