async def async_calculate(x, y, operator):
    if operator == '+':
        return x + y
    elif operator == '-':
        return x - y
    elif operator == '*':
        return x * y
    elif operator == '/':
        if y == 0:
            raise ValueError("Division by zero")
        return x / y
    else:
        raise ValueError("Invalid operator")