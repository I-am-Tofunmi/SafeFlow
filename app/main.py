from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import engine, Base

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SafeFlow Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def root():
    return {"message": "SafeFlow API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- ROUTER LOADING ---
from app.api import auth, ai, transactions, trustscore, lessons, admin, contacts, webhooks, web3_attest, analytics, biometrics 

app.include_router(auth.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(trustscore.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(web3_attest.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(biometrics.router, prefix="/api")

# --- FRONTEND MOUNTING (Local Dev Only) ---
import os
from fastapi.staticfiles import StaticFiles

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontends")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontends")