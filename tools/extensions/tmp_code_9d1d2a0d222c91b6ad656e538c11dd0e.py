
# main.py
from calculator import add, subtract, multiply, divide
from input_validation import validate_inputs
from error_handling import handle_error

def main():
    while True:
        try:
            a = input("Enter the first number: ")
            b = input("Enter the second number: ")
            operation = input("Enter the operation (+, -, *, /): ")

            if not validate_inputs(a, b, operation):
                continue

            a, b = float(a), float(b)

            if operation == '+':
                result = add(a, b)
            elif operation == '-':
                result = subtract(a, b)
            elif operation == '*':
                result = multiply(a, b)
            elif operation == '/':
                result = divide(a, b)
            else:
                handle_error("Invalid operation.")
                continue

            display_result(result)
        except Exception as e:
            handle_error(str(e))

def display_result(result):
    print(f"The result is {result}")

if __name__ == "__main__":
    main()
