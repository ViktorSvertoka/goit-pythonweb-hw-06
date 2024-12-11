from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Group, Student, Teacher, Subject, Grade
import random
from colorama import Fore, Style

# Database connection
engine = create_engine(
    "postgresql+psycopg2://postgres:qwerty123@localhost:5432/postgres"
)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


print(Fore.YELLOW + "Clearing existing data..." + Style.RESET_ALL)
session.query(Grade).delete()
session.query(Student).delete()
session.query(Subject).delete()
session.query(Teacher).delete()
session.query(Group).delete()
session.commit()


print(Fore.GREEN + "Seeding groups..." + Style.RESET_ALL)
groups = [Group(name=f"Group-{i+1}") for i in range(3)]
session.add_all(groups)
session.commit()
print(Fore.CYAN + f"Added {len(groups)} groups." + Style.RESET_ALL)


print(Fore.GREEN + "Seeding teachers..." + Style.RESET_ALL)
teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()
print(Fore.CYAN + f"Added {len(teachers)} teachers." + Style.RESET_ALL)


print(Fore.GREEN + "Seeding subjects..." + Style.RESET_ALL)
subjects = [
    Subject(name=f"Subject-{i+1}", teacher=random.choice(teachers)) for i in range(8)
]
session.add_all(subjects)
session.commit()
print(Fore.CYAN + f"Added {len(subjects)} subjects." + Style.RESET_ALL)


print(Fore.GREEN + "Seeding students..." + Style.RESET_ALL)
students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)
session.commit()
print(Fore.CYAN + f"Added {len(students)} students." + Style.RESET_ALL)


print(Fore.GREEN + "Seeding grades..." + Style.RESET_ALL)
grade_count = 0
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
        grade_count += 1

session.commit()
print(Fore.CYAN + f"Added {grade_count} grades." + Style.RESET_ALL)

session.close()
print(Fore.YELLOW + "Seeding completed successfully!" + Style.RESET_ALL)
