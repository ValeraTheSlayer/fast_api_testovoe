import logging

logger = logging.getLogger(__name__)

async def async_calculate(x, y, operator):
    logger.info(f"Рассчитываю: {x} {operator} {y}")
    if operator == '+':
        return x + y
    elif operator == '-':
        return x - y
    elif operator == '*':
        return x * y
    elif operator == '/':
        if y == 0:
            logger.error("Попытка деления на 0")
            raise ValueError("Division by zero")
        return x / y
    else:
        logger.error(f"Невалидный оператор: {operator}")
        raise ValueError("Invalid operator")