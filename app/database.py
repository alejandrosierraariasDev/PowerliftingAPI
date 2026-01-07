import copy

DEFAULT_DATA = [
    {
        "id": 1,
        "name": "Jesus Olivares",
        "category": "120kg+",
        "age": 28,
        "country": "USA",
        "achievements": [
            "IPF World Champion",
            "Raw World Record Squat"
        ],
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
        "achievements": [
            "Multiple IPF World Champion",
            "First Raw 490kg Squat"
        ],
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
        "achievements": [
            "IPF World Champion",
            "USAPL National Champion"
        ],
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
        "achievements": [
            "Multiple IPF World Champion",
            "World Record Total (74kg)"
        ],
        "records": [
            {"exercise": "Squat", "weight_kg": 303, "reps": 1},
            {"exercise": "Bench Press", "weight_kg": 205, "reps": 1},
            {"exercise": "Deadlift", "weight_kg": 335, "reps": 1}
        ]
    },
    {
        "id": 5,
        "name": "Jamila Jamal",
        "category": "84kg+",
        "age": 33,
        "country": "USA",
        "achievements": [
            "IPF World Champion",
            "World Record Deadlift"
        ],
        "records": [
            {"exercise": "Squat", "weight_kg": 275, "reps": 1},
            {"exercise": "Bench Press", "weight_kg": 170, "reps": 1},
            {"exercise": "Deadlift", "weight_kg": 260, "reps": 1}
        ]
    }
]

db_athletes = copy.deepcopy(DEFAULT_DATA)

def reload_defaults():
    global db_athletes
    db_athletes[:] = copy.deepcopy(DEFAULT_DATA)