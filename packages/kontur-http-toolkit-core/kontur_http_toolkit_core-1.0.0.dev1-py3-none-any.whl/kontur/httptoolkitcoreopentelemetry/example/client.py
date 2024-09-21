import asyncio

from kontur.httptoolkitcore import AsyncService, Service
from kontur.httptoolkitcore.transport import HttpxTransport, AsyncHttpxTransport
from kontur.httptoolkitcoreopentelemetry import HttpxTransportInstrumentor

from instrumentation import tracer


HttpxTransportInstrumentor.instrument()


def sync_request():
    with tracer.start_as_current_span("client-app-sync"):
        response = Service(
            transport=HttpxTransport(
                "http://server:8888",
                open_timeout_in_seconds=60,
                read_timeout_in_seconds=60,
            )
        ).get("/")
        assert response.status_code == 200


async def async_request():
    with tracer.start_as_current_span("client-app-async"):
        response = await AsyncService(
            transport=AsyncHttpxTransport(
                "http://server:8888",
                open_timeout_in_seconds=60,
                read_timeout_in_seconds=60,
            )
        ).get("/")
        assert response.status_code == 200


with tracer.start_as_current_span("client-app"):
    sync_request()
    asyncio.run(async_request())
