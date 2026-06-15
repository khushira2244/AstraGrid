from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router


app = FastAPI(
    title="AstraGrid API",
    description="Backend API for SIFT Sentinel / AstraGrid cyber-physical incident investigation outputs.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AstraGrid API is running",
        "docs": "/docs",
    }