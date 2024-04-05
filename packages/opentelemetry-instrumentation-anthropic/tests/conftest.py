"""Unit tests configuration module."""

import os
import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

pytest_plugins = []


@pytest.fixture(scope="session")
def exporter():
    exporter = InMemorySpanExporter()
    processor = SimpleSpanProcessor(exporter)

    provider = TracerProvider()
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    AnthropicInstrumentor(enrich_token_usage=True).instrument()

    return exporter


@pytest.fixture(autouse=True)
def clear_exporter(exporter):
    exporter.clear()


@pytest.fixture(autouse=True)
def environment():
    os.environ["ANTHROPIC_API_KEY"] = "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"


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["x-api-key"]}
