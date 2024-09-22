""" Metodo che restituisce la somma tra due operatori
"""
def add(a, b):
    return a + b

""" Metodo che restituisce la differenza tra due operatori
"""
def subtract(a, b):
    return a - b

""" Metodo che restituisce il prodotto tra due operatori
"""
def multiply(a, b):
    return a * b 

""" Metodo che restituisce la divisione tra due operatori
"""
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

