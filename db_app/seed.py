import random
from db_connect import session
from datetime import datetime, timedelta
from faker import Faker
from models import Group, Student, Teacher, Subject, Grade


fake = Faker()

group_names = ["Group-A", "Group-B", "Group-C"]
groups = []
for name in group_names:
    group = Group(group_name=name)
    session.add(group)
    groups.append(group)
session.commit()

teachers = []
for _ in range(random.randint(3, 5)):
    teacher = Teacher(teacher_name=fake.name())
    session.add(teacher)
    teachers.append(teacher)
session.commit()

subject_names = [
    "Algorithms",
    "Data Structures",
    "Machine Learning",
    "Artificial Intelligence",
    "Computer Networks",
    "Operating Systems",
    "Database Management Systems",
    "Software Engineering",
    "Cybersecurity",
    "Cloud Computing",
]

subjects = []
for name in random.sample(subject_names, random.randint(5, 8)):
    subject = Subject(subject_name=name, teacher=random.choice(teachers))
    session.add(subject)
    subjects.append(subject)
session.commit()

students = []
for _ in range(random.randint(30, 50)):
    student = Student(student_name=fake.name(), group=random.choice(groups))
    session.add(student)
    students.append(student)
session.commit()

for student in students:
    for _ in range(random.randint(1, 20)):
        grade = Grade(
            grade=random.randint(60, 100),
            date_of=datetime.now() - timedelta(days=random.randint(1, 365)),
            student=student,
            subject=random.choice(subjects),
        )
        session.add(grade)
session.commit()
