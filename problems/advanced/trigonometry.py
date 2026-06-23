# =============================================================================
# problems/advanced/trigonometry.py
# Randomised problem generator for Trigonometry (SAT Advanced).
# =============================================================================

import random
import math


# Common angle trig values (degrees → value)
_SIN = {30: 0.5, 45: round(math.sqrt(2)/2, 4), 60: round(math.sqrt(3)/2, 4)}
_COS = {30: round(math.sqrt(3)/2, 4), 45: round(math.sqrt(2)/2, 4), 60: 0.5}
_TAN = {30: round(1/math.sqrt(3), 4), 45: 1.0, 60: round(math.sqrt(3), 4)}


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_common_angle_sin, _type_common_angle_cos])
    elif difficulty == "medium":
        fn = random.choice([_type_find_opp_side, _type_find_adj_side])
    else:
        fn = random.choice([_type_find_hyp, _type_find_angle])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_common_angle_sin(difficulty: str) -> dict:
    angle = random.choice([30, 45, 60])
    val   = _SIN[angle]

    question = f"What is the value of sin({angle}°)? Give your answer as a decimal rounded to 4 decimal places."
    explanation = (
        f"sin(30°) = 0.5000\n"
        f"sin(45°) = √2/2 ≈ 0.7071\n"
        f"sin(60°) = √3/2 ≈ 0.8660\n\n"
        f"sin({angle}°) = {val}"
    )
    return {
        "question":    question,
        "answer":      val,
        "hint":        "sin 30° = 0.5,  sin 45° ≈ 0.7071,  sin 60° ≈ 0.8660.",
        "hint2":       f"Look up or recall sin({angle}°).",
        "hint3":       f"sin({angle}°) = {val}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_common_angle_cos(difficulty: str) -> dict:
    angle = random.choice([30, 45, 60])
    val   = _COS[angle]

    question = f"What is the value of cos({angle}°)? Give your answer as a decimal rounded to 4 decimal places."
    explanation = (
        f"cos(30°) = √3/2 ≈ 0.8660\n"
        f"cos(45°) = √2/2 ≈ 0.7071\n"
        f"cos(60°) = 0.5000\n\n"
        f"cos({angle}°) = {val}"
    )
    return {
        "question":    question,
        "answer":      val,
        "hint":        "cos 30° ≈ 0.8660,  cos 45° ≈ 0.7071,  cos 60° = 0.5.",
        "hint2":       f"Look up or recall cos({angle}°).",
        "hint3":       f"cos({angle}°) = {val}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_find_opp_side(difficulty: str) -> dict:
    """Given hypotenuse and angle, find opposite side using sine."""
    angle = random.choice([30, 45, 60])
    hyp   = random.choice([10, 12, 14, 16, 20])
    opp   = round(hyp * _SIN[angle], 2)

    question = (
        f"In a right triangle, the angle is {angle}° and the hypotenuse is {hyp}. "
        f"Find the side opposite the {angle}° angle. Round to 2 decimal places."
    )
    explanation = (
        f"sin θ = opposite / hypotenuse\n"
        f"sin({angle}°) = opp / {hyp}\n"
        f"opp = {hyp} × sin({angle}°)\n"
        f"opp = {hyp} × {_SIN[angle]}\n"
        f"opp = {opp}"
    )
    return {
        "question":    question,
        "answer":      opp,
        "hint":        "Use SOH: sin θ = opposite / hypotenuse.",
        "hint2":       f"opp = hyp × sin({angle}°) = {hyp} × {_SIN[angle]}.",
        "hint3":       f"opp = {opp}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_find_adj_side(difficulty: str) -> dict:
    """Given hypotenuse and angle, find adjacent side using cosine."""
    angle = random.choice([30, 45, 60])
    hyp   = random.choice([10, 12, 14, 16, 20])
    adj   = round(hyp * _COS[angle], 2)

    question = (
        f"In a right triangle, the angle is {angle}° and the hypotenuse is {hyp}. "
        f"Find the side adjacent to the {angle}° angle. Round to 2 decimal places."
    )
    explanation = (
        f"cos θ = adjacent / hypotenuse\n"
        f"cos({angle}°) = adj / {hyp}\n"
        f"adj = {hyp} × cos({angle}°)\n"
        f"adj = {hyp} × {_COS[angle]}\n"
        f"adj = {adj}"
    )
    return {
        "question":    question,
        "answer":      adj,
        "hint":        "Use CAH: cos θ = adjacent / hypotenuse.",
        "hint2":       f"adj = hyp × cos({angle}°) = {hyp} × {_COS[angle]}.",
        "hint3":       f"adj = {adj}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_find_hyp(difficulty: str) -> dict:
    """Given opposite and angle, find hypotenuse using sine."""
    angle = random.choice([30, 45, 60])
    hyp   = random.choice([10, 12, 14, 16, 20])
    opp   = round(hyp * _SIN[angle], 2)

    question = (
        f"In a right triangle, the angle is {angle}° and the opposite side is {opp}. "
        f"Find the hypotenuse. Round to 2 decimal places."
    )
    explanation = (
        f"sin θ = opposite / hypotenuse\n"
        f"sin({angle}°) = {opp} / hyp\n"
        f"hyp = {opp} / sin({angle}°)\n"
        f"hyp = {opp} / {_SIN[angle]}\n"
        f"hyp = {hyp}"
    )
    return {
        "question":    question,
        "answer":      round(hyp, 2),
        "hint":        "sin θ = opp / hyp  →  hyp = opp / sin θ.",
        "hint2":       f"hyp = {opp} / sin({angle}°) = {opp} / {_SIN[angle]}.",
        "hint3":       f"hyp = {hyp}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_find_angle(difficulty: str) -> dict:
    """Given opposite and hypotenuse, find angle using arcsin. Answer in degrees."""
    angle  = random.choice([30, 45, 60])
    hyp    = random.choice([10, 12, 14, 20])
    opp    = round(hyp * _SIN[angle], 2)
    ratio  = round(opp / hyp, 4)

    question = (
        f"In a right triangle, the opposite side is {opp} and the hypotenuse is {hyp}. "
        f"Find the angle θ in degrees. Round to the nearest whole number."
    )
    explanation = (
        f"sin θ = opposite / hypotenuse = {opp} / {hyp} = {ratio}\n"
        f"θ = sin⁻¹({ratio})\n"
        f"θ = {angle}°"
    )
    return {
        "question":    question,
        "answer":      angle,
        "hint":        "Use inverse sine: θ = sin⁻¹(opposite / hypotenuse).",
        "hint2":       f"sin θ = {opp} / {hyp} = {ratio}.  Apply sin⁻¹.",
        "hint3":       f"θ = sin⁻¹({ratio}) = {angle}°.",
        "explanation": explanation,
        "type":        "numeric",
    }
