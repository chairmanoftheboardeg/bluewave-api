import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status

# Simple in-memory rate limiter:
# key -> (window_start, count)
_BUCKETS: Dict[str, Tuple[float, int]] = {}

def rate_limit(request: Request, key_prefix: str, limit: int = 20, window_seconds: int = 60) -> None:
    # best-effort IP; behind proxies Render sets X-Forwarded-For
    xff = request.headers.get("x-forwarded-for")
    ip = (xff.split(",")[0].strip() if xff else (request.client.host if request.client else "unknown"))
    key = f"{key_prefix}:{ip}"

    now = time.time()
    window_start, count = _BUCKETS.get(key, (now, 0))

    if now - window_start > window_seconds:
        window_start, count = now, 0

    count += 1
    _BUCKETS[key] = (window_start, count)

    if count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again shortly.",
        )
