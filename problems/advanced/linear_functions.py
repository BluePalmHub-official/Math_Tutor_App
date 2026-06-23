# =============================================================================
# problems/advanced/linear_functions.py
# Randomised problem generator for Linear Functions (SAT Advanced).
# =============================================================================

import random
from fractions import Fraction


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_slope_two_points, _type_y_value])
    elif difficulty == "medium":
        fn = random.choice([_type_y_intercept, _type_x_intercept])
    else:
        fn = random.choice([_type_perpendicular_slope, _type_slope_from_standard])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_slope_two_points(difficulty: str) -> dict:
    """Find slope given two points with integer slope."""
    x1 = random.randint(-4, 4)
    x2 = x1 + random.randint(1, 5)
    m  = random.randint(-4, 4)
    while m == 0:
        m = random.randint(-4, 4)
    y1 = random.randint(-6, 6)
    y2 = y1 + m * (x2 - x1)

    question = (
        f"Find the slope of the line passing through "
        f"({x1}, {y1}) and ({x2}, {y2})."
    )
    explanation = (
        f"Slope formula:  m = (y₂ − y₁) / (x₂ − x₁)\n"
        f"m = ({y2} − {y1}) / ({x2} − {x1})\n"
        f"m = {y2 - y1} / {x2 - x1}\n"
        f"m = {m}"
    )
    return {
        "question":    question,
        "answer":      m,
        "hint":        "Slope = (y₂ − y₁) / (x₂ − x₁). Put y-values on top.",
        "hint2":       f"Rise = {y2} − {y1} = {y2 - y1}.  Run = {x2} − {x1} = {x2 - x1}.",
        "hint3":       f"m = {y2 - y1} / {x2 - x1} = {m}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_y_value(difficulty: str) -> dict:
    """Given y = mx + b, find y when x = given value."""
    m = random.randint(-4, 4)
    while m == 0:
        m = random.randint(-4, 4)
    b  = random.randint(-8, 8)
    xv = random.randint(-5, 5)
    ans = m * xv + b

    question = (
        f"Find the value of y when x = {xv} for the equation  y = {m}x + {b}."
    )
    explanation = (
        f"Substitute x = {xv} into y = {m}x + {b}:\n"
        f"y = {m}({xv}) + {b}\n"
        f"y = {m * xv} + {b}\n"
        f"y = {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        f"Replace x with {xv} in the equation.",
        "hint2":       f"y = {m} × {xv} + {b} = {m*xv} + {b}.",
        "hint3":       f"y = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_y_intercept(difficulty: str) -> dict:
    """Given slope and a point, find the y-intercept b."""
    m  = random.randint(-4, 4)
    while m == 0:
        m = random.randint(-4, 4)
    x1 = random.randint(-5, 5)
    b  = random.randint(-10, 10)
    y1 = m * x1 + b

    question = (
        f"A line has slope {m} and passes through ({x1}, {y1}). "
        f"Find the y-intercept."
    )
    explanation = (
        f"Use y = mx + b with m = {m} and point ({x1}, {y1}):\n"
        f"{y1} = {m}({x1}) + b\n"
        f"{y1} = {m * x1} + b\n"
        f"b = {y1} − {m * x1} = {b}"
    )
    return {
        "question":    question,
        "answer":      b,
        "hint":        "Substitute m and the point into y = mx + b, then solve for b.",
        "hint2":       f"{y1} = {m}({x1}) + b  →  {y1} = {m*x1} + b.",
        "hint3":       f"b = {y1} − {m*x1} = {b}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_x_intercept(difficulty: str) -> dict:
    """Find the x-intercept of y = mx + b."""
    m = random.randint(-5, 5)
    while m == 0:
        m = random.randint(-5, 5)
    xi = random.randint(-6, 6)
    b  = -m * xi  # ensures x-intercept is xi

    question = f"Find the x-intercept of the line  y = {m}x + {b}."
    explanation = (
        f"The x-intercept is where y = 0.\n"
        f"Set y = 0:   0 = {m}x + {b}\n"
        f"Subtract {b}:  {-b} = {m}x\n"
        f"Divide by {m}:  x = {-b} / {m} = {xi}"
    )
    return {
        "question":    question,
        "answer":      xi,
        "hint":        "Set y = 0 and solve for x.",
        "hint2":       f"0 = {m}x + {b}  →  {m}x = {-b}.",
        "hint3":       f"x = {-b} / {m} = {xi}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_perpendicular_slope(difficulty: str) -> dict:
    """Find slope of perpendicular line. Uses clean fractions: 1/2, 2/3, etc."""
    pairs = [(2, -1, 2), (3, -1, 3), (4, -1, 4), (-2, 1, 2),
             (1, -2, 1), (1, -3, 1), (-1, 2, 1), (-3, 1, 3)]
    m_num, perp_num, perp_den = random.choice(pairs)
    perp = Fraction(perp_num, perp_den)

    question = (
        f"A line has slope {m_num}. "
        f"What is the slope of a line perpendicular to it?"
    )
    perp_display = str(perp) if perp.denominator > 1 else str(int(perp))
    explanation = (
        f"Perpendicular slope = −1 / m = −1 / {m_num}\n"
        f"= {perp_display}"
    )
    ans = float(perp)
    return {
        "question":    question,
        "answer":      round(ans, 4),
        "hint":        "Perpendicular slope = negative reciprocal of given slope.",
        "hint2":       f"Flip {m_num} to get 1/{m_num}, then change the sign.",
        "hint3":       f"Perpendicular slope = {perp_display}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_slope_from_standard(difficulty: str) -> dict:
    """Find slope after rearranging ax + by = c."""
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    c = random.randint(2, 20)
    # slope = -a/b
    slope_f = Fraction(-a, b)
    slope_val = round(float(slope_f), 4)

    question = (
        f"Find the slope of the line  {a}x + {b}y = {c}."
    )
    y_int = Fraction(c, b)
    explanation = (
        f"Rearrange to y = mx + b form:\n"
        f"{b}y = −{a}x + {c}\n"
        f"y = (−{a}/{b})x + {c}/{b}\n"
        f"Slope = −{a}/{b} = {slope_f}"
    )
    return {
        "question":    question,
        "answer":      slope_val,
        "hint":        "Rearrange to y = mx + b by solving for y.",
        "hint2":       f"Subtract {a}x: {b}y = −{a}x + {c}, then divide by {b}.",
        "hint3":       f"Slope = −{a}/{b} = {slope_f}.",
        "explanation": explanation,
        "type":        "numeric",
    }
