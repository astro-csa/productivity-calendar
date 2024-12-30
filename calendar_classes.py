import datetime
import json
import shutil
from pathlib import Path

calendars_dir = Path("data") # Directory for storing calendar files

class Task:
    """Represents a task with a description, completion status, and recurrence."""
    def __init__(self, description):
        self.description = description
        self.completed = False

    def complete(self):
        """Marks the task as completed."""
        self.completed = True

    def __str__(self):
        """Returns a string representation of the task with its status."""
        status = "✓" if self.completed else "x"
        return f"{self.description}[{status}]"

class Day:
    """Represents a day with a date and a list of tasks."""
    def __init__(self, date):
        self.date = date
        self.tasks = []

    def add_task(self, description):
        """Adds a new task to the day's task list."""
        task = Task(description)
        self.tasks.append(task)

    def delete_task(self, task_no):
        """Deletes a task from the day's task list by its number."""
        if task_no < 0 or task_no > len(self.tasks):
            print("There is no task matching the description.")
        else:
            del self.tasks[task_no - 1]

    def complete_task(self, task_no):
        """Marks a task as completed by its number."""
        if task_no < 0 or task_no > len(self.tasks):
            print("There is no task matching the description.")
        else:
            self.tasks[task_no - 1].complete()

    def list_tasks(self):
        """Prints all tasks for the day."""
        if not self.tasks:
            print("There are no tasks for this day.")
        else:
            for i, task in enumerate(self.tasks, start=1):
                print(f"{i}) {task}")

class Calendar:
    """Represents a calendar with multiple days and tasks."""
    def __init__(self, path):
        self.calendar_path = calendars_dir / path
        self.days = {}
        self.recurrent_tasks = {}

    def _handle_recurrence(self, start_date, description, recurrence, end_date):
        """Generates recurring tasks."""
        start_date_obj = datetime.datetime.strptime(start_date,"%d/%m/%Y").date()
        end_date_obj = datetime.datetime.strptime(end_date,"%d/%m/%Y").date()
        delta = datetime.timedelta(days=1) if recurrence == "d" else datetime.timedelta(weeks=1)

        current_date = start_date_obj + delta
        while current_date <= end_date_obj:
            date_str = current_date.strftime("%d/%m/%Y")
            if date_str not in self.days:
                self.days[date_str] = Day(date_str)
            self.days[date_str].add_task(description,recurrence)
            current_date += delta

    @staticmethod
    def shiftted_day(shift=0):
        """
        Return today's date shifted by the given amount as a formatted string (dd/mm/yyyy).
        """
        day = datetime.date.today() + datetime.timedelta(days=shift)
        return day.strftime("%d/%m/%Y")
    
    @classmethod
    def create_calendar(cls, calendar):
        """Creates a new calendar or loads an existing one."""
        if not calendars_dir.exists():
            calendars_dir.mkdir()
        calendar_path = calendars_dir / calendar
        if calendar_path.exists():
            print("There is an existing calendar with that name, what would you like to do?\n1. Load it.\n2. Overwrite it.")
            while True:
                choice = input("Your choice: ")
                match choice:
                    case "1":
                        return Calendar.load_calendar(calendar)
                    case "2":
                        shutil.rmtree(calendar_path)
                        break
                    case _:
                        print("Option not valid, try again")
        calendar_path.mkdir()
        with open(calendar_path / "calendar.json", "w") as file: # Creates an empty file
            pass
        print(f"Calendar '{calendar}' succesfully created.")

    @classmethod
    def load_calendar(cls, calendar):
        """Loads the calendar from a JSON file."""
        calendar_path = calendars_dir / calendar
        if not calendar_path.exists():
            while True:
                choice = input("There is no existing calendar with that name, would you like to create one? (y/n) ")
                match choice:
                    case "y":
                        Calendar.create_calendar(calendar)
                        return
                    case "n":
                        return
                    case _:
                        print("Option not valid, try again. Use lowercase letters only.")
        else:
            calendar_obj = Calendar(calendar)
            try:
                with open(calendar_path / "calendar.json", "r") as file:
                    data = json.load(file)
                    for date, tasks in data.items():
                        day = Day(date)
                        for task_data in tasks:
                            task = Task(description=task_data["description"])
                            if task_data["completed"]:
                                task.complete()
                            day.tasks.append(task)
                        calendar_obj.days[date] = day
            except json.decoder.JSONDecodeError:
                pass
            
            print("Calendar successfully loaded.")
            return calendar_obj

    @classmethod
    def delete_calendar(cls, calendar):
        """Deletes the calendar file."""
        calendar_path = calendars_dir / calendar
        if not calendar_path.exists():
            print("There is no existing calendar with that name.")
        else:
            while True:
                choice = input(f"\nYou are about to delete {calendar} calendar. Are you sure? (y/n) ")
                match choice:
                    case "y":
                        shutil.rmtree(calendar_path)
                        print(f"Calendar {calendar} has been deleted.")
                        return
                    case "n":
                        print("Operation aborted.")
                        return
                    case _:
                        print("Option not valid, please try again and use lowercase.")

    @classmethod
    def list_all_calendars(cls):
        """Lists all calendar files in the subdirectory."""
        try:
            data = list(calendars_dir.iterdir())
            if data:
                print("Calendars available:\n")
                for calendar_file in data:
                    print(calendar_file.name)
            else:
                print("No calendars found.\n")
        except FileNotFoundError:
            print("There are no calendars and 'data' directory is not created.\n")

    def save_calendar(self):
        """Saves the calendar to a JSON file."""
        try:
            with open(self.calendar_path / "recurrency.json", "w") as file:
                json.dump(self.recurrent_tasks, file, indent=4)
            print("Recurrency saved successfully.")
        except:
            print("An error occurred while saving the calendar."),
        
        data = {}
        for date, day in self.days.items():
            data[date] = [
                {"description": task.description, "completed": task.completed} for task in day.tasks
            ]
        try:
            with open(self.calendar_path / "calendar.json", "w") as file:
                json.dump(data, file, indent=4)
            print("Calendar saved successfully.")
        except:
            print("An error occurred while saving the calendar.")

    def add_task(self, date, description, recurrence=0, end_date=0):
        """Adds a task to a specified date in the calendar."""
        # Handle 'Today', 'Tomorrow', and 'Yesterday' keywords.
        if date.lower() == "today":
            date = self.shiftted_day()
        elif date.lower() == "tomorrow":
            date = self.shiftted_day(1)
        elif date.lower() == "yesterday":
            date = self.shiftted_day(-1)

        # Check if the provided recurrence option is valid
        if not isinstance(recurrence,int) or recurrence < 0:
            print("Invalid recurrence option. It must be a positive integer.")
            return
        if recurrence > 0:
            self.recurrent_tasks[description] = {"description": description, "recurrence": recurrence, "start date": date, "end date": end_date}
        if date not in self.days:
            self.days[date] = Day(date)
        self.days[date].add_task(description)

    def delete_task(self, date, task_no):
        """Deletes a task from a specified date in the calendar."""
        if date.lower() == "today":
            date = self.shiftted_day()
        elif date.lower() == "tomorrow":
            date = self.shiftted_day(1)
        elif date.lower() == "yesterday":
            date = self.shiftted_day(-1)

        if date not in self.days:
            print("There are no tasks for this date.")
        else:
            self.days[date].delete_task(task_no)
            print("Task deleted successfully.")
            # Deletes empty days
            if not self.days[date].tasks:
                del self.days[date]

    def complete_task(self, date, task_no):
        """Marks a task as completed for a specified date in the calendar."""
        # Handle 'Today', 'Tomorrow', and 'Yesterday' keywords.
        if date.lower() == "today":
            date = self.shiftted_day()
        elif date.lower() == "tomorrow":
            date = self.shiftted_day(1)
        elif date.lower() == "yesterday":
            date = self.shiftted_day(-1)

        if date not in self.days:
            print("There are no tasks for this date.")
        else:
            self.days[date].complete_task(task_no)

    def list_week_tasks(self):
        """Lists all tasks for the current week."""
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        current_week = []
        for i in range(7):
            day = monday + datetime.timedelta(days=i)
            current_week.append(day.strftime("%d/%m/%Y"))
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        flag = False
        for date, day in sorted(self.days.items()):
            if date == self.shiftted_day(0):
                print(f"\n{weekdays[datetime.datetime.strptime(date, '%d/%m/%Y').weekday()]} {date} (Today)")
                flag = True
                day.list_tasks()
            elif date != today and date in current_week:
                print(f"\n{weekdays[datetime.datetime.strptime(date, '%d/%m/%Y').weekday()]} {date}")
                flag = True
                day.list_tasks()
        if not flag:
            print("There are no tasks for the current week.")

    def list_all_tasks(self):
        """Lists all tasks in the calendar."""
        if not self.days:
            print("There are no tasks in the calendar.")
        else:
            for date, day in sorted(self.days.items()):
                if date == self.shiftted_day(0):
                    print(f"\n{date} (Today)")
                else:
                    print(f"\n{date}")
                day.list_tasks()