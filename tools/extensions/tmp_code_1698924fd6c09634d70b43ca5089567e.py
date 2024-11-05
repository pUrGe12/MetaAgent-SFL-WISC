
# Given information
x_min = 0
x_max = 1
N = 1  # Initial guess for N

# Function to calculate the integral of the square of the wave function
def integral(N):
    return N**2 * (2 - 2 * (1 + x_max)**0.5 + 2 * (1 + x_min)**0.5)

# Check if the integral equals 1 (Normalization condition)
tolerance = 1e-6
integral_value = integral(N)
while abs(integral_value - 1) > tolerance:
    N += 0.001
    integral_value = integral(N)

N
