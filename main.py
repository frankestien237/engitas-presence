from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid

DATABASE_URL = "sqlite:///./presence.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    device_id = Column(String, unique=True, nullable=True)     # ID unique du téléphone (bloque les multi-comptes)
    current_device_token = Column(String, nullable=True) # Token de session active

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Présence - Appareil Unique & Un Compte par Téléphone")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schémas ---
class RegisterRequest(BaseModel):
    username: str
    password: str
    device_id: str  # Le téléphone doit envoyer son ID unique à l'inscription

class LoginRequest(BaseModel):
    username: str
    password: str
    device_id: str  # Le téléphone doit aussi envoyer son ID au login


# --- 1. Route d'Inscription (Register) ---
@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Règle 1 : Vérifier si ce téléphone a déjà créé un compte
    existing_phone = db.query(UserDB).filter(UserDB.device_id == data.device_id).first()
    if existing_phone:
        raise HTTPException(
            status_code=403, 
            detail="Ce téléphone est déjà associé à un autre compte. Impossible d'en créer un nouveau."
        )
    
    # Règle 2 : Vérifier si le nom d'utilisateur existe déjà
    existing_user = db.query(UserDB).filter(UserDB.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà pris.")
    
    # Création du compte en liant le téléphone
    new_user = UserDB(
        username=data.username,
        password=data.password, # Penser à hasher en production
        device_id=data.device_id
    )
    db.add(new_user)
    db.commit()
    
    return {"success": True, "message": "Compte créé avec succès et lié à cet appareil."}


# --- 2. Route de Connexion (Login) ---
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == data.username).first()
    
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    
    # Règle 3 : Vérifier si le téléphone qui tente de se connecter est bien celui qui possède ce compte
    # (Empêche quelqu'un d'autre de se connecter sur un téléphone qui appartient déjà à un autre utilisateur)
    if user.device_id and user.device_id != data.device_id:
        raise HTTPException(
            status_code=403, 
            detail="Sécurité : Ce compte ne peut pas être ouvert depuis cet appareil."
        )
    
    # Si le compte n'a pas encore de device_id enregistré (cas des anciens comptes), on l'associe maintenant
    if not user.device_id:
        user.device_id = data.device_id

    # Générer le token de session unique pour l'appareil
    new_device_token = str(uuid.uuid4())
    user.current_device_token = new_device_token
    db.commit()
    
    return {
        "success": True,
        "device_token": new_device_token,
        "message": "Connexion réussie."
    }