#blueprint (class)
class ToDoList:
    #constructor
    def __init__(self,filename):
        print("a new to-do list created")
        self.filename=filename
        self.tasks=[]

    def add_task(self,task_name):
        new_task={"task":task_name,"done":False}
        self.tasks.append(new_task)
        print(f"added {task_name} to the {self.filename} list")
    def view_task(self):
        print(f"---tasks in {self.filename}---")
        for task in self.tasks:            
            print(f"{task['task']}")
#bundled together attribute and method -> encapsulation
#instantiating -> creating an object/instance
shopping_list=ToDoList("shopping.json")

shopping_list.add_task("Milk")
shopping_list.add_task("Eggs")
shopping_list.add_task("Bread")
shopping_list.view_task()

work_list=ToDoList("work.json")

work_list.add_task("Create python lecture")
work_list.add_task("study ml")
work_list.view_task()