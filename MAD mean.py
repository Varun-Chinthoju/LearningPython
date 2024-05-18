def mad(data):
    mean = sum(data) / len(data)
    abs_diff = [abs(x - mean) for x in data]
    mad = sum(abs_diff) / len(abs_diff)
    return mad

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(mad(data))