def binary_search(low, high):
    trys = 1
    happy = "\N{smiling face with sunglasses}"
    while low <= high:
        mid = (low + high) // 2
        print(f"My guess is {mid}. Is it correct, or should I guess higher or lower?")
        feedback = input()  # Get user's feedback
        if feedback == "correct":
            # be happy when the bot guesses the number
            print(happy)
            print("YESSIR I DID IT!!!!")
            print(happy)
            print("It took ", trys, " guess(es)!")
            return mid
        elif feedback == "higher":
            low = mid + 1
        elif feedback == "lower":
            high = mid - 1
        else:
            print(
                "Invalid feedback. Please respond with 'correct', 'higher', or 'lower'."
            )
        trys += 1
    print(
        "Hmm, something went wrong. I couldn't find the number based on your feedback."
    )
    return None


# Call the function
binary_search(1, 1000)
