from db_connect import session
from pprint import pprint
from sqlalchemy import func, desc
from colorama import Fore, Style, init

from models import Student, Group, Subject, Teacher, Grade

init(autoreset=True)

# 1. Знайти 5 студентів з найвищим середнім балом по всіх предметах
avg_grades = (
    session.query(Grade.student_id, func.avg(Grade.grade).label("average_grade"))
    .group_by(Grade.student_id)
    .subquery()
)

five_top_students = (
    session.query(Student.student_name, avg_grades.c.average_grade)
    .join(avg_grades, Student.id == avg_grades.c.student_id)
    .order_by(desc(avg_grades.c.average_grade))
    .limit(5)
    .all()
)

print(Fore.GREEN + "1. Результат select_1")
pprint(five_top_students)


# 2. Знайти студента з найвищим середнім балом по певному предмету
subject_id = 3
best_student = (
    session.query(
        Student.student_name,
        func.avg(Grade.grade).label("average_grade"),
        Subject.subject_name.label("subject_name"),
    )
    .join(Grade, Grade.student_id == Student.id)
    .join(Subject, Subject.id == Grade.subject_id)
    .filter(Grade.subject_id == subject_id)
    .group_by(Student.id, Subject.subject_name)
    .order_by(desc(func.avg(Grade.grade)))
    .first()
)

if best_student:
    print(Fore.CYAN + "2. Результат select_2 (Тема: Algorithms)")
    pprint(
        [
            (
                best_student.student_name,
                float(best_student.average_grade),
                best_student.subject_name,
            )
        ]
    )
else:
    print(Fore.RED + "Немає результатів" + Style.RESET_ALL)


# 3. Знайти середній бал по групах для певного предмету
group_avrg = (
    session.query(
        Group.group_name.label("group_name"),
        func.avg(Grade.grade).label("average_grade"),
        Subject.subject_name.label("subject_name"),
    )
    .join(Student, Student.group_id == Group.id)
    .join(Grade, Grade.student_id == Student.id)
    .join(Subject, Subject.id == Grade.subject_id)
    .filter(Grade.subject_id == subject_id)
    .group_by(Group.id, Subject.subject_name)
    .order_by(Group.group_name)
    .all()
)

results = [
    (group_name, float(average_grade), subject_name)
    for group_name, average_grade, subject_name in group_avrg
]

print(Fore.YELLOW + "3. Результат select_3 (Тема: Cybersecurity)")
pprint(results)


# 4. Знайти середній бал по всіх предметах
avrg_grade = session.query(func.avg(Grade.grade)).scalar()

print(Fore.MAGENTA + "4. Результат select_4")
pprint([float(avrg_grade)])


# 5. Знайти, які курси викладає певний викладач
teacher_id = 2
courses = (
    session.query(
        Teacher.teacher_name.label("teacher_name"),
        Subject.subject_name.label("subject_name"),
    )
    .join(Subject, Subject.teacher_id == Teacher.id)
    .filter(Teacher.id == teacher_id)
    .order_by(Subject.subject_name)
    .all()
)

print(Fore.BLUE + "5. Результат select_5 (Викладач: 2)")
pprint(courses)


# 6. Знайти список студентів у конкретній групі
group_id = 3
students = (
    session.query(
        Group.group_name.label("group_name"),
        Student.student_name.label("student_name"),
    )
    .join(Student, Student.group_id == Group.id)
    .filter(Group.id == group_id)
    .order_by(Student.student_name)
    .all()
)

print(Fore.GREEN + "6. Результат select_6 (Група: Group-C)")
pprint(students)


# 7. Знайти оцінки студентів у конкретній групі по конкретному предмету
subject_id = 1
student_grades = (
    session.query(
        Group.group_name.label("group_name"),
        Student.student_name.label("student_name"),
        Subject.subject_name.label("subject_name"),
        Grade.grade,
        Grade.date_of.label("date"),
    )
    .join(Student, Student.group_id == Group.id)
    .join(Grade, Grade.student_id == Student.id)
    .join(Subject, Subject.id == Grade.subject_id)
    .filter(Group.id == group_id, Subject.id == subject_id)
    .order_by(Student.student_name)
    .all()
)

print(Fore.RED + "7. Результат select_7 (Група: Group-C, Тема: Software Engineering)")
pprint(student_grades)


# 8. Знайти середній бал, який дає конкретний викладач на своїх предметах
teacher_id = 7
avrg_grades = (
    session.query(
        Teacher.teacher_name.label("teacher_name"),
        Subject.subject_name.label("subject_name"),
        func.avg(Grade.grade).label("average_grade"),
    )
    .join(Subject, Subject.teacher_id == Teacher.id)
    .join(Grade, Grade.subject_id == Subject.id)
    .filter(Teacher.id == teacher_id)
    .group_by(Subject.id, Teacher.teacher_name)
    .order_by(Subject.subject_name)
    .all()
)

results = [
    (teacher_name, subject_name, float(average_grade))
    for teacher_name, subject_name, average_grade in avrg_grades
]

print(Fore.CYAN + "8. Результат select_8 (Викладач: Raj Koothrappali)")
pprint(results)


# 9. Знайти список курсів, які проходить конкретний студент
student_id = 4
courses = (
    session.query(
        Student.student_name.label("student_name"),
        Subject.subject_name.label("subject_name"),
    )
    .join(Grade, Grade.student_id == Student.id)
    .join(Subject, Subject.id == Grade.subject_id)
    .filter(Student.id == student_id)
    .distinct()
    .order_by(Subject.subject_name)
    .all()
)

print(Fore.YELLOW + "9. Результат select_9 (Студент: Sheldon Cooper)")
pprint(courses)


# 10. Знайти список курсів, які викладає певний викладач для конкретного студента
teacher_id = 4
teacher_courses = (
    session.query(
        Teacher.teacher_name.label("teacher_name"),
        Student.student_name.label("student_name"),
        Subject.subject_name.label("subject_name"),
    )
    .join(Subject, Subject.teacher_id == Teacher.id)
    .join(Grade, Grade.subject_id == Subject.id)
    .join(Student, Student.id == Grade.student_id)
    .filter(Teacher.id == teacher_id, Student.id == student_id)
    .distinct()
    .order_by(Subject.subject_name)
    .all()
)

print(
    Fore.MAGENTA
    + "10. Результат select_10 (Порівняння: Leonard Hofstadter і Howard Wolowitz)"
)
pprint(teacher_courses)
