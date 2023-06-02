from random import randint, choice
from time import sleep

def generate_arithmetic_operation():
    # Randomly choose the arithmetic operation and set the parameters
    operation, upper_limit, precision = choice((
        ("+ ", 9999999, "14"),  # Addition
        ("- ", 9999999, "14"),  # Subtraction
        ("/ ", 99999, "14.7f"),  # Division
        ("* ", 999, "14"),  # Multiplication
        ("**", 12, "14"),  # Exponentiation
        ("% ", 9999999, "14")  # Modulo
    ))
    return operation, upper_limit, precision

def perform_arithmetic_operation(operation, upper_limit):
    number1 = randint(1, upper_limit)
    number2 = randint(1, upper_limit)
    if operation == '/':
        result = round(number1 / number2, 7)  # Limit division precision
    else:
        result = eval(f"{number1} {operation} {number2}")
    return number1, operation, number2, result

def format_output(number1, operation, number2, result, precision):
    preformatted_result = "{0:>" + precision + "}"
    formatted_result = preformatted_result.format(result)
    return f" {number1:>7} {operation} {number2:<7} = {formatted_result}"

def main():
    while True:
        operation, upper_limit, precision = generate_arithmetic_operation()
        number1, operation, number2, result = perform_arithmetic_operation(operation, upper_limit)
        output = format_output(number1, operation, number2, result, precision)
        print(output)
        sleep(0.125)

if __name__ == "__main__":
    main()
