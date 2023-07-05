from sympy import symbols, expand

def lagrange_polynomial(x_values, y_values):
    x = symbols('x')  # define the variable
    n = len(x_values)
    L = 0  # Initialize Lagrange polynomial

    for i in range(n):
        term = 1
        for j in range(n):
            if i != j:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        print("i:", i)
        print("y_values", y_values[i])
        L +=  y_values[i] * term
    
    return expand(L)