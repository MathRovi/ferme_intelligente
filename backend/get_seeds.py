from sqlalchemy.orm import Session
from db_models import Plant
from db_conn import SessionLocal

plants = [
    "Tomate",
    "Basilic",
    "Menthe",
    "Fraise",
    "Salade",
    "Poivron"
]

session = SessionLocal()
for idx, name in enumerate(plants, start=1):
    if not session.query(Plant).filter_by(id=idx).first():
        session.add(Plant(id=idx, name=name))
session.commit()
session.close()

print("🌱 Plantes insérées avec succès.")
