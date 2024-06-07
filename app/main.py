from fastapi import FastAPI
from .internal import admin
from .routers import standard
from .dependencies import limiter, _rate_limit_exceeded_handler, RateLimitExceeded

# Set the app
app = FastAPI()

# register the Errorhandler for Ratelimits
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore

# Include Routers
app.include_router(standard.app, prefix="/standard", tags=["Standard"])

