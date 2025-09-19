"""Clear proxy configurations function."""

from .storage_data import proxy_configurations


def clear_proxy_configs() -> None:
    """Clear all proxy configurations."""
    proxy_configurations.clear()
