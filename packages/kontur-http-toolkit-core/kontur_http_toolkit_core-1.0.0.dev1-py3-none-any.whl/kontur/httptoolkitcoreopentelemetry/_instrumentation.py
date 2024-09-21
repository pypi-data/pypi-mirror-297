from typing import Collection, Optional

from importlib.metadata import distribution
from kontur.httptoolkitcore.transport._httpx._session._async import AsyncHttpxSession
from kontur.httptoolkitcore.transport._httpx._session._sync import HttpxSession
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import TracerProvider


class HttpxTransportInstrumentor:
    @staticmethod
    def instrument(tracer_provider: Optional[TracerProvider] = None) -> None:
        def instrument_session(cls) -> None:
            if hasattr(cls, "__init_without_tracing__"):
                return
            cls.__init_without_tracing__ = cls.__init__

            def __init_with_tracing__(self, *args, **kwargs) -> None:
                self.__init_without_tracing__(*args, **kwargs)
                if tracer_provider is None:
                    HTTPXClientInstrumentor.instrument_client(client=self)
                else:
                    HTTPXClientInstrumentor.instrument_client(
                        client=self,
                        tracer_provider=tracer_provider,
                    )

            cls.__init__ = __init_with_tracing__

        instrument_session(HttpxSession)
        instrument_session(AsyncHttpxSession)

    @staticmethod
    def uninstrument() -> None:
        def uninstrument_session(cls) -> None:
            if not hasattr(cls, "__init_without_tracing__"):
                return
            cls.__init__ = cls.__init_without_tracing__
            del cls.__init_without_tracing__

        uninstrument_session(HttpxSession)
        uninstrument_session(AsyncHttpxSession)


class OtelHttpxTransportInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self) -> Collection[str]:
        requires = distribution("kontur_http_toolkit_core").requires or []
        return tuple([i.split(";")[0].strip() for i in requires if 'extra == "instruments"' in i])

    def _instrument(self, tracer_provider: Optional[TracerProvider] = None, **kwargs) -> None:
        HttpxTransportInstrumentor.instrument(tracer_provider)

    def _uninstrument(self, **kwargs) -> None:
        HttpxTransportInstrumentor.uninstrument()
