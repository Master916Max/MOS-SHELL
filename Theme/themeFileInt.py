
def read_theme_file(file_path: str) -> dict:
    """Load theme settings from a custom .theme file."""
    settings = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if "," in value:  # parse as tuple if it looks like colors
                parts = value.split(",")
                try:
                    value = tuple(int(p) for p in parts)
                except ValueError:
                    pass  # leave as string if not numbers
            elif value.isdigit():
                value = int(value)
            settings[key] = value
    return settings