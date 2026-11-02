import os

from app import create_app
from extensions import db
from models import User, Note


app = create_app()

DEMO_PASSWORD = os.environ.get("SEED_PASSWORD", "DemoPass123!")


seed_users = [
    {
        "username": "demo",
        "email": "demo@example.com"
    },
    {
        "username": "student",
        "email": "student@example.com"
    },
    {
        "username": "manager",
        "email": "manager@example.com"
    }
]


seed_notes = {
    "demo": [
        {
            "title": "Complete Python exercises",
            "content": "Practice Python functions, classes and data structures.",
            "category": "Learning",
            "priority": "High",
            "completed": False
        },
        {
            "title": "Plan weekly activities",
            "content": "Organize tasks and priorities for the coming week.",
            "category": "Personal",
            "priority": "Medium",
            "completed": True
        },
        {
            "title": "Read programming documentation",
            "content": "Review Flask and SQLAlchemy documentation.",
            "category": "Learning",
            "priority": "Low",
            "completed": False
        }
    ],
    "student": [
        {
            "title": "Submit coursework",
            "content": "Finish and submit the current programming assignment.",
            "category": "Education",
            "priority": "High",
            "completed": False
        },
        {
            "title": "Review lecture notes",
            "content": "Revise notes from the previous class.",
            "category": "Education",
            "priority": "Medium",
            "completed": True
        }
    ],
    "manager": [
        {
            "title": "Prepare project report",
            "content": "Prepare the monthly project progress report.",
            "category": "Work",
            "priority": "High",
            "completed": False
        },
        {
            "title": "Schedule team meeting",
            "content": "Organize the next project planning meeting.",
            "category": "Work",
            "priority": "Medium",
            "completed": False
        }
    ]
}


with app.app_context():
    created_users = 0
    created_notes = 0

    for user_data in seed_users:
        user = User.query.filter_by(
            email=user_data["email"]
        ).first()

        if user is None:
            user = User(
                username=user_data["username"],
                email=user_data["email"]
            )
            user.set_password(DEMO_PASSWORD)

            db.session.add(user)
            db.session.flush()

            created_users += 1

        for note_data in seed_notes[user_data["username"]]:
            existing_note = Note.query.filter_by(
                user_id=user.id,
                title=note_data["title"]
            ).first()

            if existing_note is None:
                note = Note(
                    **note_data,
                    user_id=user.id
                )

                db.session.add(note)
                created_notes += 1

    db.session.commit()

    print("Database seeding completed.")
    print(f"New users created: {created_users}")
    print(f"New notes created: {created_notes}")
    print("Demo username: demo")
    print("Demo email: demo@example.com")
    print("Demo password: value of SEED_PASSWORD or DemoPass123!")
