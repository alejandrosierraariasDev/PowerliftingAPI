# Lista de atletas por defecto (tus 5 favoritos)
import copy
DEFAULT_DATA = [
    {
        "id": 1,
        "name": "Jesus Olivares",
        "category": "120kg+",
        "records": [
            {"exercise": "Squat", "weight_kg": 470, "reps": 1},
            {"exercise": "Bench Press", "weight_kg": 270, "reps": 2},
            {"exercise": "Deadlift", "weight_kg": 430, "reps": 1}
        ],
        "achievements": ["Raw World Record Squat", "IPF World Championship Medalist"],
        "age": 28,
        "country": "USA"
    },
    {
        "id": 2,
        "name": "LeBron James",
        "category": "NBA",
        "records": [
            {"stat": "Points Per Game", "value": 27.0},
            {"stat": "Assists Per Game", "value": 7.4},
            {"stat": "Rebounds Per Game", "value": 7.4}
        ],
        "achievements": ["4× NBA Champion", "4× NBA MVP", "17× All-Star"],
        "age": 38,
        "country": "USA"
    },
    {
        "id": 3,
        "name": "Jon Jones",
        "category": "UFC",
        "records": [
            {"stat": "Wins", "value": 27},
            {"stat": "Losses", "value": 1},
            {"stat": "Knockouts", "value": 10},
            {"stat": "Submissions", "value": 6}
        ],
        "achievements": ["UFC Light Heavyweight Champion", "Most Title Defenses in UFC History"],
        "age": 35,
        "country": "USA"
    },
    {
        "id": 4,
        "name": "Lasha Talakhadze",
        "category": "Weightlifting",
        "records": [
            {"exercise": "Snatch", "weight_kg": 225, "reps": 1},
            {"exercise": "Clean & Jerk", "weight_kg": 267, "reps": 1},
            {"exercise": "Total", "weight_kg": 492, "reps": 1}
        ],
        "achievements": ["Olympic Gold Medalist 2016 & 2020", "Multiple World Records"],
        "age": 28,
        "country": "Georgia"
    },
    {
        "id": 5,
        "name": "Amanda Nunes",
        "category": "UFC",
        "records": [
            {"stat": "Wins", "value": 23},
            {"stat": "Losses", "value": 5},
            {"stat": "Knockouts", "value": 13},
            {"stat": "Submissions", "value": 4}
        ],
        "achievements": ["UFC Bantamweight Champion", "UFC Featherweight Champion", "First Woman to Hold Two Titles Simultaneously"],
        "age": 35,
        "country": "Brazil"
    }
]

# Esta es nuestra "Base de datos" en memoria
db_athletes = list(DEFAULT_DATA)

def reload_defaults():
    global db_athletes
    # deepcopy asegura que los objetos anidados (listas de records) también sean nuevos
    db_athletes[:] = copy.deepcopy(DEFAULT_DATA)
