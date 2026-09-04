from app.schedule import ScheduleManager

VALID_DAYS = {
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
}


def get_positive_int(prompt: str):
    """Prompt until a valid positive integer is entered, or return None on empty cancel."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Input cannot be empty. Please try again (or leave blank again to cancel).")
            raw = input(prompt).strip()
            if not raw:
                return None
        try:
            value = int(raw)
            if value <= 0:
                print("Please enter a positive integer (greater than 0).")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_valid_day(prompt: str = "Enter day (e.g., Monday): "):
    """Prompt for a valid weekday name (case-insensitive)."""
    while True:
        day = input(prompt).strip()
        if not day:
            print("Day cannot be empty.")
            continue
        if day.lower() in VALID_DAYS:
            return day.capitalize()
        print(f"Invalid day. Please enter one of: {', '.join(sorted(d.capitalize() for d in VALID_DAYS))}")


def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons = manager.get_lessons_for_day(day)
    if not lessons:
        print("No lessons scheduled for that day.")
        return

    print(f"{'Course':<25} {'Instrument':<15} {'Time':<10} {'Teacher ID':<12}")
    print("-" * 65)
    for course, lesson in lessons:
        time_str = lesson.get("time", "N/A")
        print(f"{course.name:<25} {course.instrument:<15} {time_str:<10} {course.teacher_id:<12}")


def switch_course(manager, student_id, from_course_id, to_course_id):
    """Switch a student from one course to another via the manager."""
    if student_id is None or from_course_id is None or to_course_id is None:
        print("Switch cancelled due to missing input.")
        return

    if from_course_id == to_course_id:
        print("From and To course IDs are the same. No change needed.")
        return

    student = manager.find_student_by_id(student_id)
    if not student:
        print(f"Error: Student ID {student_id} does not exist.")
        return

    from_course = manager.find_course_by_id(from_course_id)
    if not from_course:
        print(f"Error: From Course ID {from_course_id} does not exist.")
        return

    to_course = manager.find_course_by_id(to_course_id)
    if not to_course:
        print(f"Error: To Course ID {to_course_id} does not exist.")
        return

    if from_course_id not in student.enrolled_course_ids:
        print(f"Error: Student {student.name} is not enrolled in course {from_course_id}.")
        return

    success = manager.switch_student_course(student_id, from_course_id, to_course_id)
    if success:
        print(f"Student {student.name} (ID {student_id}) successfully switched "
              f"from '{from_course.name}' to '{to_course.name}'.")
    else:
        print("Switch failed unexpectedly. Please check the data.")


def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager()

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. Daily Roster")
        print("2. Student Check-in")
        print("3. Switch Student Course")
        print("q. Quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == "1":
            day = get_valid_day()
            if day:
                front_desk_daily_roster(manager, day)

        elif choice == "2":
            student_id = get_positive_int("Student ID: ")
            if student_id is None:
                print("Check-in cancelled.")
                continue

            course_id = get_positive_int("Course ID: ")
            if course_id is None:
                print("Check-in cancelled.")
                continue

            if not manager.find_student_by_id(student_id):
                print(f"Error: Student ID {student_id} does not exist.")
                continue
            if not manager.find_course_by_id(course_id):
                print(f"Error: Course ID {course_id} does not exist.")
                continue

            manager.check_in(student_id, course_id)

        elif choice == "3":
            student_id = get_positive_int("Student ID: ")
            if student_id is None:
                print("Switch cancelled.")
                continue

            from_id = get_positive_int("From Course ID: ")
            if from_id is None:
                print("Switch cancelled.")
                continue

            to_id = get_positive_int("To Course ID: ")
            if to_id is None:
                print("Switch cancelled.")
                continue

            switch_course(manager, student_id, from_id, to_id)

        elif choice == "q":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or q.")


if __name__ == "__main__":
    main()