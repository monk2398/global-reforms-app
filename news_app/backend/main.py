from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException

from admin_api import router as admin_router
from database import (
    delete_news,
    get_news_by_id,
    init_db,
    insert_news,
    list_by_category,
    list_latest,
)
from models import NewsCategory, NewsCreate, NewsOut
from news_fetcher import detect_tags, fetch_and_store_news

app = FastAPI(title="Geopolitics News API", version="1.0.0")
app.include_router(admin_router)

scheduler = BackgroundScheduler()


def _row_to_news(row) -> NewsOut:
    return NewsOut(
        id=row["id"],
        title=row["title"],
        summary=row["summary"],
        category=row["category"],
        image_url=row["image_url"],
        source=row["source"],
        published_at=datetime.fromisoformat(row["published_at"]),
        tags=row["tags"].split(",") if row["tags"] else detect_tags(f"{row['title']} {row['summary']}"),
    )


@app.on_event("startup")
def startup() -> None:
    init_db()
    scheduler.add_job(fetch_and_store_news, "interval", minutes=10, id="rss_fetch", replace_existing=True)
    scheduler.start()


@app.on_event("shutdown")
def shutdown() -> None:
    scheduler.shutdown(wait=False)


@app.get("/news/latest", response_model=list[NewsOut])
def get_latest_news(limit: int = 20):
    return [_row_to_news(row) for row in list_latest(limit=limit)]


@app.get("/news/category/{category}", response_model=list[NewsOut])
def get_news_by_category(category: NewsCategory, limit: int = 20):
    return [_row_to_news(row) for row in list_by_category(category.value, limit=limit)]


@app.post("/news/add", response_model=NewsOut)
def add_news(news: NewsCreate):
    payload = news.model_dump()
    payload["published_at"] = news.published_at.isoformat()
    payload["category"] = news.category.value
    payload["image_url"] = str(news.image_url)
    payload["tags"] = ",".join(detect_tags(f"{news.title} {news.summary}"))
    news_id = insert_news(payload)

    saved = get_news_by_id(news_id)
    if not saved:
        raise HTTPException(status_code=500, detail="Unable to save news item")
    return _row_to_news(saved)


@app.delete("/news/{news_id}")
def remove_news(news_id: int):
    if not delete_news(news_id):
        raise HTTPException(status_code=404, detail="News item not found")
    return {"status": "deleted", "id": news_id}
