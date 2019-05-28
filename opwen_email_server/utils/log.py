from logging import CRITICAL
from logging import DEBUG
from logging import INFO
from logging import WARNING
from logging import Formatter
from logging import Handler
from logging import Logger
from logging import StreamHandler
from logging import getLevelName
from logging import getLogger
from typing import Any
from typing import Iterable
from typing import Optional

from applicationinsights import TelemetryClient
from applicationinsights.channel import AsynchronousQueue
from applicationinsights.channel import AsynchronousSender
from applicationinsights.channel import NullSender
from applicationinsights.channel import TelemetryChannel
from cached_property import cached_property

from opwen_email_server.config import APPINSIGHTS_HOST
from opwen_email_server.config import APPINSIGHTS_KEY
from opwen_email_server.config import LOG_LEVEL
from opwen_email_server.constants.logging import SEPARATOR
from opwen_email_server.constants.logging import STDERR
from opwen_email_server.utils.collections import append
from opwen_email_server.utils.collections import singleton


@singleton
def _create_telemetry_channel() -> TelemetryChannel:
    if not APPINSIGHTS_KEY:
        sender = NullSender()
    else:
        sender = AsynchronousSender(APPINSIGHTS_HOST)

    queue = AsynchronousQueue(sender)
    return TelemetryChannel(queue=queue)


class LogMixin:
    _telemetry_channel = _create_telemetry_channel()
    _telemetry_key = APPINSIGHTS_KEY or '00000000-0000-0000-0000-000000000000'

    @cached_property
    def _default_log_handlers(self) -> Iterable[Handler]:
        handlers = []

        stderr = StreamHandler()
        stderr.setFormatter(Formatter(STDERR))
        handlers.append(stderr)

        return handlers

    @cached_property
    def _logger(self) -> Logger:
        log = getLogger()
        for handler in self._default_log_handlers:
            log.addHandler(handler)
        log.setLevel(LOG_LEVEL)
        return log

    @cached_property
    def _telemetry_client(self) -> TelemetryClient:
        return TelemetryClient(self._telemetry_key, self._telemetry_channel)

    def log_debug(self, message: str, *args: Any):
        self._log(DEBUG, message, args)

    def log_info(self, message: str, *args: Any):
        self._log(INFO, message, args)

    def log_warning(self, message: str, *args: Any):
        self._log(WARNING, message, args)

    def log_exception(self, ex: Exception, message: str, *args: Any):
        self._log(CRITICAL, message + ' (%r)', append(args, ex))

        # noinspection PyBroadException
        try:
            raise ex
        except Exception:
            self._telemetry_client.track_exception()
            self._telemetry_channel.flush()

    def _log(self, level: int, log_message: str, log_args: Iterable[Any]):
        if not self._logger.isEnabledFor(level):
            return

        message_parts = ['%s']
        args = [self.__class__.__name__]
        message_parts.append(log_message)
        args.extend(log_args)
        message = SEPARATOR.join(message_parts)
        self._logger.log(level, message, *args)
        self._telemetry_client.track_trace(message % tuple(args), severity=getLevelName(level))

    def log_event(self, event_name: str, properties: Optional[dict] = None):
        self._logger.info('%s%s%s', event_name, SEPARATOR, properties)
        self._telemetry_client.track_event(event_name, properties)
