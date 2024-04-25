fibonacci = 1
copy_fibonacci = 0
print_var = 0
count = 0
print(copy_fibonacci)
print(fibonacci)
while count <= 10:
    print_var = copy_fibonacci + fibonacci
    print(print_var)
    copy_fibonacci = fibonacci
    fibonacci = print_var
    count += 1
