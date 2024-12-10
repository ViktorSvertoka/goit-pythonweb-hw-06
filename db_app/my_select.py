from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc
from models import Student, Grade, Subject, Group, Teacher

# Database connection
engine = create_engine(
    "postgresql+psycopg2://postgres:qwerty123@postgres_db:5432/postgres"
)
Session = sessionmaker(bind=engine)


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    with Session() as session:
        students = (
            session.query(Student.name, func.avg(Grade.value).label("avg_grade"))
            .join(Grade)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(5)
            .all()
        )
        return students


def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    with Session() as session:
        student = (
            session.query(Student.name, func.avg(Grade.value).label("avg_grade"))
            .join(Grade)
            .filter(Grade.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .first()
        )
        return student


def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    with Session() as session:
        groups_avg = (
            session.query(Group.name, func.avg(Grade.value).label("avg_grade"))
            .join(Student)
            .join(Grade)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id)
            .all()
        )
        return groups_avg


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    with Session() as session:
        avg_grade = session.query(func.avg(Grade.value)).scalar()
        return avg_grade


def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    with Session() as session:
        courses = (
            session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        )
        return courses


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    with Session() as session:
        students = (
            session.query(Student.name).filter(Student.group_id == group_id).all()
        )
        return students


def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    with Session() as session:
        grades = (
            session.query(Student.name, Grade.value)
            .join(Grade)
            .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
            .all()
        )
        return grades


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    with Session() as session:
        avg_grade = (
            session.query(func.avg(Grade.value).label("avg_grade"))
            .join(Subject)
            .filter(Subject.teacher_id == teacher_id)
            .scalar()
        )
        return avg_grade


def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    with Session() as session:
        courses = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id)
            .distinct()
            .all()
        )
        return courses


def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    with Session() as session:
        courses = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
            .distinct()
            .all()
        )
        return courses


# Демо використання функцій (заміни yourparam на потрібні значення):
if __name__ == "__main__":
    print("Top 5 students with highest average grades:", select_1())
    print("Student with highest average grade in a subject:", select_2(subject_id=1))
    print("Average grades in groups for a subject:", select_3(subject_id=1))
    print("Average grade for all students:", select_4())
    print("Courses taught by a teacher:", select_5(teacher_id=1))
    print("Students in a group:", select_6(group_id=1))
    print(
        "Grades of students in a group for a subject:",
        select_7(group_id=1, subject_id=1),
    )
    print("Average grade given by a teacher:", select_8(teacher_id=1))
    print("Courses attended by a student:", select_9(student_id=1))
    print(
        "Courses taught by a teacher to a student:",
        select_10(student_id=1, teacher_id=1),
    )
