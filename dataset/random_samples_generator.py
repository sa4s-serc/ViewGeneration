'''
This script generates unique random numbers between 1 and 340. 
It ensures that each number is used only once by maintaining a list of available numbers and removing them as they are used.
When all numbers have been used, it raises an error.
'''
import random

numbers = list(range(1, 341))
random.shuffle(numbers)

def get_unique_random_number():
    if not numbers:
        raise ValueError("All numbers have been used!")
    return numbers.pop()

# Example usage:
print(get_unique_random_number())  
