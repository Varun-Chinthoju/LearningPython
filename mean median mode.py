def find_mean_median_mode(numbers):
    if not numbers:
        raise ValueError("Input list cannot be empty")

    mean = sum(numbers) / len(numbers)

    sorted_numbers = sorted(numbers)

    if len(sorted_numbers) % 2 == 0:
        median = (
            sorted_numbers[len(sorted_numbers) // 2 - 1]
            + sorted_numbers[len(sorted_numbers) // 2]
        ) / 2
    else:
        median = sorted_numbers[len(sorted_numbers) // 2]

    from collections import Counter

    counts = Counter(sorted_numbers)
    mode = counts.most_common(1)[0][0]
    return {"mean": mean, "median": median, "mode": mode}


numbers = [12, 11, 7, 14, 13, 48, 42, 45, 10, 47, 12]
results = find_mean_median_mode(numbers)
print(results)
