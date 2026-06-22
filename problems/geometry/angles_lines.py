# =============================================================================
# problems/geometry/angles_lines.py
# Randomised problem generator for Angles & Lines.
# =============================================================================

import random


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_complementary, _type_supplementary])
    elif difficulty == "medium":
        fn = random.choice([_type_vertically_opposite, _type_straight_line])
    else:
        fn = random.choice([_type_parallel_alternate, _type_parallel_coint])
    return fn(difficulty)


def _type_complementary(difficulty: str) -> dict:
    """Find the complement of a given angle."""
    a   = random.randint(10, 80)
    ans = 90 - a
    question    = f"Two angles are complementary. One angle is {a}°. What is the other angle in degrees?"
    explanation = f"Complementary angles add to 90°.\n90° - {a}° = {ans}°"
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Complementary angles add up to 90°.",
        "hint2":       f"90 - {a} = ?",
        "hint3":       f"90 - {a} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_supplementary(difficulty: str) -> dict:
    """Find the supplement of a given angle."""
    a   = random.randint(20, 160)
    ans = 180 - a
    question    = f"Two angles are supplementary. One angle is {a}°. What is the other angle in degrees?"
    explanation = f"Supplementary angles add to 180°.\n180° - {a}° = {ans}°"
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Supplementary angles add up to 180°.",
        "hint2":       f"180 - {a} = ?",
        "hint3":       f"180 - {a} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_vertically_opposite(difficulty: str) -> dict:
    """Solve for x using vertically opposite angles."""
    x   = random.randint(10, 40)
    m1  = random.randint(2, 5)
    b1  = random.randint(5, 20)
    b2  = m1 * x + b1 - random.randint(5, 15)
    m2  = m1 - 1 if m1 > 1 else 1
    # Ensure consistency: m1*x+b1 = m2*x+b2
    b2  = m1 * x + b1 - m2 * x

    question = (
        f"Two lines intersect. Vertically opposite angles are "
        f"({m1}x + {b1})° and ({m2}x + {b2})°. Find x."
    )
    explanation = (
        f"Vertically opposite angles are equal:\n"
        f"{m1}x + {b1} = {m2}x + {b2}\n"
        f"{m1 - m2}x = {b2 - b1}\n"
        f"x = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Vertically opposite angles are equal — set them equal to each other.",
        "hint2":       f"{m1}x + {b1} = {m2}x + {b2}. Collect x terms.",
        "hint3":       f"{m1-m2}x = {b2-b1}, so x = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_straight_line(difficulty: str) -> dict:
    """Angles on a straight line sum to 180°."""
    a1  = random.randint(20, 60)
    a2  = random.randint(20, 60)
    ans = 180 - a1 - a2

    while ans <= 0:
        a1  = random.randint(20, 50)
        a2  = random.randint(20, 50)
        ans = 180 - a1 - a2

    question = (
        f"Three angles lie on a straight line: {a1}°, x°, and {a2}°. "
        f"Find x."
    )
    explanation = (
        f"Angles on a straight line add to 180°:\n"
        f"{a1} + x + {a2} = 180\n"
        f"x = 180 - {a1} - {a2} = {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Angles on a straight line add up to 180°.",
        "hint2":       f"{a1} + x + {a2} = 180.",
        "hint3":       f"x = 180 - {a1} - {a2} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_parallel_alternate(difficulty: str) -> dict:
    """Alternate angles with parallel lines."""
    x   = random.randint(15, 50)
    m   = random.randint(2, 4)
    b   = random.randint(5, 20)
    ang = m * x + b

    question = (
        f"Two parallel lines are cut by a transversal. "
        f"One alternate angle is ({m}x + {b})° and the other is {ang}°. "
        f"Find x."
    )
    explanation = (
        f"Alternate angles are equal (Z-shape):\n"
        f"{m}x + {b} = {ang}\n"
        f"{m}x = {ang - b}\n"
        f"x = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Alternate angles between parallel lines are equal.",
        "hint2":       f"Set {m}x + {b} = {ang}.",
        "hint3":       f"{m}x = {ang-b}, so x = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_parallel_coint(difficulty: str) -> dict:
    """Co-interior angles sum to 180°."""
    x   = random.randint(10, 30)
    m1  = random.randint(2, 4)
    b1  = random.randint(10, 30)
    m2  = random.randint(1, 3)
    b2  = 180 - (m1 * x + b1) - m2 * x

    while b2 <= 0:
        x  = random.randint(10, 25)
        b2 = 180 - (m1 * x + b1) - m2 * x

    question = (
        f"Two parallel lines are cut by a transversal. "
        f"The co-interior angles are ({m1}x + {b1})° and ({m2}x + {b2})°. "
        f"Find x."
    )
    explanation = (
        f"Co-interior angles add to 180° (C-shape):\n"
        f"({m1}x + {b1}) + ({m2}x + {b2}) = 180\n"
        f"{m1+m2}x + {b1+b2} = 180\n"
        f"{m1+m2}x = {180-b1-b2}\n"
        f"x = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Co-interior angles between parallel lines add to 180°.",
        "hint2":       f"({m1}x+{b1}) + ({m2}x+{b2}) = 180.",
        "hint3":       f"{m1+m2}x + {b1+b2} = 180, so x = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }