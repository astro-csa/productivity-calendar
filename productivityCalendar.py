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
    
    def complete_task(self,task):
        pass

class Calendar:
    def __init__(self):
        pass

print("====PRODUCTIVITY CALENDAR====")
print("Select an option:")
print("1. Print existing calendars.")
print("2. Add a calendar.")
choice = input("Your choice: ")

match choice:
    case "1":
        print("You chose option 1.")
    case "2":
        print("You chose option 2")
    case _:
        print("You are stupid...")

print(f"{choice}")
