# =============================================================================
# problems/geometry/triangles.py
# Randomised problem generator for Triangles.
# =============================================================================

import random
import math

PYTHAGOREAN_TRIPLES = [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(6,8,10),(9,12,15)]


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_angle_sum, _type_area])
    elif difficulty == "medium":
        fn = random.choice([_type_isosceles, _type_pythagorean])
    else:
        fn = random.choice([_type_pythagorean_leg, _type_exterior_angle])
    return fn(difficulty)


def _type_angle_sum(difficulty: str) -> dict:
    a   = random.randint(30, 80)
    b   = random.randint(30, 80)
    while a + b >= 180:
        b = random.randint(20, 70)
    ans = 180 - a - b

    question    = f"A triangle has angles of {a}° and {b}°. Find the third angle in degrees."
    explanation = (
        f"Angles in a triangle sum to 180°:\n"
        f"{a} + {b} + x = 180\n"
        f"x = 180 - {a} - {b} = {ans}°"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "The three angles of any triangle add up to 180°.",
        "hint2":       f"{a} + {b} + x = 180.",
        "hint3":       f"x = 180 - {a} - {b} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_area(difficulty: str) -> dict:
    base   = random.randint(4, 20)
    height = random.randint(3, 15)
    ans    = (base * height) // 2
    # Ensure whole number
    if base % 2 != 0 and height % 2 != 0:
        base += 1
        ans   = (base * height) // 2

    question    = f"Find the area of a triangle with base {base} cm and height {height} cm."
    explanation = (
        f"Area = ½ × base × height\n"
        f"     = ½ × {base} × {height}\n"
        f"     = {ans} cm²"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Area of a triangle = ½ × base × height.",
        "hint2":       f"½ × {base} × {height} = ?",
        "hint3":       f"½ × {base} × {height} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_isosceles(difficulty: str) -> dict:
    apex = random.choice([20, 30, 40, 50, 60, 80, 100, 110])
    base = (180 - apex) // 2

    question    = f"An isosceles triangle has an apex angle of {apex}°. Find each base angle in degrees."
    explanation = (
        f"Angles sum to 180°. Both base angles are equal:\n"
        f"{apex} + 2 × base = 180\n"
        f"2 × base = {180 - apex}\n"
        f"base = {base}°"
    )
    return {
        "question":    question,
        "answer":      base,
        "hint":        "The two base angles of an isosceles triangle are equal.",
        "hint2":       f"apex + 2 × base = 180. So 2 × base = {180-apex}.",
        "hint3":       f"base = {180-apex} ÷ 2 = {base}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_pythagorean(difficulty: str) -> dict:
    """Find hypotenuse given two legs."""
    mult     = random.randint(1, 3)
    a, b, c  = random.choice(PYTHAGOREAN_TRIPLES)
    a, b, c  = a * mult, b * mult, c * mult

    question    = f"A right triangle has legs of {a} cm and {b} cm. Find the hypotenuse in cm."
    explanation = (
        f"Use the Pythagorean theorem: a² + b² = c²\n"
        f"{a}² + {b}² = c²\n"
        f"{a*a} + {b*b} = c²\n"
        f"{a*a + b*b} = c²\n"
        f"c = √{a*a+b*b} = {c} cm"
    )
    return {
        "question":    question,
        "answer":      c,
        "hint":        "Use the Pythagorean theorem: a² + b² = c².",
        "hint2":       f"{a}² + {b}² = {a*a} + {b*b} = {a*a+b*b}.",
        "hint3":       f"c = √{a*a+b*b} = {c}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_pythagorean_leg(difficulty: str) -> dict:
    """Find a leg given hypotenuse and other leg."""
    mult     = random.randint(1, 2)
    a, b, c  = random.choice(PYTHAGOREAN_TRIPLES)
    a, b, c  = a * mult, b * mult, c * mult

    question    = f"A right triangle has hypotenuse {c} cm and one leg {a} cm. Find the other leg in cm."
    explanation = (
        f"a² + b² = c²\n"
        f"{a}² + b² = {c}²\n"
        f"{a*a} + b² = {c*c}\n"
        f"b² = {c*c} - {a*a} = {c*c - a*a}\n"
        f"b = √{c*c-a*a} = {b} cm"
    )
    return {
        "question":    question,
        "answer":      b,
        "hint":        "Rearrange a² + b² = c² to find the missing leg: b² = c² - a².",
        "hint2":       f"b² = {c}² - {a}² = {c*c} - {a*a} = {c*c-a*a}.",
        "hint3":       f"b = √{c*c-a*a} = {b}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_exterior_angle(difficulty: str) -> dict:
    """Exterior angle = sum of two non-adjacent interior angles."""
    a   = random.randint(30, 70)
    b   = random.randint(30, 70)
    while a + b >= 180:
        b = random.randint(20, 60)
    ext = a + b

    question = (
        f"In a triangle, two interior angles are {a}° and {b}°. "
        f"Find the exterior angle adjacent to the third interior angle."
    )
    explanation = (
        f"Exterior angle = sum of the two non-adjacent interior angles\n"
        f"= {a}° + {b}° = {ext}°"
    )
    return {
        "question":    question,
        "answer":      ext,
        "hint":        "An exterior angle equals the sum of the two non-adjacent interior angles.",
        "hint2":       f"Exterior = {a} + {b}.",
        "hint3":       f"{a} + {b} = {ext}.",
        "explanation": explanation,
        "type":        "numeric",
    }