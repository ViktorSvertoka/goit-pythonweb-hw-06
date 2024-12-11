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

    models = {
        "Teacher": Teacher,
        "Student": Student,
        "Group": Group,
        "Subject": Subject,
    }

    try:

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

        elif args.action == "select_1":
            print(select_1())
        elif args.action == "select_2" and args.subject_id:
            print(select_2(args.subject_id))
        elif args.action == "select_3" and args.subject_id:
            print(select_3(args.subject_id))
        elif args.action == "select_4":
            print(select_4())
        elif args.action == "select_5" and args.teacher_id:
            print(select_5(args.teacher_id))
        elif args.action == "select_6" and args.group_id:
            print(select_6(args.group_id))
        elif args.action == "select_7" and args.group_id and args.subject_id:
            print(select_7(args.group_id, args.subject_id))
        elif args.action == "select_8" and args.teacher_id:
            print(select_8(args.teacher_id))
        elif args.action == "select_9" and args.student_id:
            print(select_9(args.student_id))
        elif args.action == "select_10" and args.student_id and args.teacher_id:
            print(select_10(args.student_id, args.teacher_id))
        else:
            print("Невідома команда або недостатньо параметрів.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


if __name__ == "__main__":
    main()
