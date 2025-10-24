import json
import os
class ToDoList:
    #constructor
    def __init__(self,filename):
        print("a new to-do list created")
        self.filename=filename
        self.tasks=self.load_tasks()
    
    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error loading tasks from file.")
            return []
    
    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)
        print("Tasks saved successfully!")
    def add_task(self,task_name):
        new_task={"task":task_name,"done":False}
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"task added {task_name} ")
    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
        else:
            print("\n---To-Do List---")
            for index, task in enumerate(self.tasks, start=1):
                status = "[X]" if task["done"] else "[]"
                print(f"{index}. {task['task']} - {status}")
    def mark_task_done(self):
        self.view_tasks()
        try:
            task_index=int(input("Enter the task number to mark as done: "))
            if 1 <= task_index <= len(self.tasks):
                self.tasks[task_index-1]["done"] = True
                print("Task marked as done!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")

#------------------------------------
def main_menu():
    my_app=ToDoList("my_tasks.json")
    while True:
        print("\n---To-Do List Menu ---")
        print("1.Add a new task")
        print("2. View all tasks")
        print("3. Mark a task as done")
        print("4. Quit")

        choice=input("Enter your choice (1,2,3,4): ")
        if choice=="1":
            task_name=input("enter the task description: ")
            my_app.add_task(task_name)
        elif choice=="2":
            my_app.view_tasks()
        elif choice=="3":
            my_app.mark_task_done()
        elif choice=="4":
            my_app.save_tasks()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()