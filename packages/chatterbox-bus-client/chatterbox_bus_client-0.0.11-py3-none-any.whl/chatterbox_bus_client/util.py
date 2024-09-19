# optional imports
try:
    from dateutil import parser as dtparser
except ImportError:
    dtparser = None

try:
    from chatterbox.util.time import to_local
except ImportError:
    try:
        from lingua_nostra.time import to_local
    except ImportError:
        try:
            from mycroft.util.time import to_local
        except ImportError:
            try:
                from lingua_franca.time import to_local
            except ImportError:
                from logging import getLogger
                LOG = getLogger("BUS")
                def to_local(dt):
                    LOG.warning("timezone information not available")
                    return dt
