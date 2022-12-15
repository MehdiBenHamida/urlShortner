import httpx
from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .app import app
from .db_config import get_db_session
from .schemas import UrlCreateSchema, UrlSchema
from .services import create_short_url, get_url


@app.get("/")
def root():
    """
    Endpoint: root
    :return: app name
    """
    return {"api_name": "Url Shortner"}


@app.post("/shorten", response_model=UrlSchema, status_code=httpx.codes.CREATED)
def get_short_link(url: UrlCreateSchema, db: Session = Depends(get_db_session)):
    """
    Endpoint for shortening a URL from an original URL
    :param url: original url
    :param db: database session
    :return: url object
    """
    url = create_short_url(original_url=url.url, db=db)
    return {
        'original_url': url.original_url,
        'short_url': url.short_url,
        'created_at': url.created_at,
        'expires_at': url.expires_at,
    }


@app.get("/{short_url}")
def redirect(short_url: str, db: Session = Depends(get_db_session)):
    """
    Endpoint to redirect to the original url from the short url
    :param short_url: short url string code
    :param db: database session
    :return:
    """
    url = get_url(short_url=short_url, db=db)
    if url is None:
        raise HTTPException(
            status_code=httpx.codes.NOT_FOUND, detail="The link does not exist, could not redirect."
        )
    return RedirectResponse(url=url.original_url)
