# ascii box: prints a with a given x and y
def print_ascii_box(x, y):
    for i in range(y):
        if i == 0 or i == y - 1:
            print("+" + "-" * (x - 2) + "+")
        else:
            print("|" + " " * (x - 2) + "|")


print_ascii_box(10, 10)
