from fastapi import APIRouter, HTTPException
from pyla_logger import logger

from ...core.add_proxy_config import add_proxy_config
from ...core.clear_proxy_configs import clear_proxy_configs
from ..models.setup_request import SetupRequest
from ..models.setup_response import SetupResponse

router = APIRouter()


@router.post("/setup", response_model=SetupResponse)
async def configure_proxy_mappings(request: SetupRequest) -> SetupResponse:
    """Configure proxy path prefix to target URL mappings.

    Clears existing configurations and stores new mappings for use by the proxy handler.
    """
    try:
        # Clear existing proxy configurations (fresh setup each call)
        clear_proxy_configs()
        logger.info("Cleared existing proxy configurations")

        # Store new mappings
        configured_count = 0
        for prefix, target_url in request.mappings.items():
            add_proxy_config(prefix, target_url)
            configured_count += 1
            logger.debug(f"Added proxy mapping: {prefix} -> {target_url}")

        logger.info(f"Configured {configured_count} proxy mappings")

        return SetupResponse(
            success=True,
            configured_mappings=request.mappings,
            message=f"Configured {configured_count} proxy mappings",
        )

    except Exception as e:
        logger.error(f"Failed to configure proxy mappings: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while configuring proxy mappings"
        )
