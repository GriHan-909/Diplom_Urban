from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
import uvicorn


DATABASE_URL = "sqlite:///./users.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_currency_rate(base: str, target: str) -> float:
    API_KEY = "1cdba79ff526921c2bce04dd"
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base.upper()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['conversion_rates'].get(target.upper(), None)
    return None


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    db: Session = SessionLocal()
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    print(user)
    db.close()
    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")
    return RedirectResponse(url="/currency", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/currency", response_class=HTMLResponse)
async def currency_page(request: Request, base: str = "RUB", target: str = "USD"):
    rate = get_currency_rate(base, target)
    return templates.TemplateResponse("currency.html", {"request": request, "rate": rate, "base": base, "target": target})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
