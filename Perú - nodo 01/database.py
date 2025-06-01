from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

with open("services/config.json") as f:
    config = json.load(f)

DATABASE_URL = config["db_url"]

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




