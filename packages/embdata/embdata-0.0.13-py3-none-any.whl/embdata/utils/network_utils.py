import socket


def get_open_port() -> str:
    """Find and return an available port on the system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))  # Bind to an available port provided by the OS
        s.listen(1)
        return s.getsockname()[1]
