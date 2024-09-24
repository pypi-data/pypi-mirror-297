import logging
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

logging.basicConfig(filename='app/logs/search.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# file_handler = logging.FileHandler('logs/search.log')
# file_handler.setFormatter(formatter)


def log_info(req_body, res_body):
    logging.info("Request Body: " + str(req_body))
    logging.info("Response Body: " + str(res_body))


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            req_body = await request.body()
            response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)

            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(log_info, req_body, res_body)
                return Response(content=res_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type, background=task)
            else:
                res_body = response.body
                response.background = BackgroundTask(log_info, req_body, res_body)
                return response

        return custom_route_handler
