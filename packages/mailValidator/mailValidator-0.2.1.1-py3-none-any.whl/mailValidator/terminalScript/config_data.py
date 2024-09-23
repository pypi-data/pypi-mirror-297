


def Config(arg):
    timeout = 5
    if hasattr(arg, 'timeout'):  # Check if 'timeout' is an attribute of 'arg'
        timeout = arg.timeout
    return {'timeout': timeout}  # Use dictionary literal for better readability
