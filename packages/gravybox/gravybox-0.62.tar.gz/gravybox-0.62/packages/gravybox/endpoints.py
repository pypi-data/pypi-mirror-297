import json
import time
import traceback
import uuid

from httpx import ReadTimeout
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from gravybox.betterstack import collect_logger
from gravybox.exceptions import DataUnavailable, GravyboxException
from gravybox.protocol import GravyboxResponse, Condition

logger = collect_logger()


class ErrorLoggingEndpoint(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        log_extras = {
            "client_host": request.client.host,
            "client_headers": request.headers.items()
        }
        try:
            payload = await request.json()
            log_extras["request_json"] = json.dumps(payload)
            request.state.trace_id = payload.get("trace_id", str(uuid.uuid4()))
            log_extras["trace_id"] = request.state.trace_id
        except Exception as error:
            log_extras["error_str"] = str(error)
            log_extras["condition"] = Condition.invalid_request.value
            logger.error("(!) failed to parse request", extra=log_extras)
            return JSONResponse(
                status_code=400,
                content=GravyboxResponse(
                    success=False,
                    error=Condition.invalid_request.value
                ).model_dump()
            )
        logger.info("( ) endpoint receiving request", extra=log_extras)
        start_time = time.time()
        try:
            response = await call_next(request)
            log_extras["status_code"] = response.status_code
            log_extras["condition"] = Condition.success.value
            return response
        except DataUnavailable:
            log_extras["status_code"] = 200
            log_extras["condition"] = Condition.data_unavailable.value
            return JSONResponse(
                status_code=200,
                content=GravyboxResponse(
                    success=False,
                    error=Condition.data_unavailable.value
                ).model_dump()
            )
        except ReadTimeout:
            log_extras["status_code"] = 500
            log_extras["condition"] = Condition.upstream_timeout.value
            return JSONResponse(
                status_code=500,
                content=GravyboxResponse(
                    success=False,
                    error=Condition.upstream_timeout.value
                ).model_dump()
            )
        except Exception as error:
            if isinstance(error, GravyboxException):
                log_extras |= error.log_extras
            log_extras["error_str"] = str(error)
            log_extras["traceback"] = traceback.format_exc()
            log_extras["status_code"] = 500
            log_extras["condition"] = Condition.unhandled_exception.value
            logger.error("(!) endpoint failed with unhandled exception", extra=log_extras)
            return JSONResponse(
                status_code=500,
                content=GravyboxResponse(
                    success=False,
                    error=Condition.unhandled_exception.value
                ).model_dump()
            )
        finally:
            log_extras["elapsed_time"] = time.time() - start_time
            logger.info("(*) endpoint emitting response", extra=log_extras)
