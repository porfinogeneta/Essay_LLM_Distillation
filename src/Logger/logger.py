import logging
import colorlog



def setup_logger():
    """Set up a colored logger with custom formatting"""
    logger = logging.getLogger('graph_matcher')
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create console handler with custom formatter
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s',
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red'
            }
        }
    ))
    logger.addHandler(handler)
    return logger