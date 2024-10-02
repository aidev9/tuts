import matplotlib.pyplot as plt

def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Calculate the first 10 Fibonacci numbers
fib_numbers = fibonacci(10)

# Plotting the Fibonacci numbers in a bar chart
plt.bar(range(1, 11), fib_numbers)
plt.xlabel('Position in Fibonacci Sequence')
plt.ylabel('Fibonacci Number')
plt.title('First 10 Fibonacci Numbers')
plt.show()