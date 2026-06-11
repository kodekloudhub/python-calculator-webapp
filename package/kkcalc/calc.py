"""KodeKloud sample calculator library — published to Azure Artifacts."""


def safe_divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b
