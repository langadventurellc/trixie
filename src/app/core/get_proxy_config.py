"""Get proxy configuration function."""

from typing import Optional

from .storage_data import proxy_configurations


def get_proxy_config(path: str) -> Optional[str]:
    """Get the target URL for a given path using prefix matching.

    Finds the longest matching prefix for accurate routing.

    Args:
        path: The request path to match (e.g., "/v1/users/123")

    Returns:
        Target URL if a matching prefix is found, None otherwise
    """
    if not proxy_configurations:
        return None

    # Sort prefixes by length (longest first) for accurate matching
    sorted_prefixes = sorted(proxy_configurations.keys(), key=len, reverse=True)

    for prefix in sorted_prefixes:
        if path.startswith(prefix):
            return proxy_configurations[prefix]

    return None
