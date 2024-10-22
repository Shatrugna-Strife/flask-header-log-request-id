from http import HTTPStatus
import logging

from flask import Flask
from flask_header_log_request_id import RequestID
from flask_header_log_request_id.log_filter import RequestIDLogFilter
from flask_header_log_request_id.request_id import current_request_id


def create_logger_and_app_with_middleware():
    app = Flask(__name__)

    # Configure and load Middleware
    app.config['REQUEST_ID_UNIQUE_VALUE_PREFIX'] = 'TEST-'
    RequestID(app)

    # Log Formatter
    class CustomLogFormatter(logging.Formatter):
        def format(self, record):
            record.request_id = current_request_id()
            return super().format(record)

    # Log Handler
    class CustomLoggingHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.logs = []

        def emit(self, record):
            """Emits the record to the list of logs."""
            log_entry = self.format(record)
            self.logs.append(log_entry)
        
        def get_logs(self):
            """Returns the list of logs."""
            return self.logs
        

    # Custom Logger
    custom_logger = logging.getLogger(__name__)
    logging_handler = CustomLoggingHandler()
    logging_handler.addFilter(RequestIDLogFilter())
    logging_handler.setFormatter(CustomLogFormatter('REQUEST_ID=%(request_id)s %(message)s'))
    custom_logger.addHandler(logging_handler)

    @app.route("/sample")
    def sample():
        custom_logger.warning("TestLog")
        return '', HTTPStatus.NO_CONTENT

    return custom_logger, logging_handler, app