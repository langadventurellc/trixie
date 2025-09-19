"""Add proxy configuration function."""

from .storage_data import proxy_configurations


def add_proxy_config(prefix: str, target_url: str) -> None:
    """Add a proxy configuration mapping.

    Args:
        prefix: Path prefix to match (e.g., "/v1/users")
        target_url: Target URL to forward to (e.g., "https://api.example.com")
    """
    proxy_configurations[prefix] = target_url
