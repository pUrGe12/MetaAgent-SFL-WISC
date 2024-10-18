
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_inputs(a, b, operation):
    if not is_numeric(a) or not is_numeric(b):
        handle_error("Invalid input. Please enter numeric values.")
        return False
    if operation not in ['+', '-', '*', '/']:
        handle_error("Invalid operation. Please enter one of +, -, *, /.")
        return False
    return True
    