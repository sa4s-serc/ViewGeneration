import random

numbers = list(range(1, 341))
random.shuffle(numbers)

def get_unique_random_number():
    if not numbers:
        raise ValueError("All numbers have been used!")
    return numbers.pop()

# Example usage:
print(get_unique_random_number())  
