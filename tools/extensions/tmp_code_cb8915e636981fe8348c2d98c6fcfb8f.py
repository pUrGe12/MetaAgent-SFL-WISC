
def is_prime(num):
    """Helper function to check if a number is prime."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_fib(n: int):
    """
    prime_fib returns n-th number that is a Fibonacci number and it's also prime.
    >>> prime_fib(1)
    2
    >>> prime_fib(2)
    3
    >>> prime_fib(3)
    5
    >>> prime_fib(4)
    13
    >>> prime_fib(5)
    89
    """
    prime_fibs = []
    a, b = 1, 1
    while len(prime_fibs) < n:
        a, b = b, a + b
        if is_prime(b):
            prime_fibs.append(b)
    return prime_fibs[n - 1]

# Unit tests
def test_prime_fib():
    # Basic test cases
    assert prime_fib(1) == 2
    assert prime_fib(2) == 3
    assert prime_fib(3) == 5
    assert prime_fib(4) == 13
    assert prime_fib(5) == 89
    
    # Edge test cases
    assert prime_fib(6) == 233
    assert prime_fib(7) == 1597
    
    # Large-scale test cases
    print("prime_fib(10):", prime_fib(10))  # Debugging output
    print("prime_fib(15):", prime_fib(15))  # Debugging output
    
    print("All tests passed!")

# Run the tests
test_prime_fib()
