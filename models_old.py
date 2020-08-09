import json


 class projects:
     def __init__(self):
         try:
             with open("projects.json", "r") as f:
                 self.projects = json.load(f)
         except FileNotFoundError:
             self.projects = []

     def all(self):
         return self.projects

     def get(self, id):
         return self.projects[id]
         todo = [todo for todo in self.all() if todo['id'] == id]
         if todo:
             return todo[0]
         return []

     def create(self, data):
         self.projects.append(data)
         self.save_all()

     def save_all(self):
         with open("projects.json", "w") as f:
             json.dump(self.projects, f)

     def update(self, id, data):
         todo = self.get(id)
         if todo:
             index = self.projects.index(todo)
             self.projects[index] = data
             self.save_all()
             return True
         return False


     def delete(self, id):
         todo = self.get(id)
         if todo:
             self.projects.remove(todo)
             self.save_all()
             return True
         return False


 projects = projects(