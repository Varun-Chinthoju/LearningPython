import random

def roll_dice(num_dice, num_sides):
  rolls = []
  for _ in range(num_dice):
    rolls.append(random.randint(1, num_sides))
  return rolls

def main():
  while True:
    try:
      num_dice = int(input("Enter number of dice (or 'q' to quit): "))
      if num_dice == 'q':
        break
      num_sides = int(input("Enter number of sides on each die: "))
      if num_sides <= 0:
        raise ValueError
      break
    except ValueError:
      print("Invalid input. Enter positive integers for number of dice and sides.")

  roll_results = roll_dice(num_dice, num_sides)
  print(f"You rolled {num_dice}d{num_sides}: {roll_results}")

if __name__ == "__main__":
  main()