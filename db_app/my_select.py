from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc
from models import Student, Grade, Subject, Group, Teacher
from colorama import Fore, Style

# Database connection
engine = create_engine(
    "postgresql+psycopg2://postgres:qwerty123@localhost:5432/postgres"
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
        return students if students else "Немає даних."


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
        return student if student else f"Немає студента для предмета з id {subject_id}."


def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    with Session() as session:
        groups_avg = (
            session.query(Group.name, func.avg(Grade.value).label("avg_grade"))
            .select_from(Group)
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id)
            .all()
        )
        return (
            groups_avg if groups_avg else f"Немає даних для предмета з id {subject_id}."
        )


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    with Session() as session:
        avg_grade = session.query(func.avg(Grade.value)).scalar()
        return avg_grade if avg_grade else "Немає даних."


def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    with Session() as session:
        courses = (
            session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        )
        return courses if courses else f"Немає курсів для викладача з id {teacher_id}."


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    with Session() as session:
        students = (
            session.query(Student.name).filter(Student.group_id == group_id).all()
        )
        return students if students else f"Немає студентів в групі з id {group_id}."


def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    with Session() as session:
        grades = (
            session.query(Student.name, Grade.value)
            .join(Grade)
            .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
            .all()
        )
        return (
            grades
            if grades
            else f"Немає оцінок для групи з id {group_id} та предмета з id {subject_id}."
        )


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    with Session() as session:
        avg_grade = (
            session.query(func.avg(Grade.value).label("avg_grade"))
            .join(Subject)
            .filter(Subject.teacher_id == teacher_id)
            .scalar()
        )
        return (
            avg_grade if avg_grade else f"Немає оцінок для викладача з id {teacher_id}."
        )


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
        return courses if courses else f"Студент з id {student_id} не відвідує курси."


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
        return (
            courses
            if courses
            else f"Студент з id {student_id} не відвідує курси викладача з id {teacher_id}."
        )


# Демо використання функцій (заміни yourparam на потрібні значення):
if __name__ == "__main__":
    print(Fore.GREEN + "Топ 5 студентів із найбільшим середнім балом:")
    print(select_1())

    print(Fore.YELLOW + "Студент з найвищим середнім балом з предмета:")
    print(select_2(subject_id=1))

    print(Fore.BLUE + "Середній бал у групах для предмета:")
    print(select_3(subject_id=1))

    print(Fore.CYAN + "Середній бал на потоці:")
    print(select_4())

    print(Fore.MAGENTA + "Курси, які читає викладач:")
    print(select_5(teacher_id=1))

    print(Fore.RED + "Студенти у групі:")
    print(select_6(group_id=1))

    print(Fore.GREEN + "Оцінки студентів у групі для предмета:")
    print(select_7(group_id=1, subject_id=1))

    print(Fore.YELLOW + "Середній бал викладача:")
    print(select_8(teacher_id=1))

    print(Fore.BLUE + "Курси, які відвідує студент:")
    print(select_9(student_id=1))

    print(Fore.CYAN + "Курси, які викладає викладач певному студенту:")
    print(select_10(student_id=1, teacher_id=1))
