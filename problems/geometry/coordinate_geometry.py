# =============================================================================
# problems/geometry/coordinate_geometry.py
# Randomised problem generator for Coordinate Geometry.
# =============================================================================

import random
import math


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_midpoint, _type_gradient])
    elif difficulty == "medium":
        fn = random.choice([_type_distance, _type_line_equation])
    else:
        fn = random.choice([_type_line_from_points, _type_missing_endpoint])
    return fn(difficulty)


def _type_midpoint(difficulty: str) -> dict:
    x1, y1 = random.randint(-6, 6), random.randint(-6, 6)
    x2, y2 = random.randint(-6, 6), random.randint(-6, 6)
    # Ensure whole-number midpoint
    while (x1 + x2) % 2 != 0 or (y1 + y2) % 2 != 0:
        x2, y2 = random.randint(-6, 6), random.randint(-6, 6)

    mx  = (x1 + x2) // 2
    my  = (y1 + y2) // 2
    ans = mx  # We ask for x-coordinate of midpoint

    question = (
        f"Find the x-coordinate of the midpoint of the segment "
        f"from A({x1}, {y1}) to B({x2}, {y2})."
    )
    explanation = (
        f"Midpoint x = (x₁ + x₂) / 2\n"
        f"= ({x1} + {x2}) / 2\n"
        f"= {x1+x2} / 2\n"
        f"= {mx}\n"
        f"Full midpoint: ({mx}, {my})"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Midpoint x = (x₁ + x₂) / 2.",
        "hint2":       f"({x1} + {x2}) / 2 = {x1+x2} / 2.",
        "hint3":       f"= {mx}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_gradient(difficulty: str) -> dict:
    x1, y1 = random.randint(-4, 4), random.randint(-4, 4)
    run     = random.choice([-4, -3, -2, 2, 3, 4])
    m       = random.choice([-3, -2, -1, 1, 2, 3])
    x2      = x1 + run
    y2      = y1 + m * run

    question = (
        f"Find the gradient of the line through "
        f"A({x1}, {y1}) and B({x2}, {y2})."
    )
    explanation = (
        f"m = (y₂ - y₁) / (x₂ - x₁)\n"
        f"= ({y2} - {y1}) / ({x2} - {x1})\n"
        f"= {y2-y1} / {x2-x1}\n"
        f"= {m}"
    )
    return {
        "question":    question,
        "answer":      m,
        "hint":        "Gradient m = (y₂ - y₁) / (x₂ - x₁).",
        "hint2":       f"({y2} - {y1}) / ({x2} - {x1}) = {y2-y1} / {x2-x1}.",
        "hint3":       f"= {m}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_distance(difficulty: str) -> dict:
    """Distance using Pythagorean triples for clean answers."""
    triples = [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15)]
    a, b, c = random.choice(triples)
    # Random signs for direction
    sx, sy = random.choice([1,-1]), random.choice([1,-1])
    x1, y1 = random.randint(-3,3), random.randint(-3,3)
    x2, y2 = x1 + sx*a, y1 + sy*b

    question = (
        f"Find the distance between A({x1}, {y1}) and B({x2}, {y2})."
    )
    explanation = (
        f"d = √[(x₂-x₁)² + (y₂-y₁)²]\n"
        f"= √[({x2}-{x1})² + ({y2}-{y1})²]\n"
        f"= √[{a}² + {b}²]\n"
        f"= √[{a*a} + {b*b}]\n"
        f"= √{a*a+b*b} = {c}"
    )
    return {
        "question":    question,
        "answer":      c,
        "hint":        "Distance = √[(x₂-x₁)² + (y₂-y₁)²].",
        "hint2":       f"√[{a}² + {b}²] = √[{a*a} + {b*b}] = √{a*a+b*b}.",
        "hint3":       f"= {c}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_line_equation(difficulty: str) -> dict:
    """Find y-intercept given gradient and a point."""
    m  = random.choice([-3,-2,-1,1,2,3])
    x0 = random.randint(-4, 4)
    y0 = random.randint(-6, 6)
    c  = y0 - m * x0

    question = (
        f"A line has gradient {m} and passes through ({x0}, {y0}). "
        f"Find the y-intercept (c in y = mx + c)."
    )
    explanation = (
        f"Use y = mx + c with the known point:\n"
        f"{y0} = {m} × {x0} + c\n"
        f"{y0} = {m*x0} + c\n"
        f"c = {y0} - {m*x0} = {c}"
    )
    return {
        "question":    question,
        "answer":      c,
        "hint":        "Substitute the point into y = mx + c and solve for c.",
        "hint2":       f"{y0} = {m} × {x0} + c → {y0} = {m*x0} + c.",
        "hint3":       f"c = {y0} - {m*x0} = {c}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_line_from_points(difficulty: str) -> dict:
    """Find gradient and y-intercept from two points."""
    x1, y1 = random.randint(-3, 3), random.randint(-4, 4)
    run     = random.choice([-3,-2,2,3])
    m       = random.choice([-2,-1,1,2])
    x2      = x1 + run
    y2      = y1 + m * run
    c       = y1 - m * x1

    question = (
        f"Find the gradient of the line through A({x1}, {y1}) and B({x2}, {y2}), "
        f"then find its y-intercept. Enter the gradient."
    )
    explanation = (
        f"Gradient: m = ({y2}-{y1}) / ({x2}-{x1}) = {y2-y1}/{x2-x1} = {m}\n"
        f"y-intercept: use point ({x1},{y1}):\n"
        f"{y1} = {m}({x1}) + c → c = {y1} - {m*x1} = {c}\n"
        f"Equation: y = {m}x + {c if c != 0 else ''}"
    )
    return {
        "question":    question,
        "answer":      m,
        "hint":        "Find gradient first: m = (y₂-y₁)/(x₂-x₁).",
        "hint2":       f"m = ({y2}-{y1}) / ({x2}-{x1}) = {y2-y1}/{x2-x1}.",
        "hint3":       f"m = {m}. Then y-intercept: c = {c}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_missing_endpoint(difficulty: str) -> dict:
    """Given midpoint and one endpoint, find the other."""
    # Midpoint M, endpoint A, find B
    mx = random.randint(-3, 3)
    my = random.randint(-3, 3)
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = 2 * mx - x1
    y2 = 2 * my - y1

    question = (
        f"The midpoint of segment AB is M({mx}, {my}). "
        f"If A is ({x1}, {y1}), find the x-coordinate of B."
    )
    explanation = (
        f"Midpoint formula: mx = (x₁ + x₂) / 2\n"
        f"{mx} = ({x1} + x₂) / 2\n"
        f"2 × {mx} = {x1} + x₂\n"
        f"{2*mx} = {x1} + x₂\n"
        f"x₂ = {2*mx} - {x1} = {x2}\n"
        f"Full point B: ({x2}, {y2})"
    )
    return {
        "question":    question,
        "answer":      x2,
        "hint":        "Use midpoint formula: mx = (x₁+x₂)/2. Rearrange for x₂.",
        "hint2":       f"2×{mx} = {x1} + x₂. So x₂ = {2*mx} - {x1}.",
        "hint3":       f"x₂ = {x2}.",
        "explanation": explanation,
        "type":        "numeric",
    }