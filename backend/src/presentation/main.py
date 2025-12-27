from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.session import Database, init_db
from src.infrastructure.settings import settings
from src.presentation.api.v1 import api_router


app = FastAPI(
    title="Kacheck API",
    description="Workout tracking application API",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    database = Database(settings.DATABASE_URL)
    init_db(database)


# Include API routers
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Kacheck API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

