from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, User, Purchase
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS qo'shish
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Admin — barcha foydalanuvchilar
@app.get("/admin/users")
def get_all_users(secret: str, db: Session = Depends(get_db)):
    if secret != "ADMIN_SECRET_KEY":
        return {"error": "Ruxsat yo'q"}
    users = db.query(User).all()
    return users

# Admin — dori qo'shish
@app.post("/admin/purchase/add")
def admin_add_purchase(secret: str, telegram_id: int, amount: int, db: Session = Depends(get_db)):
    if secret != "ADMIN_SECRET_KEY":
        return {"error": "Ruxsat yo'q"}
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
    return {"message": "Qo'shildi", "purchases": user.purchases, "island": user.current_island}

# Admin — reset
@app.post("/admin/reset")
def admin_reset(secret: str, telegram_id: int, db: Session = Depends(get_db)):
    if secret != "ADMIN_SECRET_KEY":
        return {"error": "Ruxsat yo'q"}
    user = db.query(User).filter(User.id == telegram_id).first()
    if not user:
        return {"error": "Foydalanuvchi topilmadi"}
    user.purchases = 0
    user.current_island = 0
    user.status = "active"
    db.commit()
    return {"message": "Reset qilindi"}

# Admin — mukofot tasdiqlash
@app.post("/admin/reward")
def admin_reward(secret: str, telegram_id: int, reward_type: str, db: Session = Depends(get_db)):
    if secret != "ADMIN_SECRET_KEY":
        return {"error": "Ruxsat yo'q"}
    from models import Reward
    reward = Reward(user_id=telegram_id, reward_type=reward_type, date=datetime.now())
    db.add(reward)
    db.commit()
    return {"message": f"{reward_type} mukofoti berildi"}
