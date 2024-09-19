# core/logging_config.py

# Create a global reference to the logging function
log_function = None

def set_log_function(func):
    global log_function
    log_function = func

def log(message):
    if log_function:
        log_function(message)
    else:
        print(f"Log function not set: {message}")  # Fallback logging
