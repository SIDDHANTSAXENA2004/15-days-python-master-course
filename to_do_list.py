import json
import os

TASKS_FILE = "tasks.json"

#tasks=[{"task":"Buy milk","done":False},{"task":"Buy eggs","done":False},{"task":"Buy bread","done":False}]
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error loading tasks from file.")
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
    print("Tasks saved successfully!")

def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        print("\n---To-Do List---")
        for index, task in enumerate(tasks, start=1):
            status = "[X]" if task["done"] else "[]"
            print(f"{index}. {task['task']} - {status}")

def add_task(tasks):
    task_name=input("enter the task description: ")
    new_task={
        "task":task_name,
        "done":False
    }
    tasks.append(new_task)
    print("Task added successfully!")
    
def mark_task_done(tasks):
    view_tasks(tasks)
    try:
        task_index=int(input("Enter the task number to mark as done: "))
        if 1 <= task_index <= len(tasks):
            tasks[task_index-1]["done"] = True
            print("Task marked as done!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

def main():
    tasks=load_tasks()
    while True:
        print("\n---To-Do List Menu ---")
        print("1.Add a new task")
        print("2. View all tasks")
        print("3. Mark a task as done")
        print("4. Quit")

        choice=input("Enter your choice (1,2,3,4): ")
        if choice=="1":
            add_task(tasks)
            save_tasks(tasks)
        elif choice=="2":
            view_tasks(tasks)
        elif choice=="3":
            mark_task_done(tasks)
            save_tasks(tasks)
        elif choice=="4":
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()