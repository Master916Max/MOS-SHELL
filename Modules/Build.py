
def next_build_version():
    """
    Returns the next build version.
    The build version is incremented by 1 each time this function is called.
    """
    try:
        with open("build_version.txt", "r") as file:
            current_version = int(file.read().strip())
    except FileNotFoundError:
        current_version = 0

    next_version = current_version + 1

    with open("build_version.txt", "w") as file:
        file.write(str(next_version))

    return next_version

def get_build_version():
    """
    Returns the current build version.
    If the build version file does not exist, it returns 0.
    """
    try:
        with open("build_version.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0