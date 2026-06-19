# =============================================================================
# problems/algebra/linear_equations.py
# Randomised problem generator for Linear Equations.
#
# Public API — one function only:
#   generate(difficulty="easy") -> dict
#
# Difficulty levels:
#   easy   — ax + b = c, small integers, whole number answer
#   medium — ax + b = cx + d, or a(x + b) = c, larger numbers
#   hard   — fractions, decimals, brackets on both sides
# =============================================================================

import random
from fractions import Fraction


def generate(difficulty: str = "easy") -> dict:
    """Return one randomised linear equation problem at the given difficulty."""
    if difficulty == "easy":
        fn = random.choice([_type_ax_plus_b, _type_ax_minus_b])
    elif difficulty == "medium":
        fn = random.choice([_type_both_sides, _type_bracket_simple])
    else:
        fn = random.choice([_type_bracket_both_sides, _type_fraction_answer])
    return fn(difficulty)


# ---------------------------------------------------------------------------
# Problem type generators
# ---------------------------------------------------------------------------

def _type_ax_plus_b(difficulty: str) -> dict:
    """Form:  ax + b = c"""
    if difficulty == "easy":
        a = random.randint(2, 5)
        x = random.randint(1, 9)
        b = random.randint(1, 9)
    else:
        a = random.randint(3, 12)
        x = random.randint(2, 15)
        b = random.randint(2, 20)

    c = a * x + b

    question = f"Solve:   {a}x + {b} = {c}"
    explanation = (
        f"Step 1 — Subtract {b} from both sides:\n"
        f"         {a}x  =  {c - b}\n"
        f"Step 2 — Divide both sides by {a}:\n"
        f"         x  =  {x}\n"
        f"Check:   {a}({x}) + {b}  =  {a*x} + {b}  =  {c}  ✓"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        f"Start by subtracting {b} from both sides.",
        "hint2":       f"After subtracting {b}:  {a}x = {c - b}. Now divide both sides by {a}.",
        "hint3":       f"Divide {c - b} by {a} to find x.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_ax_minus_b(difficulty: str) -> dict:
    """Form:  ax − b = c"""
    if difficulty == "easy":
        a = random.randint(2, 5)
        x = random.randint(2, 9)
        b = random.randint(1, 8)
    else:
        a = random.randint(3, 10)
        x = random.randint(3, 15)
        b = random.randint(2, 18)

    c = a * x - b

    question = f"Solve:   {a}x \u2212 {b} = {c}"
    explanation = (
        f"Step 1 — Add {b} to both sides:\n"
        f"         {a}x  =  {c + b}\n"
        f"Step 2 — Divide both sides by {a}:\n"
        f"         x  =  {x}\n"
        f"Check:   {a}({x}) \u2212 {b}  =  {a*x} \u2212 {b}  =  {c}  ✓"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        f"Start by adding {b} to both sides to undo the subtraction.",
        "hint2":       f"After adding {b}:  {a}x = {c + b}. Now divide both sides by {a}.",
        "hint3":       f"Divide {c + b} by {a} to get x.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_both_sides(difficulty: str) -> dict:
    """Form:  ax + b = cx + d  (variable on both sides)"""
    if difficulty == "medium":
        x = random.randint(2, 10)
        a = random.randint(3, 8)
        c = random.randint(1, a - 1)
        b = random.randint(1, 10)
    else:
        x = random.randint(3, 15)
        a = random.randint(5, 12)
        c = random.randint(1, a - 1)
        b = random.randint(2, 15)

    d       = a * x + b - c * x
    diff_a  = a - c
    diff_d  = d - b

    question = f"Solve:   {a}x + {b} = {c}x + {d}"
    explanation = (
        f"Step 1 — Subtract {c}x from both sides:\n"
        f"         {diff_a}x + {b}  =  {d}\n"
        f"Step 2 — Subtract {b} from both sides:\n"
        f"         {diff_a}x  =  {diff_d}\n"
        f"Step 3 — Divide both sides by {diff_a}:\n"
        f"         x  =  {x}\n"
        f"Check:   {a}({x})+{b}={a*x+b}  and  {c}({x})+{d}={c*x+d}  ✓"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        f"Variable is on both sides — subtract {c}x from both sides first.",
        "hint2":       f"After collecting x terms:  {diff_a}x + {b} = {d}. Subtract {b}.",
        "hint3":       f"Divide {diff_d} by {diff_a} to find x.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_bracket_simple(difficulty: str) -> dict:
    """Form:  a(x + b) = c  or  a(x − b) = c"""
    a  = random.randint(2, 6)
    x  = random.randint(2, 10)
    b  = random.randint(1, 8)
    op = random.choice(["+", "\u2212"])

    if op == "+":
        c        = a * (x + b)
        expanded = f"{a}x + {a*b}"
        rhs2     = c - a * b
        h2       = f"After expanding: {expanded} = {c}. Subtract {a*b} from both sides."
        chk_inner = x + b
    else:
        c        = a * (x - b)
        expanded = f"{a}x \u2212 {a*b}"
        rhs2     = c + a * b
        h2       = f"After expanding: {expanded} = {c}. Add {a*b} to both sides."
        chk_inner = x - b

    question = f"Solve:   {a}(x {op} {b}) = {c}"
    explanation = (
        f"Step 1 — Expand the brackets:\n"
        f"         {expanded}  =  {c}\n"
        f"Step 2 — Isolate {a}x:\n"
        f"         {a}x  =  {rhs2}\n"
        f"Step 3 — Divide both sides by {a}:\n"
        f"         x  =  {x}\n"
        f"Check:   {a}({x} {op} {b}) = {a}({chk_inner}) = {c}  ✓"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Expand (multiply out) the bracket before anything else.",
        "hint2":       h2,
        "hint3":       f"After isolating {a}x, divide both sides by {a}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_bracket_both_sides(difficulty: str) -> dict:
    """Form:  a(x + b) = c(x + d)  (hard)"""
    a = random.randint(3, 7)
    c = random.randint(1, a - 1)
    b = random.randint(1, 6)
    x = random.randint(2, 12)

    # Ensure d is an integer: d = (a*(x+b) - c*x) / c
    lhs = a * (x + b)
    # Adjust x until d comes out as integer
    for _ in range(20):
        if (lhs - c * x) % c == 0:
            break
        x += 1
        lhs = a * (x + b)

    d      = (lhs - c * x) // c
    diff_a = a - c
    net    = c * d - a * b

    question = f"Solve:   {a}(x + {b}) = {c}(x + {d})"
    explanation = (
        f"Step 1 — Expand both brackets:\n"
        f"         {a}x + {a*b}  =  {c}x + {c*d}\n"
        f"Step 2 — Subtract {c}x from both sides:\n"
        f"         {diff_a}x + {a*b}  =  {c*d}\n"
        f"Step 3 — Subtract {a*b} from both sides:\n"
        f"         {diff_a}x  =  {net}\n"
        f"Step 4 — Divide by {diff_a}:\n"
        f"         x  =  {x}\n"
        f"Check:   {a}({x}+{b})={a*(x+b)}  and  {c}({x}+{d})={c*(x+d)}  ✓"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Expand BOTH brackets first, then collect like terms.",
        "hint2":       f"After expanding: {a}x + {a*b} = {c}x + {c*d}. Subtract {c}x.",
        "hint3":       f"After collecting: {diff_a}x = {net}. Divide by {diff_a}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_fraction_answer(difficulty: str) -> dict:
    """Form:  ax + b = c  with a non-integer answer  (hard)"""
    a = random.choice([2, 3, 4, 5, 6])
    b = random.randint(1, 8)
    c = random.randint(b + 1, b + a * 6)

    # Force a fractional answer
    while (c - b) % a == 0:
        c += 1

    frac         = Fraction(c - b, a)
    answer_float = round(float(frac), 4)

    question = f"Solve:   {a}x + {b} = {c}   (give answer as a decimal)"
    explanation = (
        f"Step 1 — Subtract {b} from both sides:\n"
        f"         {a}x  =  {c - b}\n"
        f"Step 2 — Divide both sides by {a}:\n"
        f"         x  =  {c-b}/{a}  =  {answer_float}\n"
        f"Check:   {a}({answer_float}) + {b} \u2248 {round(a*answer_float+b,2)}  ✓"
    )
    return {
        "question":    question,
        "answer":      answer_float,
        "hint":        f"Start by subtracting {b} from both sides.",
        "hint2":       f"After subtracting: {a}x = {c-b}. Divide both sides by {a}.",
        "hint3":       f"{c-b} \u00f7 {a} = {answer_float}. A decimal answer is fine here.",
        "explanation": explanation,
        "type":        "numeric",
    }