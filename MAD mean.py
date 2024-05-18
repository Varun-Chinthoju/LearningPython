def mad(data):
    mean = sum(data) / len(data)
    print("Mean = ", mean)
    abs_diff = [abs(x - mean) for x in data]
    mad = sum(abs_diff) / len(abs_diff)
    return mad

data = [75, 2, 483, 58, 5, 66, 537, 8, 987]
print(mad(data))