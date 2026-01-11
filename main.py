from fastapi import FastAPI, Query, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, LeadDB, UserDB, LeadHistoryDB, UserRole
from models import Lead, LeadStatusUpdate, User
import bcrypt
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "SUPER_SECRET_KEY_ZMIEN"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/leads")
def create_lead(lead: Lead):
    session = SessionLocal()
    try:
        if session.query(LeadDB).filter(LeadDB.email == lead.email).first():
            raise HTTPException(400, "Email już istnieje")

        lead_db = LeadDB(
            name=lead.name,
            email=lead.email,
            status=lead.status.value
        )
        session.add(lead_db)
        session.commit()
        session.refresh(lead_db)

        return {"message": "Lead dodany", "id": lead_db.id}
    finally:
        session.close()


@app.get("/leads")
def get_leads(
    status: str | None = Query(default=None),
    id: int | None = Query(default=None)
):
    session = SessionLocal()
    try:
        query = session.query(LeadDB)
        if status:
            query = query.filter(LeadDB.status == status)
        if id:
            query = query.filter(LeadDB.id == id)

        leads = query.all()

        return {
            "count": len(leads),
            "leads": [
                {
                    "id": l.id,
                    "name": l.name,
                    "email": l.email,
                    "status": l.status,
                    "created_at": l.created_at.isoformat()
                }
                for l in leads
            ]
        }
    finally:
        session.close()


@app.patch("/leads/{id}/status")
def update_lead_status(id: int, data: LeadStatusUpdate):
    session = SessionLocal()
    try:
        lead = session.query(LeadDB).filter(LeadDB.id == id).first()
        if not lead:
            raise HTTPException(404, "Nie znaleziono leada")

        if data.status.value == "client" and lead.status != "meeting":
            raise HTTPException(400, "Najpierw meeting")

        history = LeadHistoryDB(
            lead_id=lead.id,
            old_status=lead.status,
            new_status=data.status.value
        )

        lead.status = data.status.value
        session.add(history)
        session.commit()

        return {"message": "Status zmieniony"}
    finally:
        session.close()


@app.get("/leads/{id}/history")
def get_lead_history(id: int):
    session = SessionLocal()
    try:
        history = (
            session.query(LeadHistoryDB)
            .filter(LeadHistoryDB.lead_id == id)
            .order_by(LeadHistoryDB.changed_at)
            .all()
        )

        return {
            "lead_id": id,
            "history": [
                {
                    "old_status": h.old_status,
                    "new_status": h.new_status,
                    "changed_at": h.changed_at.isoformat()
                }
                for h in history
            ]
        }
    finally:
        session.close()


@app.post("/users")
def create_user(user: User, role: UserRole = Header(...)):
    if role != UserRole.admin:
        raise HTTPException(403, "Brak dostępu")

    session = SessionLocal()
    try:
        if session.query(UserDB).filter(UserDB.email == user.email).first():
            raise HTTPException(400, "Email już istnieje")

        hashed = bcrypt.hashpw(
            user.password.encode(),
            bcrypt.gensalt()
        ).decode()

        db_user = UserDB(
            username=user.username,
            email=user.email,
            password=hashed,
            role=user.role
        )
        session.add(db_user)
        session.commit()

        return {"message": "Użytkownik dodany"}
    finally:
        session.close()
