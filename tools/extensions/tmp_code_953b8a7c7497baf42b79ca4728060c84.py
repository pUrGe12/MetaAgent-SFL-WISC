
def is_simple_power(x, n):
    if not isinstance(x, (int, float)) or not isinstance(n, (int, float)):
        raise ValueError("Both x and n must be numeric values.")
    if n == 0:
        return x == 1
    if n == 1:
        return x == 1
    if x == 1:
        return True
    if x <= 0 or n <= 0:
        return False
    power = 1
    while power < x:
        power *= n
    return power == x

# Test cases
print(is_simple_power(1, 4))  # True
print(is_simple_power(2, 2))  # True
print(is_simple_power(8, 2))  # True
print(is_simple_power(3, 2))  # False
print(is_simple_power(3, 1))  # False
print(is_simple_power(5, 3))  # False

# Edge cases
print(is_simple_power(-8, -2))  # False
print(is_simple_power(0, 0))    # True
print(is_simple_power(0, 2))    # False
print(is_simple_power(2, 0))    # False
print(is_simple_power(16, 2.0)) # True
print(is_simple_power(16.0, 2)) # True
print(is_simple_power(16.0, 2.0)) # True
print(is_simple_power(1.5, 2))  # False
print(is_simple_power(2, 1.5))  # False

# Non-numeric inputs
try:
    print(is_simple_power(2, 'a'))  # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power('a', 2))  # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, None)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(None, 2)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, [2]))  # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power([2], 2))  # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, {2: 2})) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power({2: 2}, 2)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, (2,))) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power((2,), 2)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, True)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(True, 2)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, False)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(False, 2)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, complex(2, 3))) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(complex(2, 3), 2)) # ValueError
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, float('inf'))) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(float('inf'), 2)) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, float('nan'))) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(float('nan'), 2)) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, float('-inf'))) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(float('-inf'), 2)) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(2, float('-nan'))) # False
except ValueError as e:
    print(e)

try:
    print(is_simple_power(float('-nan'), 2)) # False
except ValueError as e:
    print(e)
