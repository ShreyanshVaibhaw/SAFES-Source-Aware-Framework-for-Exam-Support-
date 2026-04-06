"""Sliding-window rate limiter middleware."""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Dict, List

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Per-IP sliding window rate limiter.

    Args:
        app: ASGI application
        requests_per_minute: Maximum requests per IP per 60-second window
    """

    def __init__(self, app, requests_per_minute: int = 60) -> None:
        super().__init__(app)
        self.max_requests = requests_per_minute
        self.window = 60.0  # seconds
        self._requests: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        cutoff = now - self.window

        # Clean stale entries for this IP
        timestamps = self._requests[client_ip]
        self._requests[client_ip] = [t for t in timestamps if t > cutoff]
        timestamps = self._requests[client_ip]

        if len(timestamps) >= self.max_requests:
            oldest = min(timestamps) if timestamps else now
            retry_after = int(oldest + self.window - now) + 1
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."},
                headers={"Retry-After": str(max(1, retry_after))},
            )

        self._requests[client_ip].append(now)
        response = await call_next(request)
        return response
