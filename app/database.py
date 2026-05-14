from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# cargar variables .env
load_dotenv()

# variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# motor SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)