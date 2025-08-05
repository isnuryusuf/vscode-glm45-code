from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import items, users

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Vue Boilerplate", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Vue Boilerplate"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}