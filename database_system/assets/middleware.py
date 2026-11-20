import logging
import time

logger = logging.getLogger(__name__)


class RequestUseTimeMiddleware:
    """ 请求耗时中间件 """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        end_time = time.perf_counter()
        use_time = round((end_time - start_time) * 1000, 2)
        logger.info(f"请求耗时：{use_time}ms")

        request.request_cost_time = use_time
        response["X-Request-Cost-Time"] = f"{use_time:.2f}ms"

        return response
