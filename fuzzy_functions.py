# fuzzy_functions.py
import math

def fuzzy_442(x, y):
    val = (x + y) - 1
    return max(0, val)
def fuzzy_441(x, y):
    val = (x + y) - 1
    val = max(0, val)
    return math.sqrt(val)
def fuzzy_440(x, y):
    val = 2 * ((x + y) - 1)
    val = max(0, min(1, val))
    return val
def fuzzy_432(x, y):
    # Val = x * y
    Val = x * y
    return Val

def fuzzy_431(x, y):
    # Val = sqrt(x*y) - ((1-x)*(1-y))
    # Si Val < 0 alors Val = 0
    import math
    Val = math.sqrt(x * y) - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_430(x, y):
    # Sigma = (x*y) / (1 - x - y + 2*x*y) sauf si x=0 ou y=0 alors Sigma=0
    # Val = Sigma - ((1-x)*(1-y))
    # Si Val < 0 alors Val=0
    if x == 0 or y == 0:
        Sigma = 0
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_422(x, y):
    # Val = min(x, y)
    Val = x if x <= y else y
    return Val


def fuzzy_421(x, y):
    # Val = sqrt(x * y)
    Val = math.sqrt(x * y)
    return Val

def fuzzy_420(x, y):
    # Sigma = (x*y) / (1 - x - y + 2*x*y) sauf si x=0 ou y=0 alors Sigma=0
    if x == 0 or y == 0:
        Sigma = 0
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma
    return Val

def fuzzy_411(x, y):
    # Hypothèse : x et y >= 0
    sqrt_x = math.sqrt(x)
    sqrt_y = math.sqrt(y)
    return min(sqrt_x, sqrt_y)


def fuzzy_410(x, y):
    # Val = sqrt(2 * x * y)
    # Si Val > 1 alors Val = 1
    Val = math.sqrt(2 * x * y)
    if Val > 1:
        Val = 1
    return Val
def fuzzy_400(x, y):
    V = abs(x - y)
    Val = x + y - V
    if Val > 1:
        Val = 1
    return Val

def fuzzy_342(x, y):
    V = x + y - 1
    if V < 0.25:
        V = 0.25
    Val = V - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_341(x, y):
    V = x + y - 0.75
    if V > 1:
        V = 1
    Val = V - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_340(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - (2 * ((1 - x) * (1 - y)))
    if Val < 0:
        Val = 0
    return Val
def fuzzy_332(x, y):
    Val = x + y - 1
    if Val < 0.25:
        Val = 0.25
    return Val

def fuzzy_331(x, y):
    Val = x + y - 0.75
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    return Val

def fuzzy_330(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_322(x, y):
    if x >= y and x >= 0.25:
        if y >= 0.25:
            Val = y
        else:
            Val = 0.25
    else:
        if y >= x and y >= 0.25:
            if x >= 0.25:
                Val = x
            else:
                Val = 0.25
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    return Val


def fuzzy_321(x, y):
    x2 = x ** 2
    y2 = y ** 2
    if x2 >= y2 and x2 >= 0.25:
        if y2 >= 0.25:
            Val = y2
        else:
            Val = 0.25
    else:
        if y2 >= x2 and y2 >= 0.25:
            if x2 >= 0.25:
                Val = x2
            else:
                Val = 0.25
        else:
            if x2 >= y2:
                Val = x2
            else:
                Val = y2
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_320(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma
    return Val

def fuzzy_311(x, y):
    x2 = x ** 2
    y2 = y ** 2
    if x2 >= y2 and x2 >= 0.25:
        if y2 >= 0.25:
            Val = y2
        else:
            Val = 0.25
    else:
        if y2 >= x2 and y2 >= 0.25:
            if x2 >= 0.25:
                Val = x2
            else:
                Val = 0.25
        else:
            if x2 >= y2:
                Val = x2
            else:
                Val = y2
    return Val
def fuzzy_310(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma + ((1 - x) * (1 - y))
    return Val

def fuzzy_300(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma + 2 * ((1 - x) * (1 - y))
    if Val > 1:
        Val = 1
    return Val

def fuzzy_242(x, y):
    if x >= y and x >= 0.5:
        if y >= 0.5:
            Val = y
        else:
            Val = 0.5
    else:
        if y >= x and y >= 0.5:
            if x >= 0.5:
                Val = x
            else:
                Val = 0.5
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    Val = Val - 2 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_241(x, y):
    Val = (x * y) + (abs(x - y) / 2)
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val
def fuzzy_240(x, y):
    if x == 0 or y == 0:
        Sigma = 0.25
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - 2 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_232(x, y):
    if x >= y and x >= 0.5:
        if y >= 0.5:
            Val = y
        else:
            Val = 0.5
    else:
        if y >= x and y >= 0.5:
            if x >= 0.5:
                Val = x
            else:
                Val = 0.5
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_231(x, y):
    Val = (x * y) + (abs(x - y) / 2)
    return Val

def fuzzy_230(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val
def fuzzy_222(x, y):
    if x >= y and x >= 0.5:
        if y >= 0.5:
            Val = y
        else:
            Val = 0.5
    else:
        if y >= x and y >= 0.5:
            if x >= 0.5:
                Val = x
            else:
                Val = 0.5
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    # La ligne commentée en VBA est ignorée car non active
    # Val = Val - 2 * ((1 - x) * (1 - y))
    return Val

def fuzzy_221(x, y):
    Val = (x + y) / 2
    return Val

def fuzzy_220(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denominator = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denominator if denominator != 0 else 0
    Val = Sigma
    return Val

def fuzzy_211(x, y):
    x2 = x**2
    y2 = y**2
    if x2 >= y2 and x2 >= 0.5:
        if y2 >= 0.5:
            Val = y2
        else:
            Val = 0.5
    else:
        if y2 >= x2 and y2 >= 0.5:
            if x2 >= 0.5:
                Val = x2
            else:
                Val = 0.5
        else:
            if x2 >= y2:
                Val = x2
            else:
                Val = y2
    return Val
def fuzzy_210(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denom = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denom if denom != 0 else 0
    Val = Sigma + ((1 - x) * (1 - y))
    if Val > 1:
        Val = 1
    return Val

def fuzzy_200(x, y):
    if x == 0 or y == 0:
        Sigma = 0.5
    else:
        denom = 1 - x - y + 2 * x * y
        Sigma = (x * y) / denom if denom != 0 else 0
    Val = Sigma + 2 * ((1 - x) * (1 - y))
    if Val > 1:
        Val = 1
    return Val

def fuzzy_141(x, y):
    V = (x + y) / 2
    Val = V - 3 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    else:
        Val = math.sqrt(Val)
    return Val

def fuzzy_140(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) - 3 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_131(x, y):
    if x >= y and x >= 0.75:
        if y >= 0.75:
            Val = y
        else:
            Val = 0.75
    else:
        if y >= x and y >= 0.75:
            if x >= 0.75:
                Val = x
            else:
                Val = 0.75
        else:
            if x >= y:
                Val = x
            else:
                Val = y
    Val = Val - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val


def fuzzy_130(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) - 2 * ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_121(x, y):
    return sorted([x, y, 0.75])[1]


def fuzzy_120(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_111(x, y):
    Val = math.sqrt((x + y) / 2)
    return Val

def fuzzy_110(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val)
    return Val

def fuzzy_100(x, y):
    Val = x + y - 0.5
    if Val > 1:
        Val = 1
    if Val < 0:
        Val = 0
    Val = math.sqrt(Val) + ((1 - x) * (1 - y))
    return Val

def fuzzy_040(x, y):
    Val = (x * y) + abs(x - y) - ((1 - x) * (1 - y))
    if Val < 0:
        Val = 0
    return Val

def fuzzy_030(x, y):
    Val = (x * y) + abs(x - y)
    return Val

def fuzzy_020(x, y):
    if x >= y:
        Val = x
    else:
        Val = y
    return Val

def fuzzy_010(x, y):
    Val = x + y - (x * y)
    return Val

def fuzzy_000(x, y):
    Val = x + y
    if Val > 1:
        Val = 1
    return Val




agg_functions = {
        "442": fuzzy_442,
        "441": fuzzy_441,
        "440": fuzzy_440,
        "130": fuzzy_130,
        "121": fuzzy_121,
        "120": fuzzy_120,
        "111": fuzzy_111,
        "110": fuzzy_110,
        "100": fuzzy_100,
        "040": fuzzy_040,
        "030": fuzzy_030,
        "020": fuzzy_020,
        "010": fuzzy_010,
        "000": fuzzy_000,
        "131": fuzzy_131,
        "140": fuzzy_140,
        "141": fuzzy_141,
        "200": fuzzy_200,
        "210": fuzzy_210,
        "211": fuzzy_211,
        "220": fuzzy_220,
        "221": fuzzy_221,
        "222": fuzzy_222,
        "230": fuzzy_230,
        "231": fuzzy_231,
        "232": fuzzy_232,
        "240": fuzzy_240,
        "241": fuzzy_241,
        "242": fuzzy_242,
        "300": fuzzy_300,
        "310": fuzzy_310,
        "311": fuzzy_311,
        "320": fuzzy_320,
        "321": fuzzy_321,
        "322": fuzzy_322,
        "330": fuzzy_330,
        "331": fuzzy_331,
        "332": fuzzy_332,
        "340": fuzzy_340,
        "341": fuzzy_341,
        "342": fuzzy_342,
        "400": fuzzy_400,
        "410": fuzzy_410,
        "411": fuzzy_411,
        "420": fuzzy_420,
        "421": fuzzy_421,
        "422": fuzzy_422,
        "430": fuzzy_430,
        "431": fuzzy_431,
        "432": fuzzy_432
    }
def get_aggregation_function(code):
    """
    Retourne une fonction Python à partir d’un code flou (3 ou 4 chiffres).
    """
    from .fuzzy_generator import generate_fuzzy_function, generate_asymmetric_function

    code3 = code[:3]
    code4 = code

    if code4[0] == code4[-1]:  # symétrique
        if code3 in agg_functions:
            return agg_functions[code3]
        else:
            func, _ = generate_fuzzy_function(code3)
            return func
    else:  # asymétrique
        func, _ = generate_asymmetric_function(code4)
        return func


# --- Générateurs dynamiques ---
def generate_fuzzy_function(code):
    vals = {"0": 1.0, "1": 0.75, "2": 0.5, "3": 0.25, "4": 0.0}

    v1 = vals[code[0]]
    v2 = vals[code[1]]
    v3 = vals[code[2]]

    def fuzzy_func(x, y):
        if (x == 1 and y == 0) or (x == 0 and y == 1):
            return v1
        elif x == 0.5 and y == 0.5:
            return v2
        elif (x == 0.5 and y == 1) or (x == 1 and y == 0.5):
            return v3
        val = v2 * x * y + v3 * abs(x - y)
        return max(0, min(1, val))

    return fuzzy_func, {
        "type": "symétrique générée",
        "code": code,
        "points_clés": {"(1,0)/(0,1)": v1, "(0.5,0.5)": v2, "(0.5,1)/(1,0.5)": v3},
        "approximation": "v2 * x * y + v3 * |x - y|",
    }


def generate_asymmetric_function(code):
    vals = {"0": 1.0, "1": 0.75, "2": 0.5, "3": 0.25, "4": 0.0}

    vA1B0 = vals[code[0]]
    vA05B05 = vals[code[1]]
    vA05B1 = vals[code[2]]
    vA0B1 = vals[code[3]]

    def fuzzy_func(x, y):
        if x == 1 and y == 0:
            return vA1B0
        elif x == 0.5 and y == 0.5:
            return vA05B05
        elif x == 0.5 and y == 1:
            return vA05B1
        elif x == 0 and y == 1:
            return vA0B1
        val = vA05B05 * x * y + vA05B1 * x * abs(x - y) + vA0B1 * (1 - x) * y
        return max(0, min(1, val))

    return fuzzy_func, {
        "type": "asymétrique générée",
        "code": code,
        "points_clés": {"(1,0)": vA1B0, "(0.5,0.5)": vA05B05, "(0.5,1)": vA05B1, "(0,1)": vA0B1},
        "approximation": "vA05B05 * x * y + vA05B1 * x * |x - y| + vA0B1 * (1 - x) * y",
    }

# --- Sélecteur générique ---
def get_aggregation_function(code):
    code3 = code[:3]
    code4 = code

    if code4[0] == code4[-1]:  # symétrique
        if code3 in agg_functions:
            return agg_functions[code3]
        else:
            func, _ = generate_fuzzy_function(code3)
            return func
    else:  # asymétrique
        func, _ = generate_asymmetric_function(code4)
        return func

