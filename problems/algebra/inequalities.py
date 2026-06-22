# =============================================================================
# problems/algebra/inequalities.py
# Randomised problem generator for Inequalities.
# =============================================================================

import random

SYMBOLS     = [">", "<", ">=", "<="]
SYMBOL_DISP = {">": ">", "<": "<", ">=": "≥", "<=": "≤"}
FLIP        = {">": "<", "<": ">", ">=": "<=", "<=": ">="}


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_simple_add, _type_simple_sub])
    elif difficulty == "medium":
        fn = random.choice([_type_ax_plus_b, _type_negative_coeff])
    else:
        fn = random.choice([_type_negative_coeff, _type_compound])
    return fn(difficulty)


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def _type_simple_add(difficulty: str) -> dict:
    """x + b > c"""
    sym = random.choice(SYMBOLS)
    b   = random.randint(1, 10)
    ans = random.randint(1, 10)
    c   = ans + b if sym in (">", ">=") else ans + b - 1

    disp = SYMBOL_DISP[sym]
    question    = f"Solve:   x + {b} {disp} {c}"
    boundary    = c - b
    explanation = (
        f"Subtract {b} from both sides:\n"
        f"x {disp} {boundary}"
    )
    return {
        "question":    question,
        "answer":      str(boundary),
        "hint":        f"Subtract {b} from both sides.",
        "hint2":       f"After subtracting: x {disp} {boundary}.",
        "hint3":       f"The answer is just the boundary value: {boundary}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_simple_sub(difficulty: str) -> dict:
    """x - b < c"""
    sym = random.choice(SYMBOLS)
    b   = random.randint(1, 10)
    ans = random.randint(2, 12)
    c   = ans - b

    disp        = SYMBOL_DISP[sym]
    boundary    = c + b
    question    = f"Solve:   x \u2212 {b} {disp} {c}"
    explanation = (
        f"Add {b} to both sides:\n"
        f"x {disp} {boundary}"
    )
    return {
        "question":    question,
        "answer":      str(boundary),
        "hint":        f"Add {b} to both sides.",
        "hint2":       f"After adding: x {disp} {boundary}.",
        "hint3":       f"Boundary value is {boundary}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_ax_plus_b(difficulty: str) -> dict:
    """ax + b > c  (positive coefficient)"""
    sym = random.choice(SYMBOLS)
    a   = random.randint(2, 6)
    ans = random.randint(1, 10)
    b   = random.randint(1, 10)
    c   = a * ans + b

    disp        = SYMBOL_DISP[sym]
    boundary    = ans
    question    = f"Solve:   {a}x + {b} {disp} {c}"
    explanation = (
        f"Step 1 — Subtract {b} from both sides:\n"
        f"         {a}x {disp} {c - b}\n"
        f"Step 2 — Divide both sides by {a} (positive, sign stays):\n"
        f"         x {disp} {boundary}"
    )
    return {
        "question":    question,
        "answer":      str(boundary),
        "hint":        f"Subtract {b} from both sides first.",
        "hint2":       f"After subtracting: {a}x {disp} {c - b}. Divide by {a}.",
        "hint3":       f"Dividing by {a} (positive) keeps the sign. Answer: x {disp} {boundary}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_negative_coeff(difficulty: str) -> dict:
    """−ax + b > c  (negative coefficient — must flip)"""
    sym = random.choice(SYMBOLS)
    a   = random.randint(2, 5)
    ans = random.randint(-5, 5)
    b   = random.randint(1, 10)
    c   = -a * ans + b + (1 if sym in (">", ">=") else -1)

    disp         = SYMBOL_DISP[sym]
    flipped_sym  = SYMBOL_DISP[FLIP[sym]]
    boundary     = ans

    question    = f"Solve:   \u2212{a}x + {b} {disp} {c}"
    explanation = (
        f"Step 1 — Subtract {b} from both sides:\n"
        f"         \u2212{a}x {disp} {c - b}\n"
        f"Step 2 — Divide by \u2212{a}  (NEGATIVE — flip the sign!):\n"
        f"         x {flipped_sym} {boundary}"
    )
    return {
        "question":    question,
        "answer":      str(boundary),
        "hint":        f"Subtract {b} from both sides first.",
        "hint2":       f"You will need to divide by a negative number — remember to flip the sign!",
        "hint3":       f"After dividing by -{a}: x {flipped_sym} {boundary}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_compound(difficulty: str) -> dict:
    """a < x + b < c"""
    b     = random.randint(1, 8)
    lower = random.randint(-3, 5)
    upper = lower + random.randint(3, 10)
    a     = lower + b
    c     = upper + b

    question    = f"Solve:   {a} < x + {b} < {c}"
    explanation = (
        f"Subtract {b} from all three parts:\n"
        f"{a} \u2212 {b}  <  x  <  {c} \u2212 {b}\n"
        f"{lower}  <  x  <  {upper}"
    )
    return {
        "question":    question,
        "answer":      str(lower),
        "hint":        f"Subtract {b} from all three parts simultaneously.",
        "hint2":       f"After subtracting {b}: {lower} < x < {upper}. The lower bound is {lower}.",
        "hint3":       f"Enter the lower boundary value: {lower}.",
        "explanation": explanation,
        "type":        "numeric",
    }