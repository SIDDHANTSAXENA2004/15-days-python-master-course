# project -> to do list
# add task
# view all task
# quit app


tasks=[]

# {"task":"Buy milk","done":False}

while True:
  print("\n---To-Do List Menu ---")
  print("1.Add a new task")
  print("2. View all tasks")
  print("3. Quit")

  choice=int(input("Enter your choice (1,2,3): "))
  if choice==1:
    task_name=input("enter the task description: ")
    new_task={
        "task":task_name,
        "done":False
    }
    tasks.append(new_task)
    print("Task added successfully!")
  elif choice==2:
    if not tasks:
      print("No tasks found.")
    else:
      print("\n---To-Do List---")
      for i,task in enumerate(tasks,start=1):
        status="Done" if task["done"] else "Not Done"
        print(f"{i}. {task['task']} - {status}")
  elif choice==3:
    print("Goodbye!")
    break
  else:
    print("Invalid choice. Please select a valid option.")
