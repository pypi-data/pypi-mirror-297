def add(a, b):
    """
    Adds two numbers and returns the result.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The sum of the two numbers.
    """
    return a + b

def sub(a, b):
    """
    Subtracts the second number from the first and returns the result.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The result of subtracting b from a.
    """
    return a - b

def mul(a, b):
    """
    Multiplies two numbers and returns the result.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The product of the two numbers.
    """
    return a * b

def div(a, b):
    """
    Divides the first number by the second and returns the result. 
    If division by zero is attempted, returns an error message.

    Parameters:
    a (int or float): The numerator.
    b (int or float): The denominator.

    Returns:
    float: The result of division if b is not zero.
    str: An error message if b is zero.
    """
    if b == 0:
        return "cannot divide by zero"
    return a / b

def mod(a, b):
    """
    Returns the remainder when the first number is divided by the second.

    Parameters:
    a (int or float): The numerator.
    b (int or float): The denominator.

    Returns:
    int or float: The remainder of the division.
    """
    return a % b

def pow(a, b):
    """
    Raises the first number to the power of the second and returns the result.

    Parameters:
    a (int or float): The base.
    b (int or float): The exponent.

    Returns:
    int or float: The result of a raised to the power of b.
    """
    return a ** b






def avg(*args):
    """
    Calculates the average of a variable number of numeric arguments.

    Parameters:
    *args (int or float): A variable number of numeric values.

    Returns:
    float: The average of the numbers provided.
           If no arguments are provided, returns 0.
    """
    if len(args) == 0:
        return 0
    return sum(args) / len(args)

def min(*args):
    """
    Returns the smallest value among the provided arguments.

    Parameters:
    *args (int or float): A variable number of numeric values.

    Returns:
    int or float: The smallest value in the arguments.
                  If no arguments are provided, returns None.
    """
    if len(args) == 0:
        return None
    return min(args)

def count(*args):
    """
    Counts the number of valid numeric values in the arguments.

    Parameters:
    *args: A variable number of values of any type.

    Returns:
    int: The number of arguments that are integers or floats.
    """
    return len([x for x in args if isinstance(x, (int, float))])

def sqrt(number):
    """
    Calculates the square root of a number.

    Parameters:
    number (int or float): A numeric value.

    Returns:
    float: The square root of the number if it is non-negative.
    str: An error message if the number is negative.
    """
    if number < 0:
        return "cannot calculate the sqrt because its a negative number"
    return number ** 0.5
