from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router

app = FastAPI(title="Task Trellis Remote API", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")
