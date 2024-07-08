import customtkinter
import json

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.saveTasksToJSON)

        self.taskList = []

        self.geometry("500x500")
        self.title("Todo App")
        self.columnconfigure(0, weight=1)

        self.titleLabel = customtkinter.CTkLabel(self, text="Todo App", font=("Arial", 30))
        self.titleLabel.grid(row=0, column=0, pady=10)

        self.inputEntry = customtkinter.CTkEntry(self, placeholder_text="Enter task", width=300, height=40, font=("Arial", 20))
        self.inputEntry.grid(row=1, column=0, pady=10)

        self.addButton = customtkinter.CTkButton(self, text="Add", command=lambda: self.addTask(self.inputEntry.get()), font=("Arial", 20))
        self.addButton.grid(row=2, column=0)

        self.tasksFrame = customtkinter.CTkScrollableFrame(self, height=300)
        self.tasksFrame.grid(row=3, column=0, pady=20, padx=20, sticky="ew")

        self.retrieveTasksFromJSON()

    def addTask(self, text):
        if text == "":
            return
        checkbox = customtkinter.CTkCheckBox(self.tasksFrame, text=text, font=("Arial", 20), command=lambda: self.deleteTask(checkbox),
                                     variable=customtkinter.StringVar(value="off"), onvalue="on", offvalue="off")
        checkbox.pack(pady=5, padx=(100,0), fill="both", expand=True)
        self.inputEntry.delete(0, "end")

        self.taskList.append(checkbox)
    
    def deleteTask(self, checkbox):
        for task in self.taskList:
            if task == checkbox:
                self.taskList.remove(task)
                self.after(500, task.destroy)
    
    def saveTasksToJSON(self):
        toSave = []
        for task in self.taskList:
            toSave.append(task.cget("text"))

        with open('tasks.json', 'w') as f:
            json.dump({"tasks": toSave}, f)

        self.destroy()

    def retrieveTasksFromJSON(self):
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)["tasks"]
            
        for task in tasks:
            self.addTask(task)

app = App()
app.mainloop()