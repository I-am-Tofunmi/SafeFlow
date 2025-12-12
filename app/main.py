from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def root():
    return {"message": "SafeFlow API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- SAFE ROUTER LOADING ---
# We import inside the function to prevent "Circular Import" hangs
def include_routers():
    from app.api import auth, ai, transactions, trustscore, lessons, admin, contacts, webhooks, web3_attest, analytics
    
    app.include_router(auth.router)
    app.include_router(transactions.router)
    app.include_router(trustscore.router)
    app.include_router(lessons.router)
    app.include_router(ai.router)
    app.include_router(web3_attest.router)
    app.include_router(admin.router)
    app.include_router(contacts.router)
    app.include_router(webhooks.router)
    app.include_router(analytics.router)

# Load them now
include_routers()