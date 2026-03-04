from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, field_validator


class NewsCategory(str, Enum):
    geopolitics = "geopolitics"
    defense = "defense"
    war = "war"
    economy = "economy"
    diplomacy = "diplomacy"


class NewsCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    summary: str = Field(..., min_length=20)
    category: NewsCategory
    image_url: HttpUrl
    source: str = Field(..., min_length=2, max_length=100)
    published_at: datetime

    @field_validator("summary")
    @classmethod
    def validate_summary_words(cls, summary: str) -> str:
        word_count = len(summary.split())
        if word_count > 60:
            raise ValueError("summary must be 60 words or fewer")
        return summary


class NewsUpdate(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=200)
    summary: str | None = Field(None, min_length=20)
    category: NewsCategory | None = None
    image_url: HttpUrl | None = None
    source: str | None = Field(None, min_length=2, max_length=100)
    published_at: datetime | None = None

    @field_validator("summary")
    @classmethod
    def validate_optional_summary_words(cls, summary: str | None) -> str | None:
        if summary and len(summary.split()) > 60:
            raise ValueError("summary must be 60 words or fewer")
        return summary


class NewsOut(BaseModel):
    id: int
    title: str
    summary: str
    category: NewsCategory
    image_url: str
    source: str
    published_at: datetime
    tags: list[str] = []
