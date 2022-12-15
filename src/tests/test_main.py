from datetime import datetime

import httpx
from dateutil import parser
from fastapi.testclient import TestClient

from src.app.constants import URL_TIME_TO_EXPIRE
from src.app.main import app

from .utils import db_reset


class TestMain:

    @db_reset()
    def test_create_new_short_url(self):
        """Should create a new short url that expires after `URL_TIME_TO_EXPIRE`."""
        now = datetime.utcnow()
        with TestClient(app) as client:
            url = "https://www.google.com"
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url},
            )
            # check response status_code
            assert response.status_code == httpx.codes.CREATED

            # check all fields are in the response body
            assert "original_url" in response.json()
            assert "short_url" in response.json()
            assert "created_at" in response.json()
            assert "expires_at" in response.json()

            # check short code is valid
            short_url = response.json()["short_url"]
            assert len(short_url) == 10

            # check short url expires after `URL_TIME_TO_EXPIRE`
            expires_at = parser.parse(response.json()["expires_at"])
            assert expires_at >= now + URL_TIME_TO_EXPIRE

    @db_reset()
    def test_exists_short_url(self):
        """Should return the same short url because the url already exists and update expires_at."""

        with TestClient(app) as client:
            # first query to create short url
            url = "https://www.google.com"
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url},
            )
            # check valid response
            assert response.status_code == httpx.codes.CREATED
            assert "short_url" in response.json()
            short_url = response.json()["short_url"]
            expires_at = parser.parse(response.json()["expires_at"])

            # second query
            now = datetime.utcnow()
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url},
            )
            # check `expires_at` is updated
            assert response.json()["short_url"] == short_url
            new_expires_at = parser.parse(response.json()["expires_at"])
            assert new_expires_at != expires_at
            assert new_expires_at >= now + URL_TIME_TO_EXPIRE

    @db_reset()
    def test_case_sensitivity(self):
        """Should return the same short url because the url already exists in different case
        and update expires_at."""

        with TestClient(app) as client:
            # first query to create short url
            url = "https://www.google.com"
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url},
            )
            # check valid response
            assert response.status_code == httpx.codes.CREATED
            assert "short_url" in response.json()
            short_url = response.json()["short_url"]
            expires_at = parser.parse(response.json()["expires_at"])

            # second query
            now = datetime.utcnow()
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url.upper()},
            )
            # check `expires_at` is updated
            assert response.json()["short_url"] == short_url
            new_expires_at = parser.parse(response.json()["expires_at"])
            assert new_expires_at != expires_at
            assert new_expires_at >= now + URL_TIME_TO_EXPIRE

    @db_reset()
    def test_redirect_short_url(self):
        """Should redirect to the original url from the short url."""
        with TestClient(app) as client:
            # first query to create the short url
            url = "https://www.google.com"
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url},
            )

            # check valid response
            assert response.status_code == httpx.codes.CREATED
            assert "short_url" in response.json()
            short_url = response.json()["short_url"]

            # check short url redirect to the original url
            response = client.get(f"/{short_url}", follow_redirects=False)
            assert response.status_code == httpx.codes.TEMPORARY_REDIRECT
            assert response.headers["Location"] == url

    @db_reset()
    def test_non_valid_url(self):
        """Should return http error 422 because the provided url is invalid."""
        with TestClient(app) as client:
            # Invalid url because it doesn't contain "http(s)://" prefix
            url = "www.google.com"
            response = client.post(
                "/shorten",
                headers={"Content-Type": "application/json"},
                json={"url": url},
            )
            assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY

    @db_reset()
    def test_non_existing_short_url(self):
        """Should not redirect to the original url because of non-existent short url."""
        with TestClient(app) as client:
            response = client.get("/non-existing-path", follow_redirects=False)
            assert response.status_code == httpx.codes.NOT_FOUND
