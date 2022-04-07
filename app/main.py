from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from logging.config import dictConfig

from .config import (
    APP_NAME,
    LOGGING,
    CORS_ORIGIN_WHITELIST,
    CORS_ALLOW_METHODS,
)
from .routers import router

# Load logging settings
dictConfig(LOGGING)

app = FastAPI(title=APP_NAME)
# include router
app.include_router(router)

# Set all CORS enabled origins
if CORS_ORIGIN_WHITELIST:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGIN_WHITELIST,
        allow_credentials=True,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=["*"],
    )

# api to check
# if the server is running
@app.get("/ping")
async def root():
    return {"message": f"Pong from {APP_NAME} app!"}
