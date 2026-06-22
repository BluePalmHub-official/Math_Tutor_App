# =============================================================================
# problems/geometry/polygons.py
# Randomised problem generator for Polygons.
# =============================================================================

import random

POLYGON_NAMES = {
    3: "triangle", 4: "quadrilateral", 5: "pentagon",
    6: "hexagon", 7: "heptagon", 8: "octagon",
    9: "nonagon", 10: "decagon", 12: "dodecagon",
}


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_interior_sum, _type_rect_area])
    elif difficulty == "medium":
        fn = random.choice([_type_each_interior, _type_trapezoid_area])
    else:
        fn = random.choice([_type_find_sides, _type_missing_angle])
    return fn(difficulty)


def _type_interior_sum(difficulty: str) -> dict:
    n    = random.choice([5, 6, 7, 8, 9, 10])
    name = POLYGON_NAMES[n]
    ans  = (n - 2) * 180

    question    = f"Find the sum of interior angles of a {name} ({n} sides)."
    explanation = (
        f"Sum of interior angles = (n - 2) × 180°\n"
        f"= ({n} - 2) × 180°\n"
        f"= {n-2} × 180°\n"
        f"= {ans}°"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Sum of interior angles = (n - 2) × 180°.",
        "hint2":       f"n = {n}, so ({n} - 2) × 180 = {n-2} × 180.",
        "hint3":       f"{n-2} × 180 = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_rect_area(difficulty: str) -> dict:
    l   = random.randint(4, 20)
    w   = random.randint(3, 15)
    ans = l * w

    question    = f"Find the area of a rectangle with length {l} cm and width {w} cm."
    explanation = (
        f"Area = length × width\n"
        f"     = {l} × {w}\n"
        f"     = {ans} cm²"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Area of rectangle = length × width.",
        "hint2":       f"{l} × {w} = ?",
        "hint3":       f"{l} × {w} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_each_interior(difficulty: str) -> dict:
    n    = random.choice([5, 6, 8, 9, 10, 12])
    name = POLYGON_NAMES.get(n, f"{n}-gon")
    ans  = (n - 2) * 180 // n

    question    = f"Find each interior angle of a regular {name} ({n} sides)."
    explanation = (
        f"Each interior angle = (n - 2) × 180° ÷ n\n"
        f"= ({n} - 2) × 180° ÷ {n}\n"
        f"= {(n-2)*180} ÷ {n}\n"
        f"= {ans}°"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Each interior angle of a regular polygon = (n-2) × 180 ÷ n.",
        "hint2":       f"({n}-2) × 180 = {(n-2)*180}. Divide by {n}.",
        "hint3":       f"{(n-2)*180} ÷ {n} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_trapezoid_area(difficulty: str) -> dict:
    a   = random.randint(4, 12)
    b   = random.randint(a + 2, a + 12)
    h   = random.randint(3, 10)
    ans = ((a + b) * h) // 2
    # Ensure whole number
    while (a + b) * h % 2 != 0:
        h += 1
    ans = ((a + b) * h) // 2

    question = (
        f"Find the area of a trapezoid with parallel sides {a} cm and {b} cm "
        f"and height {h} cm."
    )
    explanation = (
        f"Area = ½ × (a + b) × h\n"
        f"     = ½ × ({a} + {b}) × {h}\n"
        f"     = ½ × {a+b} × {h}\n"
        f"     = {ans} cm²"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Area of trapezoid = ½ × (a + b) × h, where a and b are the parallel sides.",
        "hint2":       f"½ × ({a} + {b}) × {h} = ½ × {a+b} × {h}.",
        "hint3":       f"½ × {(a+b)*h} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_find_sides(difficulty: str) -> dict:
    """Find number of sides given exterior angle."""
    n    = random.choice([4, 5, 6, 8, 9, 10, 12])
    ext  = 360 // n
    name = POLYGON_NAMES.get(n, f"{n}-gon")

    question = (
        f"A regular polygon has each exterior angle equal to {ext}°. "
        f"How many sides does it have?"
    )
    explanation = (
        f"Sum of exterior angles = 360°\n"
        f"Number of sides = 360° ÷ exterior angle\n"
        f"= 360 ÷ {ext} = {n}"
    )
    return {
        "question":    question,
        "answer":      n,
        "hint":        "Sum of all exterior angles = 360°. Divide by each angle.",
        "hint2":       f"n = 360 ÷ {ext} = ?",
        "hint3":       f"360 ÷ {ext} = {n}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_missing_angle(difficulty: str) -> dict:
    """Missing angle in an irregular quadrilateral."""
    a   = random.randint(60, 110)
    b   = random.randint(60, 110)
    c   = random.randint(60, 110)
    ans = 360 - a - b - c

    while ans <= 20 or ans >= 200:
        a   = random.randint(70, 100)
        b   = random.randint(70, 100)
        c   = random.randint(70, 100)
        ans = 360 - a - b - c

    question = (
        f"A quadrilateral has three angles of {a}°, {b}°, and {c}°. "
        f"Find the fourth angle."
    )
    explanation = (
        f"Sum of interior angles of a quadrilateral = (4-2)×180 = 360°\n"
        f"{a} + {b} + {c} + x = 360\n"
        f"x = 360 - {a} - {b} - {c} = {ans}°"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Interior angles of a quadrilateral sum to 360°.",
        "hint2":       f"{a} + {b} + {c} + x = 360.",
        "hint3":       f"x = 360 - {a+b+c} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }