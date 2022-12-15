from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Integer, Text

from .constants import URL_TIME_TO_EXPIRE
from .db_config import Base


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, unique=True)
    original_url = Column(Text, nullable=False)
    short_url = Column(Text, unique=True, index=True, nullable=False)
    clicks = Column(BigInteger, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + URL_TIME_TO_EXPIRE)
