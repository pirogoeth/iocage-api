import inspect


def get_caller():

    frame = inspect.currentframe()
    callstack = inspect.getouterframes(frame, 2)
    caller = callstack[2][0]
    callerinfo = inspect.getframeinfo(caller)
    
    if 'self' in caller.f_locals:
        caller_class = caller.f_locals['self'].__class__.__name__
    else:
        caller_class = None
    
    caller_name = callerinfo[2]

    if caller_class:
        caller_string = "%s.%s" % (caller_class, caller_name)
    else:
        caller_string = "%s" % (caller_name)

    return caller_string
