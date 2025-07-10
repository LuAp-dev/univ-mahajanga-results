# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, students

# Création de l'app FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API pour la consultation des résultats d'examens"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])

# Route racine
@app.get("/")
async def root():
    return {
        "message": f"Bienvenue sur {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running"
    }

# Route de santé
@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}