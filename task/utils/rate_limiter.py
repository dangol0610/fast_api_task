from fastapi import Request
from fastapi.responses import JSONResponse
from task.utils.dependencies import redis_client


async def rate_limiter_middleware(
    request: Request,
    call_next,
):
    redis = redis_client
    max_requests = 10
    time_window = 60
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, time_window)

    if current > max_requests:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})

    response = await call_next(request)
    return response
