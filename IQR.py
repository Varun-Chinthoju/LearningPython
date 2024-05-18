def find_iqr_quartiles(numbers):
  if not numbers:
    raise ValueError("Input list cannot be empty")

  sorted_numbers = sorted(numbers)

  median_index = len(sorted_numbers) // 2
  median = sorted_numbers[median_index]

  if len(sorted_numbers) % 2 == 0:
    Q1_index = (median_index - 1) // 2
  else:
    Q1_index = median_index // 2
  Q1 = sorted_numbers[Q1_index]

  if len(sorted_numbers) % 2 == 0:
    Q3_index = median_index + (len(sorted_numbers) // 2) // 2
  else:
    Q3_index = median_index + (median_index // 2) + 1
  Q3 = sorted_numbers[Q3_index]

  IQR = Q3 - Q1

  return {"IQR": IQR, "Q1": Q1, "Q3": Q3}

numbers = [65, 63, 63, 61, 59, 58, 60, 64, 49, 61, 62, 67]
results = find_iqr_quartiles(numbers)
print(results)