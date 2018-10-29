from logging import Formatter
from logging import StreamHandler
from logging import getLogger
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Tuple

from applicationinsights import TelemetryClient
from applicationinsights import exceptions

from opwen_email_server.config import APPINSIGHTS_KEY
from opwen_email_server.config import LOG_LEVEL

_STDERR_FORMAT = '%(asctime)s\t%(levelname)s\t%(message)s'
_STDERR = StreamHandler()
_STDERR.setFormatter(Formatter(_STDERR_FORMAT))

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
    info_separator = '|'

    def log_debug(self, message: str, *args: Any):
        self._log('debug', message, args)

    def log_info(self, message: str, *args: Any):
        self._log('info', message, args)

    def log_exception(self, message: str, *args: Any):
        self._log('exception', message, args)

    def _log(self, level: str, log_message: str, log_args: Iterable[Any]):
        message_parts = ['%s']
        args = [self.__class__.__name__]
        for message_part, arg in self.extra_log_args():
            message_parts.append(message_part)
            args.append(arg)
        message_parts.append(log_message)
        args.extend(log_args)
        message = self.info_separator.join(message_parts)
        log = getattr(_LOG, level)
        log(message, *args)

        if _APPINSIGHTS:
            _APPINSIGHTS.track_trace(message % tuple(args), {'level': level})
            if self.should_send_message_immediately(level):
                _APPINSIGHTS.flush()

    # noinspection PyMethodMayBeStatic
    def log_event(self, event_name: str, properties: Optional[dict] = None):
        _LOG.info('%s%s%s', event_name, self.info_separator, properties)

        if _APPINSIGHTS:
            _APPINSIGHTS.track_event(event_name, properties)
            _APPINSIGHTS.flush()

    # noinspection PyMethodMayBeStatic
    def should_send_message_immediately(self, level: str) -> bool:
        return level != 'debug'

    # noinspection PyMethodMayBeStatic
    def extra_log_args(self) -> Iterable[Tuple[str, Any]]:
        return []
