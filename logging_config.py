import logging.config
from datetime import datetime
import os
import gzip
import shutil
import platform
import socket

# Define the base log directory
log_directory = 'logs'

def get_log_filename():
    """Generate a log filename with the current date."""
    today = datetime.now().strftime('%Y-%m-%d')
    return f'app_{today}.log'

def ensure_log_directory_exists():
    """Ensure that the logs directory exists."""
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

def get_system_info():
    """Retrieve system and environment information."""
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname())
    }

class ContextualFormatter(logging.Formatter):
    """Custom formatter to include contextual information in log records."""
    def format(self, record):
        system_info = get_system_info()
        record.os = system_info['os']
        record.os_version = system_info['os_version']
        record.hostname = system_info['hostname']
        record.ip_address = system_info['ip_address']
        return super().format(record)

def setup_logging():
    """Set up logging configuration."""
    ensure_log_directory_exists()  # Ensure the logs directory exists
    
    log_filename = get_log_filename()
    
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": ContextualFormatter,  # Use custom formatter
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(os)s - %(os_version)s - %(hostname)s - %(ip_address)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": logging.INFO,
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "default",
                "level": logging.INFO,
                "filename": os.path.join(log_directory, log_filename),
                "when": "midnight",  # Rotate logs at midnight
                "interval": 1,       # Interval in days
                "backupCount": 7,    # Keep 7 backup logs
                "encoding": "utf-8",
            },
            "error_file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "default",
                "level": logging.ERROR,
                "filename": os.path.join(log_directory, f'app_errors_{get_log_filename()}'),
                "when": "midnight",  # Rotate logs at midnight
                "interval": 1,       # Interval in days
                "backupCount": 7,    # Keep 7 backup logs
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": logging.INFO,
            "handlers": ["console", "file", "error_file"]
        },
        "loggers": {
            "__main__": {
                "level": logging.INFO,
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)

def compress_old_logs():
    """Compress old log files."""
    if not os.path.exists(log_directory):
        return  # If the directory doesn't exist, there's nothing to compress

    log_files = [f for f in os.listdir(log_directory) if f.endswith('.log') and not f.endswith('.gz')]
    for log_file in log_files:
        log_path = os.path.join(log_directory, log_file)
        with open(log_path, 'rb') as f_in:
            with gzip.open(f"{log_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(log_path)

# Call the setup_logging function to configure logging
setup_logging()

# Call the compress_old_logs function to compress existing logs
compress_old_logs()