from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints.proxy_handler import router as proxy_router
from .api.router import api_router

app = FastAPI(title="Task Trellis Remote API", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount proxy router at root level (before API router to avoid conflicts)
app.include_router(proxy_router)
app.include_router(api_router, prefix="/api")
