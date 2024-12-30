from calendar_classes import Calendar

def main():
    calendar_obj = None
    print("=== PRODUCTIVITY CALENDAR ===")
    while True:
        print("\nChoose an option:\n1. See existing calendars.\n2. Create a new calendar.\n3. Open an existing calendar.\n4. Delete an existing calendar.\n5. Stop program.")
        choice = input("\nYour choice: ")
        print("\n")
        match choice:
            case "1":
                Calendar.list_all_calendars()
            case "2":
                calendar_name = input("Name of the calendar you want to create: ")
                calendar_obj = Calendar.create_calendar(calendar_name) # Returns true if it is able to create the calendar
            case "3":
                calendar_name = input("Name of the calendar you want to open: ")
                calendar_obj = Calendar.load_calendar(calendar_name)
            case "4":
                calendar_name = input("Name of the calendar you want to delete: ")
                Calendar.delete_calendar(calendar_name)
            case "5":
                print("Program ended successfully. Goodbye!")
                break
            case _:
                print("Option not valid, try again.")

        while calendar_obj:
            print("\nChoose an option:\n1. See current week tasks.\n2. See all tasks.\n3. Create a task.\n4. Complete a task.\n5. Delete a task.\n6. Save and return to calendar choice.")
            choice = input("\nYour choice: ")
            match choice:
                case "1":
                    calendar_obj.list_week_tasks()
                case "2":
                    calendar_obj.list_all_tasks()
                case "3":
                    date = input("\nSelect the date: ")
                    description = input("Task description: ")
                    recurrent = input("Is it recurrent? (y/n) ")
                    if recurrent.lower() == "y":
                        recurrence = int(input("Task recurrence: "))
                    else:
                        recurrence = 0
                    calendar_obj.add_task(date, description, recurrence)
                case "4":
                    calendar_obj.list_all_tasks()
                    date = input("\nSelect a date: ")
                    task_no = int(input("Select task number: "))
                    calendar_obj.complete_task(date, task_no - 1)
                case "5":
                    calendar_obj.list_all_tasks()
                    date = input("\nSelect a date: ")
                    task_no = int(input("Select task number: "))
                    calendar_obj.delete_task(date, task_no - 1)
                case "6":
                    calendar_obj.save_calendar()
                    calendar_obj = None
                case _:
                    print("Option not valid, try again.")

if __name__ == "__main__":
    main()