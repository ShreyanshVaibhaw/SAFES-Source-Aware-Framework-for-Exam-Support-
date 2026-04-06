"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.dependencies import init_services
from src.api.middleware.rate_limiter import RateLimiterMiddleware
from src.api.routers.documents import router as documents_router
from src.api.routers.query import router as query_router
from src.utils.config import config
from src.utils.logger import setup_logger


def create_app() -> FastAPI:
    """Application factory."""
    setup_logger(console_level=config.log_level)
    app = FastAPI(
        title=config.get("app.name", "AI Study Assistant"),
        version=config.get("app.version", "1.0.0"),
        description=config.get("app.description", "RAG-based study assistant"),
    )

    cors = config.get("api.cors.allow_origins", ["http://localhost:8501"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors,
        allow_credentials=True,
        allow_methods=config.get("api.cors.allow_methods", ["*"]),
        allow_headers=config.get("api.cors.allow_headers", ["*"]),
    )

    # Rate limiting
    rate_limit = int(config.get("api.rate_limit", 60))
    app.add_middleware(RateLimiterMiddleware, requests_per_minute=rate_limit)

    @app.on_event("startup")
    async def startup_event() -> None:
        app.state.services = init_services()

    @app.get("/health")
    async def health() -> dict:
        services = getattr(app.state, "services", {})
        retrieval = services.get("retrieval_service")
        stats = retrieval.stats() if retrieval else {}
        return {"status": "ok", "app": config.get("app.name"), "vector_store": stats}

    app.include_router(documents_router)
    app.include_router(query_router)
    return app


app = create_app()
