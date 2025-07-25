from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

def setup_tracer(service_name: str = "sql-agent"):
    if not isinstance(trace.get_tracer_provider(), TracerProvider):
        resource = Resource.create({SERVICE_NAME: service_name})
        tracer_provider = TracerProvider(resource=resource)
        span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
    
    return trace.get_tracer(__name__)
