# stores all your todo tiems and prints them
todo_list = []

while True:
    todo = input("Add a TODO: ")
    if todo == "":
        break

    todo_list.append(todo)

print("Your TODOs are below:")

for t in todo_list:
    print(t)
