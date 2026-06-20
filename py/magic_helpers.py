import types

def log_begin(s):
    print(f"↓↓↓↓ {s} ↓↓↓↓")

def log_end(s):
    print(f"↑↑↑↑ {s} ↑↑↑↑")

def log(s):
    print(f"→→→→ {s}")


def log_guard(d, l, l_):
    return d and l <= l_

def log_debug(d, l, l_, s):
    if d and l <= l_: log(s)

def logger_debug(d, l):
    def _guard(l_): 
        return d and l >= l_
    def _log(l_, s): 
        if _guard(l_): 
            log(f"DEBUG[{l_}]: {s}")
    return types.SimpleNamespace(guard=_guard, log=_log)

def logger_silent(t):
    def _guard(): 
        return not t
    def _log(s):
        if _guard():
            log(s)
    def _log_begin(s):
        if _guard():
            log_begin(s)
    def _log_end(s):
        if _guard():
            log_end(s)
    return types.SimpleNamespace(
            guard=_guard, 
            log=_log, 
            log_begin=_log_begin, 
            log_end=_log_end)
