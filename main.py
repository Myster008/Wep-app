from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, User, Purchase
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/user/{telegram_id}")
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == telegram_id).first()
    if not user:
        return {"error": "Foydalanuvchi topilmadi"}
    return user

@app.post("/user/register")
def register_user(telegram_id: int, name: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == telegram_id).first()
    if existing:
        return {"message": "Allaqachon ro'yxatdan o'tgan"}
    user = User(id=telegram_id, name=name)
    db.add(user)
    db.commit()
    return {"message": "Ro'yxatdan o'tildi", "user": telegram_id}

@app.post("/purchase/add")
def add_purchase(telegram_id: int, amount: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == telegram_id).first()
    if not user:
        return {"error": "Foydalanuvchi topilmadi"}
    
    user.purchases += amount
    user.last_purchase_date = datetime.now()
    user.current_island = user.purchases // 200

    if user.current_island >= 25:
        user.status = "finished"
    
    purchase = Purchase(user_id=telegram_id, amount=amount, date=datetime.now())
    db.add(purchase)
    db.commit()
    return {
        "purchases": user.purchases,
        "current_island": user.current_island,
        "status": user.status
    }