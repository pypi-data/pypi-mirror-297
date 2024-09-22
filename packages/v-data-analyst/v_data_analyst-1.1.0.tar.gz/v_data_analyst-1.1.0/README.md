this is the package created and developed by author: Vishwa

def div(a, b):
    """
    Divide two numbers.

    This function takes two numerical inputs, `a` and `b`, and returns the result of dividing `a` by `b`.

    Parameters:
    a (int or float): The numerator.
    b (int or float): The denominator. Must not be zero.

    Returns:
    float: The result of dividing `a` by `b`.

    Raises:
    ZeroDivisionError: If `b` is zero.

    Example:
    >>> div(10, 2)
    5.0
    """
    return a / b

def mod(a, b):
    """
    Calculate the remainder of division (modulus) of two numbers.

    This function takes two numerical inputs, `a` and `b`, and returns the remainder when `a` is divided by `b`.

    Parameters:
    a (int or float): The dividend.
    b (int or float): The divisor. Must not be zero.

    Returns:
    int or float: The remainder of the division of `a` by `b`.

    Raises:
    ZeroDivisionError: If `b` is zero.

    Example:
    >>> mod(10, 3)
    1
    """
    return a % b
