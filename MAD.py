def find_mad(numbers):
    if not numbers:
        raise ValueError("Input list cannot be empty")

    sorted_numbers = sorted(numbers)
    median_index = len(sorted_numbers) // 2
    median = (
        sorted_numbers[median_index]
        if len(sorted_numbers) % 2 == 0
        else sorted_numbers[median_index // 2]
    )

    deviations = [abs(num - median) for num in numbers]

    mad_sorted = sorted(deviations)
    mad_index = len(mad_sorted) // 2
    mad = (
        mad_sorted[mad_index]
        if len(mad_sorted) % 2 == 0
        else mad_sorted[mad_index // 2]
    )

    return mad


numbers = [1, 2, 3, 3, 5, 7, 8, 9]
mad_value = find_mad(numbers)
print(f"Median Absolute Deviation (MAD): {mad_value}")
