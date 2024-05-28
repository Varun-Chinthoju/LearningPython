students = {
    "Name": ["Varun", "Arun", "Karun", "Maroon Franklin"],
    "Age": [12, 14, 9, 95],
    "Score": [85, 90, 78, 92],
    "Grade": ["A", "B", "C", "A"],
}

"""
Name   | Age | Score | Grade
----------------------------
Varun           | 12  | 85    | A
----------------------------
Arun            | 14  | 90    | B
Karun           | 9   | 78    | C
Maroon Franklin | 95  | 92    | A
----------------------------
"""


def get_columns_widths(data):
    columns_width = []  # [15, 2, 2, 1]
    for key in data:
        # print(key)
        max_width = 0
        for name in data[key]:
            max_width = max(max_width, len(str(name)))
        columns_width.append(max_width)
    return columns_width


# ascii box: prints a with a given x and y
# def print_ascii_box(data, x, y):
#     bottom_right_corner = "╛"
#     top_left_corner = "╒"
#     bottom_left_corner = "╘"
#     top_right_corner = "╕"
#     columns_width = []  # [15, 2, 2, 1]
#     for key in data:
#         # print(key)
#         max_width = 0
#         for name in data[key]:
#             max_width = max(max_width, len(str(name)))
#         columns_width.append(max_width)
#     for i in range(y):
#         if i == 0:
#             print(
#                 top_left_corner
#                 + ("═" * sum(columns_width))
#                 + ("╤" * (x - 1))
#                 + top_right_corner
#             )
#         if i == y - 1:
#             print("│" + (name[i] + ("" + "│" * (x - 1)) + "│"))
#             print(
#                 bottom_left_corner
#                 + ("═" * sum(columns_width))
#                 + ("╧" * (x - 1))
#                 + bottom_right_corner
#             )
#         else:
#             print("│" + (name[i] + "│" * (x - 1)) + "│")
#             print("╞" + ("╪" * (x - 1)) + "╡")


def print_table(data):
    col_widths = get_columns_widths(data)
    print("═"*sum(col_widths))
    i = 0
    for column, values in data.items():
        width = int(col_widths[i])
        print(f"|{column:<{width}}",end="")
        for u in range(4):
            print(f"│{values[u]:<{width}}",end="")
            # print("")

        # print("")
        # print(f"│{values[1]:<{width}}",end="")
        # print("")
        # print(f"│{values[2]:<{width}}",end="")
        # print("")
        # print(f"│{values[3]:<{width}}",end="")
        # print("")
        # header top line
        
        # print header
        # print("")
        # header bottom line
        i+=1
# print_ascii_box(students, 3, 3)
print_table(students)
