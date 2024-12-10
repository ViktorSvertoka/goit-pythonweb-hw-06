import argparse
from my_select import (
    select_1,
    select_2,
    select_3,
    select_4,
    select_5,
    select_6,
    select_7,
    select_8,
    select_9,
    select_10,
)
from models import Teacher, Student, Group, Subject
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database connection
engine = create_engine(
    "postgresql+psycopg2://postgres:qwerty123@postgres_db:5432/postgres"
)
Session = sessionmaker(bind=engine)


def create_record(model, **kwargs):
    """Створення нового запису в моделі."""
    with Session() as session:
        record = model(**kwargs)
        session.add(record)
        session.commit()
        print(f"Створено запис: {record}")


def list_records(model):
    """Отримання списку записів моделі."""
    with Session() as session:
        records = session.query(model).all()
        return records


def update_record(model, record_id, **kwargs):
    """Оновлення запису за ID."""
    with Session() as session:
        record = session.query(model).get(record_id)
        if not record:
            print(f"Запис з ID {record_id} не знайдено.")
            return
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        print(f"Оновлено запис: {record}")


def remove_record(model, record_id):
    """Видалення запису за ID."""
    with Session() as session:
        record = session.query(model).get(record_id)
        if not record:
            print(f"Запис з ID {record_id} не знайдено.")
            return
        session.delete(record)
        session.commit()
        print(f"Видалено запис з ID {record_id}.")


def main():
    parser = argparse.ArgumentParser(description="CLI для роботи з базою даних")
    parser.add_argument(
        "-a", "--action", type=str, required=True, help="CRUD або вибірка"
    )
    parser.add_argument("-m", "--model", type=str, help="Модель для операцій CRUD")
    parser.add_argument("--id", type=int, help="ID запису для оновлення/видалення")
    parser.add_argument("--name", type=str, help="Ім'я (name)")
    parser.add_argument("--group_id", type=int, help="ID групи")
    parser.add_argument("--teacher_id", type=int, help="ID викладача")
    parser.add_argument("--subject_id", type=int, help="ID предмета")
    parser.add_argument("--student_id", type=int, help="ID студента")
    parser.add_argument("--value", type=float, help="Оцінка")

    args = parser.parse_args()

    # CRUD operations
    models = {
        "Teacher": Teacher,
        "Student": Student,
        "Group": Group,
        "Subject": Subject,
    }

    if args.action == "create" and args.model:
        model = models.get(args.model)
        if not model:
            print(f"Модель {args.model} не знайдена.")
            return
        kwargs = {
            k: v
            for k, v in vars(args).items()
            if k not in ["action", "model", "id"] and v is not None
        }
        create_record(model, **kwargs)

    elif args.action == "list" and args.model:
        model = models.get(args.model)
        if not model:
            print(f"Модель {args.model} не знайдена.")
            return
        records = list_records(model)
        for record in records:
            print(record)

    elif args.action == "update" and args.model and args.id:
        model = models.get(args.model)
        if not model:
            print(f"Модель {args.model} не знайдена.")
            return
        kwargs = {
            k: v
            for k, v in vars(args).items()
            if k not in ["action", "model", "id"] and v is not None
        }
        update_record(model, args.id, **kwargs)

    elif args.action == "remove" and args.model and args.id:
        model = models.get(args.model)
        if not model:
            print(f"Модель {args.model} не знайдена.")
            return
        remove_record(model, args.id)

    # SELECT queries
    elif args.action == "select_1":
        print(select_1())
    elif args.action == "select_2":
        print(select_2(args.subject_id))
    elif args.action == "select_3":
        print(select_3(args.subject_id))
    elif args.action == "select_4":
        print(select_4())
    elif args.action == "select_5":
        print(select_5(args.teacher_id))
    elif args.action == "select_6":
        print(select_6(args.group_id))
    elif args.action == "select_7":
        print(select_7(args.group_id, args.subject_id))
    elif args.action == "select_8":
        print(select_8(args.teacher_id))
    elif args.action == "select_9":
        print(select_9(args.student_id))
    elif args.action == "select_10":
        print(select_10(args.student_id, args.teacher_id))
    else:
        print("Невідома команда або недостатньо параметрів.")


if __name__ == "__main__":
    main()
