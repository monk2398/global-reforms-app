import os
from datetime import datetime, timezone

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import delete_news, get_news_by_id, insert_news, list_latest, update_news
from models import NewsCategory

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def is_authenticated(request: Request) -> bool:
    return request.cookies.get("admin_auth") == "1"


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie("admin_auth", "1", httponly=True)
        return response

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password."},
        status_code=401,
    )


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("admin_auth")
    return response


@router.get("", response_class=HTMLResponse)
def dashboard(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "news": list_latest(limit=100),
            "categories": [c.value for c in NewsCategory],
        },
    )


@router.post("/add")
def add_news(
    request: Request,
    title: str = Form(...),
    summary: str = Form(...),
    category: str = Form(...),
    image_url: str = Form(...),
    source: str = Form(...),
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    insert_news(
        {
            "title": title,
            "summary": " ".join(summary.split()[:60]),
            "category": category,
            "image_url": image_url,
            "source": source,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "tags": category,
        }
    )
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/edit/{news_id}")
def edit_news(
    news_id: int,
    request: Request,
    title: str = Form(...),
    summary: str = Form(...),
    category: str = Form(...),
    image_url: str = Form(...),
    source: str = Form(...),
):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    update_news(
        news_id,
        {
            "title": title,
            "summary": " ".join(summary.split()[:60]),
            "category": category,
            "image_url": image_url,
            "source": source,
        },
    )
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/delete/{news_id}")
def remove_news(news_id: int, request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    delete_news(news_id)
    return RedirectResponse(url="/admin", status_code=303)


@router.get("/news/{news_id}")
def fetch_news(news_id: int, request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
    return get_news_by_id(news_id)
