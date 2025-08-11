
def set_debug_mode(mode: bool) -> None:
    """
    Set the debug mode for the application.
    
    Args:
        mode (bool): True to enable debug mode, False to disable it.
    """
    global DEBUG_MODE
    DEBUG_MODE = mode

def set_debug_level(level: int) -> None:
    """
    Set the debug level for the application.
    
    Args:
        level (int): The debug level to set.
    """
    global DEBUG_LEVEL
    DEBUG_LEVEL = level

def debugger(message: str, level: int = 1) -> None:
    """
    Print a debug message with a specified indentation level.
    
    Args:
        message (str): The message to print.
        level (int): The indentation level (default is 1).
    """
    global DEBUG_MODE, DEBUG_LEVEL
    if not DEBUG_MODE or level > DEBUG_LEVEL:
        return
    indent = ' ' * (level * 4)
    print(f"{indent}DEBUG: {message}")
