from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()
config = dotenv_values(".env")
import httpx
from dns.query import https
from fastapi import FastAPI, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from config import engine, SessionLocal, Base
from models import User, Product
from schemas import ProductSchema, UserSchema, UserLoginSchema
from jwt_bearer import JWTBearer
from jwt_handler import signJWT
from passlib.context import CryptContext

github_client_id = os.getenv('github_client_id')
github_secret_id = os.getenv('github_secret_id')
app = FastAPI()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", tags=['products'])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {"products": products}


@app.get('/products/{id}', tags=['products'])
def get_products_with_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"data": product}


@app.post("/products", dependencies=[Depends(JWTBearer())], tags=['products'])
def add_product(product: ProductSchema, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Mahsulot qo'shildi!", }


@app.post("/signup", tags=['user'])
def user_signup(user: UserSchema = Body(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return signJWT(new_user.email)


def check_user(data: UserLoginSchema, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    if user and pwd_context.verify(data.password, user.hashed_password):
        return True
    return False


@app.post("/login", tags=['user'])
def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    if check_user(user, db):
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=400, detail="Invalid login details")


@app.get("/login_github")
async def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={github_client_id}",
                            status_code=status.HTTP_302_FOUND)


@app.get("/github-code")
async def github_code(code: str):
    params = {
        "client_id": github_client_id,
        "client_secret": github_secret_id,
        "code": code
    }
    header = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://github.com/login/oauth/access_token", params=params, headers=header)
    response_json = response.json()
    access_token = response_json.get("access_token")
    async with httpx.AsyncClient() as client:
        header.update({"Authorization": f"token {access_token}"})
        response = await client.get(url="https://api.github.com/user", headers=header)
    response_json = response.json()
    return response_json


