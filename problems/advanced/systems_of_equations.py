# =============================================================================
# problems/advanced/systems_of_equations.py
# Randomised problem generator for Systems of Equations (SAT Advanced).
# =============================================================================

import random


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_substitution_simple, _type_substitution_y_given])
    elif difficulty == "medium":
        fn = random.choice([_type_elimination_direct, _type_substitution_rearrange])
    else:
        fn = random.choice([_type_elimination_scale, _type_word_problem])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_substitution_y_given(difficulty: str) -> dict:
    """y = constant; ax + y = c  →  find x."""
    y = random.randint(-6, 6)
    a = random.randint(2, 6)
    x = random.randint(-5, 5)
    c = a * x + y

    question = (
        f"Solve the system:\n"
        f"   y = {y}\n"
        f"   {a}x + y = {c}\n"
        f"Find the value of x."
    )
    explanation = (
        f"Substitute y = {y} into the second equation:\n"
        f"{a}x + {y} = {c}\n"
        f"{a}x = {c - y}\n"
        f"x = {c - y} / {a} = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Substitute y into the second equation.",
        "hint2":       f"After substituting: {a}x + {y} = {c}  →  {a}x = {c-y}.",
        "hint3":       f"x = {c-y} / {a} = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_substitution_simple(difficulty: str) -> dict:
    """y = mx + b; x + y = c  →  find x."""
    m = random.randint(-3, 3)
    while m == 0:
        m = random.randint(-3, 3)
    b  = random.randint(-5, 5)
    x  = random.randint(-4, 4)
    y  = m * x + b
    c  = x + y

    question = (
        f"Solve the system:\n"
        f"   y = {m}x + {b}\n"
        f"   x + y = {c}\n"
        f"Find the value of x."
    )
    explanation = (
        f"Substitute y = {m}x + {b} into x + y = {c}:\n"
        f"x + ({m}x + {b}) = {c}\n"
        f"{1+m}x + {b} = {c}\n"
        f"{1+m}x = {c - b}\n"
        f"x = {c - b} / {1+m} = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Replace y in the second equation using the first equation.",
        "hint2":       f"x + ({m}x + {b}) = {c}  →  {1+m}x = {c - b}.",
        "hint3":       f"x = {c - b} / {1+m} = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_elimination_direct(difficulty: str) -> dict:
    """ax + by = c1, dx − by = c2  →  add to eliminate y, find x."""
    a  = random.randint(2, 5)
    d  = random.randint(2, 5)
    b  = random.randint(2, 5)
    x  = random.randint(-4, 4)
    y  = random.randint(-4, 4)
    c1 = a * x + b * y
    c2 = d * x - b * y

    question = (
        f"Solve the system:\n"
        f"   {a}x + {b}y = {c1}\n"
        f"   {d}x − {b}y = {c2}\n"
        f"Find the value of x."
    )
    explanation = (
        f"Add the two equations to eliminate y:\n"
        f"({a}x + {b}y) + ({d}x − {b}y) = {c1} + {c2}\n"
        f"{a+d}x = {c1+c2}\n"
        f"x = {c1+c2} / {a+d} = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Add both equations — the y terms will cancel.",
        "hint2":       f"Sum of left sides: {a+d}x.  Sum of right sides: {c1+c2}.",
        "hint3":       f"x = {c1+c2} / {a+d} = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_substitution_rearrange(difficulty: str) -> dict:
    """ax + by = c, x = d  →  find y."""
    a  = random.randint(2, 5)
    b  = random.randint(2, 5)
    x  = random.randint(-4, 4)
    y  = random.randint(-4, 4)
    c  = a * x + b * y

    question = (
        f"Solve the system:\n"
        f"   {a}x + {b}y = {c}\n"
        f"   x = {x}\n"
        f"Find the value of y."
    )
    explanation = (
        f"Substitute x = {x} into the first equation:\n"
        f"{a}({x}) + {b}y = {c}\n"
        f"{a*x} + {b}y = {c}\n"
        f"{b}y = {c - a*x}\n"
        f"y = {c - a*x} / {b} = {y}"
    )
    return {
        "question":    question,
        "answer":      y,
        "hint":        f"Substitute x = {x} into the first equation.",
        "hint2":       f"After substituting: {a*x} + {b}y = {c}  →  {b}y = {c-a*x}.",
        "hint3":       f"y = {c-a*x} / {b} = {y}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_elimination_scale(difficulty: str) -> dict:
    """Scale one equation first, then eliminate."""
    a  = random.randint(2, 4)
    b  = random.randint(2, 4)
    d  = random.randint(2, 4)
    x  = random.randint(-3, 3)
    y  = random.randint(-3, 3)
    c1 = a * x + b * y
    c2 = d * x + b * y  # same b coefficient — scale eq1 by d, eq2 by a and subtract

    # Ensure c1 != c2 (otherwise immediate solution by subtraction without scaling)
    while c1 == c2:
        x = random.randint(-3, 3)
        y = random.randint(-3, 3)
        c1 = a * x + b * y
        c2 = d * x + b * y

    question = (
        f"Solve the system:\n"
        f"   {a}x + {b}y = {c1}\n"
        f"   {d}x + {b}y = {c2}\n"
        f"Find the value of x."
    )
    explanation = (
        f"Subtract Equation 2 from Equation 1 to eliminate y:\n"
        f"({a}x + {b}y) − ({d}x + {b}y) = {c1} − {c2}\n"
        f"{a-d}x = {c1 - c2}\n"
        f"x = {c1-c2} / {a-d} = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "The y coefficients are equal — subtract one equation from the other.",
        "hint2":       f"({a}−{d})x = {c1}−{c2}  →  {a-d}x = {c1-c2}.",
        "hint3":       f"x = {c1-c2} / {a-d} = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_word_problem(difficulty: str) -> dict:
    """Two quantities, two equations — find one of the quantities."""
    price_a = random.randint(2, 6)
    price_b = random.randint(2, 6)
    while price_a == price_b:
        price_b = random.randint(2, 6)
    count_a = random.randint(3, 8)
    count_b = random.randint(3, 8)
    total   = price_a * count_a + price_b * count_b
    names   = [("apples", "pears"), ("pens", "markers"), ("tickets", "passes")]
    item_a, item_b = random.choice(names)

    question = (
        f"{item_a.capitalize()} cost ${price_a} each and {item_b} cost ${price_b} each. "
        f"A total of {count_a + count_b} items were bought for ${total}. "
        f"How many {item_a} were purchased?"
    )
    explanation = (
        f"Let a = number of {item_a},  b = number of {item_b}.\n"
        f"Equation 1 (count):  a + b = {count_a + count_b}\n"
        f"Equation 2 (cost):   {price_a}a + {price_b}b = {total}\n\n"
        f"From Eq 1:  b = {count_a + count_b} − a\n"
        f"Substitute into Eq 2:\n"
        f"{price_a}a + {price_b}({count_a + count_b} − a) = {total}\n"
        f"{price_a}a + {price_b*(count_a+count_b)} − {price_b}a = {total}\n"
        f"{price_a - price_b}a = {total - price_b*(count_a+count_b)}\n"
        f"a = {count_a}"
    )
    return {
        "question":    question,
        "answer":      count_a,
        "hint":        f"Let a = {item_a} and b = {item_b}. Write two equations: one for count, one for cost.",
        "hint2":       f"a + b = {count_a+count_b}  and  {price_a}a + {price_b}b = {total}.",
        "hint3":       f"Substitute b = {count_a+count_b} − a into the cost equation and solve.",
        "explanation": explanation,
        "type":        "numeric",
    }
