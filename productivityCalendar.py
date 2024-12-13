import datetime
import json
import os
from pathlib import Path

# Create a subdirectory named 'calendars' if it doesn't exist.
SUBDIR = "calendars"
subdir_path = Path(SUBDIR)
if not os.path.exists(SUBDIR):
    os.makedirs(SUBDIR)

class Task:
    def __init__(self,description):
        self.description = description
        self.completed = False

    def complete(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "x"
        return f"{self.description}[{status}]"
    
class Day:
    def __init__(self,date):
        self.date = date
        self.tasks = []

    def add_task(self,description):
        task = Task(description)
        self.tasks.append(task)

    def list_tasks(self):
        if not self.tasks:
            print("There are no tasks for this day.")
        else:
            for i, task in enumerate(self.tasks,start=1):
                print(f"{i}) {task}")
    
    def complete_task(self, task_no):
        if task_no < 0 or task_no > len(self.tasks):
            print("There is no task matching the description.")
        else:
            self.tasks[task_no - 1].complete()
        

class Calendar:
    def __init__(self, calendar_name):
        self.name = calendar_name
        self.calendar_path = subdir_path / f"{self.name}.json"
        self.days = {}
    
    def add_task(self, date, description):
        # Adds 'Today'. 'Tomorrow' and 'Yesterday' keywords.
        if date.lower() == "today":
            today = datetime.date.today()
            date = today.strftime("%d/%m/%Y")
        elif date.lower() == "tomorrow":
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            date = tomorrow.strftime("%d/%m/%Y")
        elif date.lower() == "yesterday":
            today = datetime.date.today()
            yesterday = today + datetime.timedelta(days=-1)
            date = yesterday.strftime("%d/%m/%Y")
        
        if date not in self.days:
            self.days[date] = Day(date)
        self.days[date].add_task(description)
    
    def complete_task(self, date, task_no):
        if date not in self.days:
            print("There is no task for this date.")
        else:
            self.days[date].complete_task(task_no)
            print("Task completed successfully.")
            
    def list_all_tasks(self):
        if not self.days:
            print("There are not tasks in the calendar.")
        else:
            for date, day in sorted(self.days.items()):
                print(f"\n{date}")
                day.list_tasks()

    def create_calendar(self):
        # Checks for an existing calendar.
        if self.calendar_path.exists():
            print("There is an existing calendar with that name, what would you like to do?\n1. Load it.\n2. Overwrite it.")
            while True:
                choice = input ("Your choice: ")
                match choice:
                    case "1":
                        self.load_calendar()
                        return
                    case "2":
                        self.save_calendar()
                        return
                    case _:
                        print("Option not valid, try again")
        else: 
            self.save_calendar()

    def save_calendar(self):
        data = {}
        for date, day in self.days.items():
            data[date] = [
                {"description": task.description, "completed": task.completed} for task in day.tasks
            ]
        try:
            with open(self.calendar_path, "w") as file:
                json.dump(data, file, indent=4)
            print("Calendar saved successfully.")
        except:
            print("An error ocurred while saving the calendar.")
    
    def delete_calendar(self):
        if not self.calendar_path.exists():
            print("There is not an existing calendar with that name.")
        else:
            while True:
                choice = input(f"\nYou are about to delete {self.name} calendar. Are you sure? (y/n) ")
                match choice:
                    case "y":
                        self.calendar_path.unlink()
                        print(f"Calendar {self.name} has been deleted.")
                        return
                    case "n":
                        print("Operation aborted.")
                        return
                    case _:
                        print("Option not valid, please try again and use lowercase.")
                
    def load_calendar(self):
        if not self.calendar_path.exists():
            while True:
                choice = input("There is not an existing calendar with that name, would you like to create one? (y/n) ")
                match choice:
                    case "y":
                        self.save_calendar()
                        return
                    case "n":
                        return
                    case _:
                        print("Option not valid, try again. Use lowercase letters only.")
        else:
            with open(self.calendar_path, "r") as file:
                data = json.load(file)
                for date, tasks in data.items():
                    day = Day(date)
                    for task_data in tasks:
                        task = Task(description=task_data["description"])
                        if task_data["completed"]:
                            task.complete()
                        day.tasks.append(task)
                    self.days[date] = day
                print("Calendar sucessfully loaded.")

    def list_all_calendars(self):
        calendar_files = list(subdir_path.glob("*.json"))
        if calendar_files:
            print("Calendars available:\n")
            for calendar_file in calendar_files:
                print(calendar_file.stem)
        else:
            print("No calendars found.\n")

       
print("=== PRODUCTIVITY CALENDAR ===")
while True:
    print("\nChoose an option:\n1. See existing calendars.\n2. Create a new calendar.\n3. Open an existing calendar.\n4. Delete an existing calendar.\n5. Stop program.")
    choice = input("\nYour choice: ")
    print("\n")
    flag = False
    match choice:
        case "1":
            calendar = Calendar('calendar')
            calendar.list_all_calendars()
        case "2":
            calendar_name = input("\nName of the calendar you want to create: ") 
            calendar_name = Calendar(calendar_name)
            calendar_name.create_calendar()
        case "3":
            calendar_name = input("\nName of the calendar you want to open: ")
            calendar_name = Calendar(calendar_name)
            calendar_name.load_calendar()
            flag = True
        case "4":
            calendar_name = input("\nName of the calendar you want to delete: ")
            calendar_name = Calendar(calendar_name)
            calendar_name.delete_calendar()
        case "5":
            print("Program ended successfully. Goodbye!")
            break
        case _:
            print("Option not valid, try again.")

    while flag:
        print("\nChoose an option:\n1. See all tasks.\n2. Create a task.\n3. Complete a task.\n4. Save and return to calendar choice.")
        choice = input("\nYour choice: ")
        match choice:
            case "1":
                calendar_name.list_all_tasks()
            case "2":
                date = input("\nSelect the date: ")
                description = input("Task description: ")
                calendar_name.add_task(date, description)
            case "3":
                calendar_name.list_all_tasks()
                date = input("\nSelect a date: ")
                task_no = int(input("Select task number: "))
                calendar_name.complete_task(date, task_no - 1)
            case "4":
                calendar_name.save_calendar()
                break
            case _:
                print("Option not valid, try again.")