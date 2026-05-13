from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USER = "postgres"
PASSWORD = quote_plus("admin123")  # 👈 carácter 0xAB
HOST = "localhost"
PORT = "5432"
DB = "IndicadoresITD"

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)