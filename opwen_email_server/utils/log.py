from logging import Formatter
from logging import StreamHandler
from logging import getLogger
from typing import Any
from typing import Iterable
from typing import Optional

from applicationinsights import TelemetryClient
from applicationinsights import exceptions

from opwen_email_server.config import APPINSIGHTS_KEY
from opwen_email_server.config import LOG_LEVEL
from opwen_email_server.constants.logging import SEPARATOR
from opwen_email_server.constants.logging import STDERR

_STDERR = StreamHandler()
_STDERR.setFormatter(Formatter(STDERR))

_LOG = getLogger()
_LOG.addHandler(_STDERR)
_LOG.setLevel(LOG_LEVEL)

_APPINSIGHTS = None  # type: TelemetryClient

if APPINSIGHTS_KEY:
    _APPINSIGHTS = TelemetryClient(APPINSIGHTS_KEY)
    _APPINSIGHTS.channel.sender.send_interval_in_milliseconds = 30 * 1000
    _APPINSIGHTS.channel.sender.max_queue_item_count = 10
    exceptions.enable(APPINSIGHTS_KEY)


class LogMixin(object):
    def log_debug(self, message: str, *args: Any):
        self._log('debug', message, args)

    def log_info(self, message: str, *args: Any):
        self._log('info', message, args)

    def log_warning(self, message: str, *args: Any):
        self._log('warning', message, args)

    def log_exception(self, message: str, *args: Any):
        self._log('exception', message, args)

    def _log(self, level: str, log_message: str, log_args: Iterable[Any]):
        message_parts = ['%s']
        args = [self.__class__.__name__]
        message_parts.append(log_message)
        args.extend(log_args)
        message = SEPARATOR.join(message_parts)
        log = getattr(_LOG, level)
        log(message, *args)

        if _APPINSIGHTS:
            _APPINSIGHTS.track_trace(message % tuple(args), {'level': level})
            if self.should_send_message_immediately(level):
                _APPINSIGHTS.flush()

    # noinspection PyMethodMayBeStatic
    def log_event(self, event_name: str, properties: Optional[dict] = None):
        _LOG.info('%s%s%s', event_name, SEPARATOR, properties)

        if _APPINSIGHTS:
            _APPINSIGHTS.track_event(event_name, properties)
            _APPINSIGHTS.flush()

    # noinspection PyMethodMayBeStatic
    def should_send_message_immediately(self, level: str) -> bool:
        return level != 'debug'
