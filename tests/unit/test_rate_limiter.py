"""Tests for rate limiter middleware."""

import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.middleware.rate_limiter import RateLimiterMiddleware


def _create_test_app(max_requests: int = 3) -> FastAPI:
    app = FastAPI()
    app.add_middleware(RateLimiterMiddleware, requests_per_minute=max_requests)

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app


def test_under_limit_passes():
    app = _create_test_app(max_requests=5)
    client = TestClient(app)
    for _ in range(5):
        resp = client.get("/ping")
        assert resp.status_code == 200


def test_over_limit_returns_429():
    app = _create_test_app(max_requests=3)
    client = TestClient(app)
    for _ in range(3):
        resp = client.get("/ping")
        assert resp.status_code == 200

    resp = client.get("/ping")
    assert resp.status_code == 429
    assert "Rate limit" in resp.json()["detail"]


def test_retry_after_header():
    app = _create_test_app(max_requests=1)
    client = TestClient(app)
    client.get("/ping")  # Use the one allowed request
    resp = client.get("/ping")
    assert resp.status_code == 429
    assert "Retry-After" in resp.headers
    retry_after = int(resp.headers["Retry-After"])
    assert retry_after >= 1
