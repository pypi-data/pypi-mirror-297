import logging
import httpx
from aiolimiter import AsyncLimiter


class RateLimitedAsyncTransport(httpx.AsyncHTTPTransport):
    """
    A rate limited async httpx TransportLayer.
    """
    from httpx._config import DEFAULT_LIMITS, Limits, Proxy
    from httpx._transports.default import SOCKET_OPTION
    from httpx._types import CertTypes, VerifyTypes
    import typing

    type SOCKET_OPTION = typing.Union[
        typing.Tuple[int, int, int],
        typing.Tuple[int, int, typing.Union[bytes, bytearray]],
        typing.Tuple[int, int, None, int],
    ]
    _logger_name: str = "greeninvoice.async_greeninvoice_api_transport"
    _logger = logging.getLogger(name=_logger_name)

    def __init__(
        self,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = ...,
        trust_env: bool = True,
        proxy: Proxy | None = None,
        uds: str | None = None,
        local_address: str | None = None,
        retries: int = 0,
        socket_options: typing.Iterable[SOCKET_OPTION] | None = None,
        max_rate: int | None = None,
        time_period: int | None = None,
    ) -> None:
        super().__init__(
            verify,
            cert,
            http1,
            http2,
            limits,
            trust_env,
            proxy,
            uds,
            local_address,
            retries,
            socket_options,
        )
        if max_rate is None or time_period is None:
            from contextlib import nullcontext
            self.rate_limiter = nullcontext()
        else:
            self.rate_limiter = AsyncLimiter(max_rate=max_rate, time_period=time_period)  # aiolimiter.AsyncLimiter(max_rate, time_period)

    async def handle_async_request(self, request):
        async with self.rate_limiter:  # this section is *at most* going to entered "max_rate" times in a "time_period" second period.
            self._logger.debug("handled request.")
            return await super().handle_async_request(request)
