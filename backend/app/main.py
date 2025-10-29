from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from .db import Base, engine, get_db
from .models import Estimate, EstimateStatus
from .schemas import EstimateCreate, EstimateOut, StatusUpdate, LoginRequest, TokenResponse
from .auth import create_token, require_user
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Repair Estimates API", version="1.0.0")
origins = [os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")]
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Basic env-based user for the demo
DEMO_USERNAME = os.getenv("DEMO_USERNAME", "admin")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "password")

@app.on_event("startup")
async def on_startup():
# Optional seed data for a nicer first run
    from .seed import seed
    db = next(get_db())
    seed(db)

@app.post("/auth/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    if data.username == DEMO_USERNAME and data.password == DEMO_PASSWORD:
        return TokenResponse(access_token=create_token(data.username))
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/estimates", response_model=List[EstimateOut])
async def list_estimates(status: Optional[EstimateStatus] = Query(None), db: Session = Depends(get_db), user: str = Depends(require_user)):
    q = db.query(Estimate)
    if status:
        q = q.filter(Estimate.status == status)
    return q.order_by(Estimate.id.desc()).all()

@app.post("/estimates", response_model=EstimateOut, status_code=201)
async def create_estimate(payload: EstimateCreate, db: Session = Depends(get_db), user: str = Depends(require_user)):
    est = Estimate(**payload.model_dump())
    db.add(est)
    db.commit()
    db.refresh(est)
    return est

@app.patch("/estimates/{estimate_id}/status", response_model=EstimateOut)
async def update_status(estimate_id: int, payload: StatusUpdate, db: Session = Depends(get_db), user: str = Depends(require_user)):
    est = db.get(Estimate, estimate_id)
    if not est:
        return est

