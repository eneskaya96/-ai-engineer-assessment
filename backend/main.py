"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.database import db
from api.routes import addresses_router


# Create database tables
db.create_tables()

# Initialize FastAPI app
app = FastAPI(
    title="Address Assessment Backend",
    description="Backend for the Root Sustainability AI/ML Engineer assessment.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(addresses_router)