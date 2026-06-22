# =============================================================================
# problems/algebra/quadratics.py
# Randomised problem generator for Quadratics.
# =============================================================================

import random
import math


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        return _type_factorable(difficulty)
    elif difficulty == "medium":
        return random.choice([_type_factorable, _type_quadratic_formula])(difficulty)
    else:
        return random.choice([_type_quadratic_formula, _type_complete_square])(difficulty)


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def _type_factorable(difficulty: str) -> dict:
    """x² + bx + c = 0 where roots are integers."""
    if difficulty == "easy":
        r1 = random.randint(1, 6)
        r2 = random.randint(1, 6)
    else:
        r1 = random.randint(-8, 8)
        r2 = random.randint(-8, 8)
        while r1 == 0 or r2 == 0:
            r1 = random.randint(-8, 8)
            r2 = random.randint(-8, 8)

    b = -(r1 + r2)
    c = r1 * r2

    # Format equation nicely
    b_str = f"+ {b}x" if b > 0 else (f"\u2212 {abs(b)}x" if b < 0 else "")
    c_str = f"+ {c}"  if c > 0 else (f"\u2212 {abs(c)}"  if c < 0 else "")
    question = f"Solve by factoring:   x\u00b2 {b_str} {c_str} = 0"

    # Sort roots so smaller is the expected answer
    ans1, ans2 = sorted([r1, r2])

    explanation = (
        f"Find two numbers that multiply to {c} and add to {b}:\n"
        f"Answer: {-r1} and {-r2}\n"
        f"Factored form: (x \u2212 {r1})(x \u2212 {r2}) = 0\n"
        f"Zero Product Rule:\n"
        f"  x \u2212 {r1} = 0  \u2192  x = {r1}\n"
        f"  x \u2212 {r2} = 0  \u2192  x = {r2}\n"
        f"Solutions: x = {ans1}  or  x = {ans2}"
    )

    return {
        "question":    question,
        "answer":      ans1,
        "hint":        f"Find two numbers that multiply to {c} and add to {b}.",
        "hint2":       f"The two numbers are {-r1} and {-r2}. Write as (x...)(x...) = 0.",
        "hint3":       f"(x \u2212 {r1})(x \u2212 {r2}) = 0. Enter the smaller root.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_quadratic_formula(difficulty: str) -> dict:
    """ax² + bx + c = 0 solved with the quadratic formula."""
    # Generate with known integer roots for clean answers
    if difficulty == "medium":
        a  = random.randint(1, 3)
        r1 = random.randint(-5, 5)
        r2 = random.randint(-5, 5)
        while r1 == r2 or r1 == 0 or r2 == 0:
            r2 = random.randint(-5, 5)
    else:
        a  = random.randint(1, 4)
        r1 = random.randint(-8, 8)
        r2 = random.randint(-8, 8)
        while r1 == r2 or r1 == 0 or r2 == 0:
            r2 = random.randint(-8, 8)

    b = -a * (r1 + r2)
    c = a * r1 * r2
    D = b * b - 4 * a * c

    b_str = f"+ {b}x" if b > 0 else f"\u2212 {abs(b)}x"
    c_str = f"+ {c}"  if c > 0 else f"\u2212 {abs(c)}"
    a_str = "" if a == 1 else str(a)

    question    = f"Use the quadratic formula:   {a_str}x\u00b2 {b_str} {c_str} = 0"
    ans1, ans2  = sorted([r1, r2])

    explanation = (
        f"a = {a},  b = {b},  c = {c}\n"
        f"Discriminant D = {b}\u00b2 \u2212 4({a})({c}) = {b*b} \u2212 {4*a*c} = {D}\n"
        f"x = (\u2212{b} \u00b1 \u221a{D}) / (2 \u00d7 {a})\n"
        f"x = ({-b} \u00b1 {int(math.sqrt(D))}) / {2*a}\n"
        f"x = {ans1}  or  x = {ans2}"
    )

    return {
        "question":    question,
        "answer":      ans1,
        "hint":        f"Identify a={a}, b={b}, c={c}. Calculate D = b\u00b2 - 4ac first.",
        "hint2":       f"D = {D}. Apply formula: x = (-{b} \u00b1 \u221a{D}) / {2*a}.",
        "hint3":       f"Two solutions: {ans1} and {ans2}. Enter the smaller one.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_complete_square(difficulty: str) -> dict:
    """x² + bx + c = 0 solved by completing the square (even b for clean steps)."""
    r1 = random.randint(-6, 6)
    r2 = random.randint(-6, 6)
    while r1 == r2 or r1 == 0 or r2 == 0:
        r2 = random.randint(-6, 6)

    b = -(r1 + r2)
    c = r1 * r2

    # Make b even for clean completing the square
    if b % 2 != 0:
        r2 += 1
        b = -(r1 + r2)
        c = r1 * r2

    half_b  = b // 2
    k       = half_b ** 2 - c
    ans1, ans2 = sorted([r1, r2])

    b_str = f"+ {b}x" if b > 0 else f"\u2212 {abs(b)}x"
    c_str = f"+ {c}"  if c > 0 else f"\u2212 {abs(c)}"

    question    = f"Solve by completing the square:   x\u00b2 {b_str} {c_str} = 0"
    explanation = (
        f"Step 1 — Move constant: x\u00b2 {b_str} = {-c}\n"
        f"Step 2 — Add ({b}/{2})\u00b2 = {half_b**2} to both sides:\n"
        f"         x\u00b2 {b_str} + {half_b**2} = {-c} + {half_b**2} = {k}\n"
        f"Step 3 — Factor: (x + {half_b})\u00b2 = {k}\n"
        f"Step 4 — Square root: x + {half_b} = \u00b1{int(math.sqrt(k))}\n"
        f"Step 5 — Solve: x = {ans1}  or  x = {ans2}"
    )

    return {
        "question":    question,
        "answer":      ans1,
        "hint":        f"Move {c} to the right, then add ({b}/2)² = {half_b**2} to both sides.",
        "hint2":       f"After completing: (x + {half_b})² = {k}. Take the square root.",
        "hint3":       f"x + {half_b} = ±{int(math.sqrt(k))}. Two solutions: {ans1} and {ans2}.",
        "explanation": explanation,
        "type":        "numeric",
    }