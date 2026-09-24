import random

numbers = [random.randint(1, 100) for _ in range(10)]

print("List:", numbers)
print("Even numbers:", [num for num in numbers if num % 2 == 0])