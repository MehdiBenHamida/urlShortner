from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .constants import MAX_RETRIES, URL_TIME_TO_EXPIRE
from .models import Url
from .utils import get_random_string, retry


@retry(exceptions=IntegrityError, max_retries=MAX_RETRIES)
def create_short_url(original_url: str, db: Session) -> Url:
    """
    Create a new short url with random characters or return the existing url after updating `expires_at`
    :param original_url: original url string
    :param db: database session
    :return: newly created url object
    """
    url = (
        db.query(Url)
        .filter(
            Url.original_url == original_url,
            Url.expires_at > datetime.utcnow()
        )
        .first()
    )
    if url:
        url.expires_at = datetime.utcnow() + URL_TIME_TO_EXPIRE
        db.commit()
        return url

    short_url = get_random_string()
    url = Url(
        original_url=original_url,
        short_url=short_url,
    )
    db.add(url)
    db.commit()

    return url


def get_url(short_url: str, db: Session) -> Url | None:
    """
    Returns the original url from a given short url string
    :param short_url: the short url string
    :param db: database session
    :return: original url object
    """
    url = (
        db.query(Url)
        .filter(
            Url.short_url == short_url,
            Url.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not url:
        return None

    url.clicks += 1
    db.commit()
    return url
