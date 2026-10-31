from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import User, Event
from app.schemas import UserCreate, EventCreate
from passlib.context import CryptContext

# Automatically create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TicketFlow API", version="1.0")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def root():
    return {"message": "Welcome to TicketFlow API! Head to /docs for Swagger documentation."}

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/events/", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, organizer_id: int, db: Session = Depends(get_db)):
    new_event = Event(**event.dict(), organizer_id=organizer_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event
