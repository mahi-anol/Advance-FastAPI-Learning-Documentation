import os
from dotenv import load_dotenv
from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate,UserUpdate,UserOut

# Load environment variable.
load_dotenv()

app=FastAPI(
    title=os.getenv("APP_NAME","PGSQL"),
    description="A CRUD API for user management with PostgreSQL",
    version="1.0.0"
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/ping")
def ping():
    return {"status":"ok","message":"pong"}

# Create: Add a new User.
@app.post("/user",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def create_user(payload:UserCreate,db:Session=Depends(get_db)):
    # check if emai of username already exists
    existing_user=db.query(User).filter(
        (User.email==payload.email) | (User.username==payload.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already exists"
        )
    
    user=User(email=payload.email,username=payload.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Read: Get all users
@app.get('/user/{user_id}',response_model=list[UserOut])
def list_users(db:Session=Depends(get_db)):
    return db.query(User).order_by(User.id.asc()).all()

# Read: Get single user by ID
@app.get("/user/{user_id}",response_model=UserOut)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user=db.get(User,user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

# UPDATE: Modify existing user.
@app.put("/user/{user_id}",response_model=UserOut)
def update_user(user_id:int,payload:UserUpdate,db:Session=Depends(get_db)):
    # Get existing user
    user=db.get(User,user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    # Update email if provided and unique.
    if payload.email and payload.email!=user.email:
        #check if email already taken
        if db.query(User).filter(User.email==payload.email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already in use"
            )
        user.email=payload.email

    
    if payload.username and payload.username != user.username:
        # check if username already taken
        if db.query(User).filter(User.username==payload.username).first():
            raise HTTPException(
                status_code=400,
                detail="Username already in use"
            )
        
    db.add(user)
    db.commit()
    db.refresh()
    return user

# DELETE : Remove a user
@app.delete("/users/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    user=db.get(User,user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Uder not found"
        )
    
    db.delete(user)
    db.commit()

    return None # 204 responses have no body