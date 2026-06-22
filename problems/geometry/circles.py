# =============================================================================
# problems/geometry/circles.py
# Randomised problem generator for Circles.
# =============================================================================

import random
import math

PI = 3.14


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_circumference, _type_area])
    elif difficulty == "medium":
        fn = random.choice([_type_from_diameter, _type_arc_length])
    else:
        fn = random.choice([_type_sector_area, _type_reverse])
    return fn(difficulty)


def _type_circumference(difficulty: str) -> dict:
    r   = random.randint(3, 12)
    ans = round(2 * PI * r, 2)

    question    = f"Find the circumference of a circle with radius {r} cm. Use π = 3.14."
    explanation = (
        f"C = 2πr\n"
        f"  = 2 × 3.14 × {r}\n"
        f"  = {ans} cm"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Circumference = 2πr.",
        "hint2":       f"C = 2 × 3.14 × {r}.",
        "hint3":       f"C = {ans} cm.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_area(difficulty: str) -> dict:
    r   = random.randint(3, 10)
    ans = round(PI * r * r, 2)

    question    = f"Find the area of a circle with radius {r} cm. Use π = 3.14."
    explanation = (
        f"A = πr²\n"
        f"  = 3.14 × {r}²\n"
        f"  = 3.14 × {r*r}\n"
        f"  = {ans} cm²"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Area = πr².",
        "hint2":       f"A = 3.14 × {r}² = 3.14 × {r*r}.",
        "hint3":       f"A = {ans} cm².",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_from_diameter(difficulty: str) -> dict:
    d   = random.choice([8, 10, 12, 14, 16, 20])
    r   = d // 2
    use = random.choice(["circumference", "area"])

    if use == "circumference":
        ans         = round(2 * PI * r, 2)
        formula     = f"C = 2πr = 2 × 3.14 × {r} = {ans} cm"
        question    = f"Find the circumference of a circle with diameter {d} cm. Use π = 3.14."
    else:
        ans         = round(PI * r * r, 2)
        formula     = f"A = πr² = 3.14 × {r}² = 3.14 × {r*r} = {ans} cm²"
        question    = f"Find the area of a circle with diameter {d} cm. Use π = 3.14."

    explanation = (
        f"First find the radius: r = diameter ÷ 2 = {d} ÷ 2 = {r} cm\n"
        f"Then: {formula}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        f"First find the radius: r = diameter ÷ 2 = {d} ÷ 2 = {r}.",
        "hint2":       f"Then apply the formula using r = {r}.",
        "hint3":       formula,
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_arc_length(difficulty: str) -> dict:
    r      = random.randint(4, 12)
    angles = [45, 60, 72, 90, 120, 135, 150, 180]
    theta  = random.choice(angles)
    ans    = round((theta / 360) * 2 * PI * r, 2)

    question = (
        f"Find the arc length of a sector with radius {r} cm "
        f"and angle {theta}°. Use π = 3.14."
    )
    explanation = (
        f"Arc length = (θ/360) × 2πr\n"
        f"= ({theta}/360) × 2 × 3.14 × {r}\n"
        f"= {round(theta/360, 4)} × {round(2*PI*r, 2)}\n"
        f"= {ans} cm"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Arc length = (θ/360) × 2πr.",
        "hint2":       f"({theta}/360) × 2 × 3.14 × {r}.",
        "hint3":       f"= {ans} cm.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_sector_area(difficulty: str) -> dict:
    r      = random.randint(4, 10)
    angles = [60, 90, 120, 180]
    theta  = random.choice(angles)
    ans    = round((theta / 360) * PI * r * r, 2)

    question = (
        f"Find the area of a sector with radius {r} cm "
        f"and angle {theta}°. Use π = 3.14."
    )
    explanation = (
        f"Sector area = (θ/360) × πr²\n"
        f"= ({theta}/360) × 3.14 × {r}²\n"
        f"= {round(theta/360,4)} × {round(PI*r*r,2)}\n"
        f"= {ans} cm²"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Sector area = (θ/360) × πr².",
        "hint2":       f"({theta}/360) × 3.14 × {r*r}.",
        "hint3":       f"= {ans} cm².",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_reverse(difficulty: str) -> dict:
    """Given circumference, find radius."""
    r   = random.randint(3, 12)
    c   = round(2 * PI * r, 2)
    ans = r

    question    = f"A circle has circumference {c} cm. Find its radius. Use π = 3.14."
    explanation = (
        f"C = 2πr\n"
        f"{c} = 2 × 3.14 × r\n"
        f"{c} = {2*PI}r\n"
        f"r = {c} ÷ {2*PI} = {ans} cm"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Use C = 2πr and rearrange: r = C ÷ (2π).",
        "hint2":       f"r = {c} ÷ (2 × 3.14) = {c} ÷ {2*PI}.",
        "hint3":       f"r = {ans} cm.",
        "explanation": explanation,
        "type":        "numeric",
    }