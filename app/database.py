import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Corrección por si Render o Supabase dan la URL con 'postgres://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Función para recargar datos (Importa modelos dentro para evitar errores circulares)
def reload_defaults(db):
    from app import models
    DEFAULT_DATA = [

        {
            "id": 1,
            "name": "Jesus Olivares",
            "category": "120kg+",
            "age": 28,
            "country": "USA",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 470, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 270, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 430, "reps": 1}
            ]
        },
        {
            "id": 2,
            "name": "Ray Williams",
            "category": "120kg+",
            "age": 37,
            "country": "USA",
            "achievements": ["Multiple IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 490, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 250, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 380, "reps": 1}
            ]
        },
        {
            "id": 3,
            "name": "Russel Orhii",
            "category": "83kg",
            "age": 30,
            "country": "USA",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 335, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 210, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 365, "reps": 1}
            ]
        },
        {
            "id": 4,
            "name": "Taylor Atwood",
            "category": "74kg",
            "age": 35,
            "country": "USA",
            "achievements": ["Multiple IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 303, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 205, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 335, "reps": 1}
            ]
        },
        {
            "id": 5,
            "name": "Gavin Adin",
            "category": "83kg",
            "age": 26,
            "country": "USA",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 340, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 215, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 370, "reps": 1}
            ]
        },
        {
            "id": 6,
            "name": "Jonathan Cayco",
            "category": "93kg",
            "age": 30,
            "country": "USA",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 350, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 240, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 360, "reps": 1}
            ]
        },
        {
            "id": 7,
            "name": "Kjell Egil Bakkelund",
            "category": "120kg+",
            "age": 34,
            "country": "Norway",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 455, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 280, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 390, "reps": 1}
            ]
        },
        {
            "id": 8,
            "name": "Agata Sitko",
            "category": "63kg",
            "age": 21,
            "country": "Poland",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 205, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 140, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 230, "reps": 1}
            ]
        },
        {
            "id": 9,
            "name": "Amanda Lawrence",
            "category": "84kg",
            "age": 31,
            "country": "USA",
            "achievements": ["Multiple IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 250, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 170, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 260, "reps": 1}
            ]
        },
        {
            "id": 10,
            "name": "Lya Bavoil",
            "category": "52kg",
            "age": 26,
            "country": "France",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 165, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 100, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 195, "reps": 1}
            ]
        },
        {
            "id": 11,
            "name": "Per Kjellberg",
            "category": "93kg",
            "age": 29,
            "country": "Sweden",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 360, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 220, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 380, "reps": 1}
            ]
        },
        {
            "id": 12,
            "name": "Emil Krastev",
            "category": "74kg",
            "age": 27,
            "country": "Bulgaria",
            "achievements": ["European Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 300, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 175, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 330, "reps": 1}
            ]
        },
        {
            "id": 13,
            "name": "Yury Belkin",
            "category": "105kg",
            "age": 31,
            "country": "Russia",
            "achievements": ["Multiple IPF World Champion", "World Record Squat"],
            "records": [
                {"exercise": "Squat", "weight_kg": 440, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 250, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 400, "reps": 1}
            ]
        },
        {
            "id": 14,
            "name": "Kirill Sarychev",
            "category": "120kg+",
            "age": 34,
            "country": "Russia",
            "achievements": ["World Record Bench Press 335kg"],
            "records": [
                {"exercise": "Squat", "weight_kg": 440, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 335, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 410, "reps": 1}
            ]
        },
        {
            "id": 15,
            "name": "Heather Connor",
            "category": "63kg",
            "age": 28,
            "country": "USA",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 200, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 135, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 215, "reps": 1}
            ]
        },
        {
            "id": 16,
            "name": "Kimberly Walford",
            "category": "76kg",
            "age": 30,
            "country": "USA",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 230, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 140, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 260, "reps": 1}
            ]
        },
        {
            "id": 17,
            "name": "Mariana Gasparyan",
            "category": "84kg",
            "age": 27,
            "country": "Russia",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 245, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 160, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 260, "reps": 1}
            ]
        },
        {
            "id": 18,
            "name": "Daniella Melo",
            "category": "84kg+",
            "age": 32,
            "country": "Brazil",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 275, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 170, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 260, "reps": 1}
            ]
        },
        {
            "id": 19,
            "name": "Carl Yngvar Christensen",
            "category": "120kg+",
            "age": 35,
            "country": "Norway",
            "achievements": ["European Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 450, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 270, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 420, "reps": 1}
            ]
        },
        {
            "id": 20,
            "name": "Joe Sullivan",
            "category": "120kg+",
            "age": 33,
            "country": "USA",
            "achievements": ["IPF National Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 460, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 260, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 400, "reps": 1}
            ]
        },
        {
            "id": 21,
            "name": "John Haack",
            "category": "90kg",
            "age": 28,
            "country": "USA",
            "achievements": ["IPF World Champion", "World Record Total 1030kg"],
            "records": [
                {"exercise": "Squat", "weight_kg": 410, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 260, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 365, "reps": 1}
            ]
        },
        {
            "id": 22,
            "name": "Bryce Lewis",
            "category": "105kg",
            "age": 29,
            "country": "USA",
            "achievements": ["IPF National Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 385, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 235, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 360, "reps": 1}
            ]
        },
        {
            "id": 23,
            "name": "Jamal Browner",
            "category": "120kg+",
            "age": 31,
            "country": "USA",
            "achievements": ["IPF World Competitor"],
            "records": [
                {"exercise": "Squat", "weight_kg": 455, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 265, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 410, "reps": 1}
            ]
        },
        {
            "id": 24,
            "name": "Sonita Muluh",
            "category": "84kg",
            "age": 26,
            "country": "USA",
            "achievements": ["IPF National Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 240, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 150, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 250, "reps": 1}
            ]
        },
        {
            "id": 25,
            "name": "Jessica Buettner",
            "category": "76kg",
            "age": 27,
            "country": "Canada",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 220, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 140, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 260, "reps": 1}
            ]
        },
        {
            "id": 26,
            "name": "Tiffany Chapon",
            "category": "63kg",
            "age": 24,
            "country": "France",
            "achievements": ["IPF European Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 180, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 120, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 200, "reps": 1}
            ]
        },
        {
            "id": 27,
            "name": "Isabella von Weissenberg",
            "category": "72kg",
            "age": 25,
            "country": "Germany",
            "achievements": ["IPF World Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 200, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 130, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 220, "reps": 1}
            ]
        },
        {
            "id": 28,
            "name": "Lukas Fink",
            "category": "93kg",
            "age": 28,
            "country": "Germany",
            "achievements": ["IPF National Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 355, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 230, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 375, "reps": 1}
            ]
        },
        {
            "id": 29,
            "name": "Petr Petras",
            "category": "83kg",
            "age": 27,
            "country": "Czech Republic",
            "achievements": ["IPF European Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 330, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 210, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 360, "reps": 1}
            ]
        },
        {
            "id": 30,
            "name": "Anatoli Novopismenny",
            "category": "105kg",
            "age": 33,
            "country": "Ukraine",
            "achievements": ["IPF European Champion"],
            "records": [
                {"exercise": "Squat", "weight_kg": 400, "reps": 1},
                {"exercise": "Bench Press", "weight_kg": 240, "reps": 1},
                {"exercise": "Deadlift", "weight_kg": 390, "reps": 1}
            ]
        }

    ]
    try:
        db.query(models.Athlete).delete()
        # Convertimos los diccionarios a objetos del modelo
        for data in DEFAULT_DATA:
            # Quitamos el ID del diccionario para que la BBDD lo genere o lo respete
            db_athlete = models.Athlete(**data)
            db.add(db_athlete)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error en reset: {e}")
        raise e