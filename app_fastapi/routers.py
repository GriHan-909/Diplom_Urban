import aiohttp
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from db import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")
API_KEY = "1cdba79ff526921c2bce04dd"


async def get_currency_rate(base: str, target: str) -> float:
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base.upper()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['conversion_rates'].get(target.upper(), None)
    return None


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...), async_session: AsyncSession = Depends(get_session)):
    new_user = User(username=username, password=password)
    async_session.add(new_user)
    await async_session.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), async_session: AsyncSession = Depends(get_session)):
    result = await async_session.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")
    return RedirectResponse(url="/currency", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/currency", response_class=HTMLResponse)
async def currency_page(request: Request, base: str = "USD", target: str = "RUB"):
    rate = await get_currency_rate(base, target)
    return templates.TemplateResponse("currency.html", {"request": request, "rate": rate, "base": base, "target": target})
