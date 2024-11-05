
def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    >>> largest_divisor(1)
    0
    >>> largest_divisor(-15)
    -1
    >>> largest_divisor(0)
    0
    >>> largest_divisor(1000000000000)
    500000000000
    """
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n < 0:
        return -1  # or handle negative numbers differently if needed
    for i in range(n-1, 0, -1):
        if n % i == 0:
            return i

# Test cases
print(largest_divisor(15))  # Expected output: 5
print(largest_divisor(1))   # Expected output: 0
print(largest_divisor(-15)) # Expected output: -1
print(largest_divisor(0))   # Expected output: 0
print(largest_divisor(1000000000000))  # Expected output: 500000000000
