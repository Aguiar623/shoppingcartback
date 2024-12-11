from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:dunklow5566@localhost/postgres"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base
Base = declarative_base()
