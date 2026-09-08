import logging

_logger_provider = None


def get_otel_handler():
    """Builds (once) an OTLP-exporting LoggerProvider and returns a stdlib
    logging.Handler bridging into it. Endpoint/service name come from the
    standard OTEL_EXPORTER_OTLP_ENDPOINT / OTEL_SERVICE_NAME env vars."""
    global _logger_provider

    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource

    if _logger_provider is None:
        _logger_provider = LoggerProvider(resource=Resource.create())
        _logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(OTLPLogExporter())
        )

    return LoggingHandler(level=logging.INFO, logger_provider=_logger_provider)
