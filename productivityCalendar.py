import json
FILE_NAME = "productivityCalendar.json"

class Task:
    def __init__(self,description):
        self.description = description
        self.completed = False

    def complete(self):
        self.completed = True

    def __str__(self):
        status = "✔" if self.completed else "x"
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
        if task_no < 0 | task_no > len(self.tasks):
            print("There is no task matching the description.")
        else:
            self.tasks[task_no - 1].complete()
        

class Calendar:
    def __init__(self):
        self.days = {}
    
    def add_task(self, date, description):
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
            for date, day in self.days.items():
                print(f"\n{date}")
                day.list_tasks()
                
    def load_calendar(self):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                print("Calendar sucessfully loaded.")
                pass
        except FileNotFoundError:
            print(f"File {FILE_NAME} not found. A empty calendar will be used.")
            return {}