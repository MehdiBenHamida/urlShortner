from datetime import datetime

from pydantic import BaseModel, HttpUrl


class UrlCreateSchema(BaseModel):
    url: HttpUrl


class UrlSchema(BaseModel):
    original_url: HttpUrl
    short_url: str
    created_at: datetime
    expires_at: datetime
