import inspect


def get_caller():

    frame = inspect.currentframe()
    callstack = inspect.getouterframes(frame, 2)
    caller = callstack[2][0]
    callerinfo = inspect.getframeinfo(caller)
    
    if 'self' in caller.f_locals:
        caller_class = caller.f_locals['self'].__class__.__name__
        caller_module = caller.f_locals['self'].__class__.__module__
    else:
        caller_class = None
        caller_module = None
    
    caller_name = callerinfo[2]
    
    if caller_class:
        caller_string = "%s.%s" % (caller_class, caller_name)
    else:
        caller_string = "%s" % (caller_name)

    if caller_module:
        caller_string = "%s." % (caller_module) + caller_string

    return caller_string
