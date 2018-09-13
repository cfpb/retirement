from datetime import datetime
import logging
import sys


logger = logging.getLogger(__name__)


def handle_error(fn):
    """
    Will save a screenshot of the current page if the method fails
    """
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            filename = datetime.now().isoformat()
            logger.exception("kwargs: %s" % kwargs)
            try:
                args[0].base.get_screenshot(filename)
            except Exception:
                logger.exception("HANDLER FAILURE:", sys.exc_info())

            raise

    return wrapper
