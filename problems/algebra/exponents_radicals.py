# =============================================================================
# problems/algebra/exponents_radicals.py
# Randomised problem generator for Exponents & Radicals.
# =============================================================================

import random
import math


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_product_rule, _type_power_rule])
    elif difficulty == "medium":
        fn = random.choice([_type_quotient_rule, _type_simplify_radical])
    else:
        fn = random.choice([_type_combined_rules, _type_fractional_exp])
    return fn(difficulty)


# ---------------------------------------------------------------------------
# Perfect squares for radical problems
# ---------------------------------------------------------------------------
PERFECT_SQUARES = [4, 9, 16, 25, 36, 49, 64, 81, 100]


def _type_product_rule(difficulty: str) -> dict:
    """bᵐ × bⁿ = ?"""
    base = random.choice([2, 3, 4, 5])
    m    = random.randint(1, 4)
    n    = random.randint(1, 4)
    ans  = base ** (m + n)

    question    = f"Simplify:   {base}\u00b3 \u00d7 {base}\u2074"
    # Override with actual values
    question    = f"Simplify:   {base}^{m} \u00d7 {base}^{n}"
    explanation = (
        f"Same base ({base}) — use the Product Rule: add the exponents.\n"
        f"{base}^{m} \u00d7 {base}^{n} = {base}^({m}+{n}) = {base}^{m+n} = {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Same base — add the exponents (Product Rule).",
        "hint2":       f"{base}^{m} × {base}^{n} = {base}^({m}+{n}) = {base}^{m+n}.",
        "hint3":       f"{base}^{m+n} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_power_rule(difficulty: str) -> dict:
    """(bᵐ)ⁿ = ?"""
    base = random.choice([2, 3, 5])
    m    = random.randint(1, 3)
    n    = random.randint(2, 3)
    ans  = base ** (m * n)

    question    = f"Simplify:   ({base}^{m})^{n}"
    explanation = (
        f"Power of a power — multiply the exponents.\n"
        f"({base}^{m})^{n} = {base}^({m}\u00d7{n}) = {base}^{m*n} = {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Power of a power rule: multiply the exponents.",
        "hint2":       f"({base}^{m})^{n} = {base}^({m}×{n}) = {base}^{m*n}.",
        "hint3":       f"{base}^{m*n} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_quotient_rule(difficulty: str) -> dict:
    """bᵐ ÷ bⁿ = ?"""
    base = random.choice([2, 3, 4, 5])
    n    = random.randint(1, 3)
    diff = random.randint(1, 4)
    m    = n + diff
    ans  = base ** diff

    question    = f"Simplify:   {base}^{m} \u00f7 {base}^{n}"
    explanation = (
        f"Same base ({base}) — use the Quotient Rule: subtract the exponents.\n"
        f"{base}^{m} \u00f7 {base}^{n} = {base}^({m}\u2212{n}) = {base}^{diff} = {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Same base — subtract the exponents (Quotient Rule).",
        "hint2":       f"{base}^{m} ÷ {base}^{n} = {base}^({m}-{n}) = {base}^{diff}.",
        "hint3":       f"{base}^{diff} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_simplify_radical(difficulty: str) -> dict:
    """√(ps × k) where ps is a perfect square."""
    ps  = random.choice(PERFECT_SQUARES)
    k   = random.choice([2, 3, 5, 6, 7])
    n   = ps * k
    ans = int(math.sqrt(ps))   # coefficient outside radical

    question    = f"Simplify:   \u221a{n}   (give the coefficient outside the radical)"
    explanation = (
        f"Find the largest perfect square factor of {n}:\n"
        f"{n} = {ps} \u00d7 {k}\n"
        f"\u221a{n} = \u221a{ps} \u00d7 \u221a{k}\n"
        f"= {ans}\u221a{k}\n"
        f"The coefficient outside the radical is {ans}."
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        f"Find a perfect square that divides {n}.",
        "hint2":       f"{n} = {ps} × {k}. So √{n} = √{ps} × √{k}.",
        "hint3":       f"√{ps} = {ans}. The coefficient is {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_combined_rules(difficulty: str) -> dict:
    """bᵐ × bⁿ ÷ bᵖ = ?"""
    base = random.choice([2, 3])
    m    = random.randint(3, 6)
    n    = random.randint(2, 4)
    p    = random.randint(1, m + n - 1)
    exp  = m + n - p
    ans  = base ** exp

    question    = f"Simplify:   {base}^{m} \u00d7 {base}^{n} \u00f7 {base}^{p}"
    explanation = (
        f"Apply product then quotient rules:\n"
        f"{base}^{m} \u00d7 {base}^{n} = {base}^{m+n}\n"
        f"{base}^{m+n} \u00f7 {base}^{p} = {base}^({m+n}\u2212{p}) = {base}^{exp}\n"
        f"= {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        "Apply product rule first (add), then quotient rule (subtract).",
        "hint2":       f"After product rule: {base}^{m+n}. Then subtract {p}.",
        "hint3":       f"{base}^{exp} = {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_fractional_exp(difficulty: str) -> dict:
    """b^(1/n) = ?"""
    pairs = [(8, 3, 2), (27, 3, 3), (16, 4, 2),
             (32, 5, 2), (64, 3, 4), (125, 3, 5)]
    base, root, ans = random.choice(pairs)

    question    = f"Evaluate:   {base}^(1/{root})"
    explanation = (
        f"{base}^(1/{root}) = {root}\u221a{base}\n"
        f"Find the {root}th root of {base}:\n"
        f"{ans}^{root} = {base}\n"
        f"Answer: {ans}"
    )
    return {
        "question":    question,
        "answer":      ans,
        "hint":        f"b^(1/n) means the nth root of b. Find the {root}th root of {base}.",
        "hint2":       f"What number raised to the power {root} gives {base}?",
        "hint3":       f"{ans}^{root} = {base}. Answer: {ans}.",
        "explanation": explanation,
        "type":        "numeric",
    }