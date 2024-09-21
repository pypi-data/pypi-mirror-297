from .base import Layer, Node, Chain, IfNode, LoopNode, node
import logging
from colorama import init, Fore, Style
import json
from pythonjsonlogger import jsonlogger
from uuid import uuid4
from datetime import datetime, timezone


__author__ = 'Francesco Lorè'
__email__ = 'flore9819@gmail.com'
__status__ = 'Development'

__version__ = "0.1.0"

init(autoreset=True)

class LogColors:
    """
    A class that defines color constants for logging messages.

    This class provides a set of color constants using the `colorama` library, which can be used to colorize 
    log messages in the terminal. The colors are defined using `colorama.Fore` and `colorama.Style` attributes.

    Attributes:
        OKCYAN (str): Color code for cyan text.
        OKGRAY (str): Color code for light black text (gray).
        WARNING (str): Color code for yellow text, typically used for warnings.
        FAIL (str): Color code for red text, typically used for errors or failures.
        ENDC (str): Color code to reset the text color to the default.
        BOLD (str): Color code to set the text to bold.

    Example:
        >>> print(LogColors.OKCYAN + "This is a cyan message." + LogColors.ENDC)
        >>> print(LogColors.WARNING + "This is a warning message." + LogColors.ENDC)
        >>> print(LogColors.FAIL + "This is an error message." + LogColors.ENDC)
        >>> print(LogColors.BOLD + "This is a bold message." + LogColors.ENDC)

    Notes:
        - `Fore` and `Style` are part of the `colorama` library and are used to apply colors and styles to terminal output.
        - The `ENDC` attribute is used to reset the text color back to the default after applying one of the color attributes.
    """
    OKCYAN = Fore.CYAN
    OKGRAY = Fore.LIGHTBLACK_EX
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT

DATE_FORMAT_TIMEZONE = "%Y-%m-%dT%H:%M:%S.%fZ"

class ColoredJsonFormatter(jsonlogger.JsonFormatter):
    """
    A custom JSON formatter for logging with colorized output based on log level.

    This formatter extends the `jsonlogger.JsonFormatter` to output log records in JSON format 
    with colors applied based on the log level. The colors are defined in the `LogColors` class.

    Attributes:
        FORMATS (dict): A dictionary mapping logging levels to corresponding color codes.
    
    Methods:
        __init__(*args, **kwargs):
            Initializes the formatter and calls the superclass initializer.
        
        add_fields(log_record, record, message_dict):
            Adds extra fields to the log record, including timestamp, log level, and trace ID.
        
        is_private_key(key):
            Checks if the given key is a private attribute.
        
        set_extra_keys(record, log_record, reserved):
            Adds extra data from the log record to the final log output, filtering out reserved and private attributes.
        
        format(record):
            Formats the log record, applying color based on the log level.
    
    Args:
        *args: Variable length argument list passed to the parent `JsonFormatter` class.
        **kwargs: Keyword arguments passed to the parent `JsonFormatter` class.
    
    Example:
        >>> logger = logging.getLogger("example")
        >>> handler = logging.StreamHandler()
        >>> formatter = ColoredJsonFormatter()
        >>> handler.setFormatter(formatter)
        >>> logger.addHandler(handler)
        >>> logger.info("This is an info message")
        >>> logger.error("This is an error message")
    
    Notes:
        - The `FORMATS` attribute maps logging levels to colors defined in the `LogColors` class.
        - The `format` method is overridden to apply color formatting to the log message based on its severity.
        - The `add_fields` method enriches the log record with additional fields like timestamp and trace ID.
    """

    FORMATS = {
        logging.DEBUG: LogColors.OKGRAY,
        logging.INFO: LogColors.OKCYAN,
        logging.WARNING: LogColors.WARNING,
        logging.ERROR: LogColors.FAIL,
        logging.CRITICAL: LogColors.BOLD + LogColors.FAIL
    }

    def __init__(self, *args, **kwargs):
        """
        Initializes the ColoredJsonFormatter and calls the parent class initializer.

        Args:
            *args: Variable length argument list.
            **kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        """
        Adds additional fields to the log record, including timestamp, log level, and trace ID.

        Args:
            log_record (dict): The dictionary of log record fields.
            record (logging.LogRecord): The log record instance.
            message_dict (dict): Dictionary of message parameters.
        """
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.now(timezone.utc).strftime(DATE_FORMAT_TIMEZONE)
        log_record["level"] = record.levelname
        log_record["type"] = "log"
        log_record["level_num"] = record.levelno
        log_record["logger_name"] = record.name
        trace = str(uuid4())

        if trace:
            log_record["trace_id"] = trace

        self.set_extra_keys(record, log_record, self._skip_fields)

    @staticmethod
    def is_private_key(key):
        """
        Determines if the given key is a private attribute.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key is a private attribute, False otherwise.
        """
        return hasattr(key, "startswith") and key.startswith("_")

    @staticmethod
    def set_extra_keys(record, log_record, reserved):
        """
        Adds extra data to the log record, filtering out reserved and private attributes.

        Args:
            record (logging.LogRecord): The log record instance.
            log_record (dict): The dictionary of log record fields.
            reserved (list): List of reserved field names to be excluded.
        """
        record_items = list(record.__dict__.items())
        records_filtered_reserved = [item for item in record_items if item[0] not in reserved]
        records_filtered_private_attr = [item for item in records_filtered_reserved if
                                         not ColoredJsonFormatter.is_private_key(item[0])]

        for key, value in records_filtered_private_attr:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            log_record[key] = value

    def format(self, record):
        """
        Formats the log record and applies color based on the log level.

        Args:
            record (logging.LogRecord): The log record instance.

        Returns:
            str: The formatted log message with color applied.
        """
        color = self.FORMATS.get(record.levelno, LogColors.ENDC)
        message = super().format(record)
        return f"{color}{message}{LogColors.ENDC}"


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColoredJsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)



__all__ = ['node', 'Layer', 'Node', "Chain", "IfNode", "LoopNode", "logger"]
