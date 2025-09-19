"""Global storage variables for proxy system."""

# Global storage for proxy configurations (path prefix -> target URL)
proxy_configurations: dict[str, str] = {}

# Global storage for transaction history (simple dict storage for internal use)
transaction_history: list[dict] = []
