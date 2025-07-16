import numpy as np

# Valeurs floues associées aux niveaux linguistiques
linguistic_values = {
    0: 1.0,    # complètement satisfaisant
    1: 0.75,   # satisfaisant
    2: 0.5,    # moyen
    3: 0.25,   # peu satisfaisant
    4: 0.0     # complètement insatisfaisant
}

def generate_fuzzy_function(triplet):
    """
    Génère une fonction floue à partir des valeurs souhaitées pour :
    f(1, 0), f(0.5, 0.5), f(0.5, 1)
    """
    A = np.array([
        [0,     1, 1],        # f(1, 0)
        [0.25,  0, 1],        # f(0.5, 0.5)
        [0.5,  0.5, 1]        # f(0.5, 1)
    ])
    b = np.array(triplet)

    coeffs = np.linalg.solve(A, b)
    a, b_coef, c = coeffs

    def fuzzy_func(x, y):
        val = a * x * y + b_coef * abs(x - y) + c
        return max(0, min(1, val))

    return fuzzy_func

# Génère les 125 fonctions d’agrégation possibles
agg_functions = {}

for a in range(5):
    for b in range(5):
        for c in range(5):
            code = f"{a}{b}{c}"
            triplet = (
                linguistic_values[a],  # f(1, 0)
                linguistic_values[b],  # f(0.5, 0.5)
                linguistic_values[c]   # f(0.5, 1)
            )
            agg_functions[code] = generate_fuzzy_function(triplet)
