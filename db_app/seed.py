from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Group, Student, Teacher, Subject, Grade
import random
from datetime import datetime, timedelta

# Database connection
engine = create_engine(
    "postgresql+psycopg2://postgres:qwerty123@localhost:5432/postgres"
)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Seed groups
groups = [Group(name=f"Group-{i+1}") for i in range(3)]
session.add_all(groups)
session.commit()

# Seed teachers
teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Seed subjects
subjects = [
    Subject(name=f"Subject-{i+1}", teacher=random.choice(teachers)) for i in range(8)
]
session.add_all(subjects)
session.commit()

# Seed students
students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)
session.commit()

# Seed grades
for student in students:
    for _ in range(20):
        subject = random.choice(subjects)
        grade = Grade(
            value=round(random.uniform(2.0, 5.0), 2),
            date=fake.date_time_between(start_date="-1y", end_date="now"),
            student=student,
            subject=subject,
        )
        session.add(grade)

session.commit()
session.close()
