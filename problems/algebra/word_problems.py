# =============================================================================
# problems/algebra/word_problems.py
# Randomised word problem generator.
# =============================================================================

import random


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_number, _type_price])
    elif difficulty == "medium":
        fn = random.choice([_type_consecutive, _type_age_simple])
    else:
        fn = random.choice([_type_age_future, _type_distance])
    return fn(difficulty)


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def _type_number(difficulty: str) -> dict:
    """A number plus/times something equals a value."""
    x   = random.randint(3, 15)
    m   = random.randint(2, 5)
    b   = random.randint(1, 10)
    rhs = m * x + b

    question = (
        f"A number is multiplied by {m} and then {b} is added. "
        f"The result is {rhs}. What is the number?"
    )
    explanation = (
        f"Let x = the number\n"
        f"Equation: {m}x + {b} = {rhs}\n"
        f"Subtract {b}: {m}x = {rhs - b}\n"
        f"Divide by {m}: x = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        f"Let x = the number. Write: {m}x + {b} = {rhs}.",
        "hint2":       f"Subtract {b} from both sides: {m}x = {rhs - b}.",
        "hint3":       f"Divide by {m}: x = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_price(difficulty: str) -> dict:
    """Two items, one costs more than the other, total given."""
    extra = random.randint(3, 20)
    item2 = random.randint(5, 30)
    item1 = item2 + extra
    total = item1 + item2

    names = random.choice([
        ("book", "pen"),
        ("shirt", "hat"),
        ("bag", "wallet"),
        ("notebook", "eraser"),
    ])
    n1, n2 = names

    question = (
        f"A {n1} costs ${extra} more than a {n2}. "
        f"Together they cost ${total}. "
        f"What is the cost of the {n2}?"
    )
    explanation = (
        f"Let x = cost of {n2}\n"
        f"Then x + {extra} = cost of {n1}\n"
        f"Equation: x + (x + {extra}) = {total}\n"
        f"2x + {extra} = {total}\n"
        f"2x = {total - extra}\n"
        f"x = {item2}"
    )
    return {
        "question":    question,
        "answer":      item2,
        "hint":        f"Let x = cost of {n2}. The {n1} costs x + {extra}.",
        "hint2":       f"Equation: x + (x + {extra}) = {total}. Simplify to 2x + {extra} = {total}.",
        "hint3":       f"2x = {total - extra}, so x = {item2}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_consecutive(difficulty: str) -> dict:
    """Sum of consecutive integers."""
    x     = random.randint(5, 25)
    count = random.choice([2, 3])
    total = sum(range(x, x + count))

    if count == 2:
        question = (
            f"The sum of two consecutive integers is {total}. "
            f"What is the smaller integer?"
        )
        explanation = (
            f"Let x = smaller integer, x+1 = larger\n"
            f"x + (x+1) = {total}\n"
            f"2x + 1 = {total}\n"
            f"2x = {total - 1}\n"
            f"x = {x}"
        )
        hint3 = f"2x + 1 = {total} → 2x = {total-1} → x = {x}."
    else:
        question = (
            f"The sum of three consecutive integers is {total}. "
            f"What is the smallest integer?"
        )
        explanation = (
            f"Let x, x+1, x+2 be the integers\n"
            f"x + (x+1) + (x+2) = {total}\n"
            f"3x + 3 = {total}\n"
            f"3x = {total - 3}\n"
            f"x = {x}"
        )
        hint3 = f"3x + 3 = {total} → 3x = {total-3} → x = {x}."

    return {
        "question":    question,
        "answer":      x,
        "hint":        f"Let x = smallest integer. Write expressions for all {count} integers.",
        "hint2":       f"Set up the equation and simplify.",
        "hint3":       hint3,
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_age_simple(difficulty: str) -> dict:
    """A is n times as old as B. Total age known."""
    b_age   = random.randint(4, 15)
    factor  = random.randint(2, 4)
    a_age   = factor * b_age
    total   = a_age + b_age

    names = random.choice([
        ("Alex", "Sam"),
        ("Maria", "her brother"),
        ("James", "his sister"),
        ("Nina", "Tom"),
    ])
    n1, n2 = names

    question = (
        f"{n1} is {factor} times as old as {n2}. "
        f"Their combined age is {total}. "
        f"How old is {n2}?"
    )
    explanation = (
        f"Let x = {n2}'s age\n"
        f"Then {factor}x = {n1}'s age\n"
        f"Equation: {factor}x + x = {total}\n"
        f"{factor + 1}x = {total}\n"
        f"x = {b_age}"
    )
    return {
        "question":    question,
        "answer":      b_age,
        "hint":        f"Let x = {n2}'s age. Then {n1}'s age = {factor}x.",
        "hint2":       f"Equation: {factor}x + x = {total}. So {factor+1}x = {total}.",
        "hint3":       f"x = {total} ÷ {factor+1} = {b_age}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_age_future(difficulty: str) -> dict:
    """Current age given relative relationship plus future condition."""
    b_now   = random.randint(5, 15)
    factor  = random.randint(2, 4)
    a_now   = factor * b_now
    years   = random.randint(2, 10)
    # Future: a_now + years = mult * (b_now + years)
    future_mult = round((a_now + years) / (b_now + years), 1)

    question = (
        f"A parent is currently {factor} times as old as their child. "
        f"In {years} years, the parent will be {int(a_now + years)} years old. "
        f"How old is the child now?"
    )
    explanation = (
        f"Let x = child's age now\n"
        f"Parent's age now = {factor}x\n"
        f"In {years} years, parent's age: {factor}x + {years} = {int(a_now + years)}\n"
        f"{factor}x = {int(a_now + years) - years}\n"
        f"x = {b_now}"
    )
    return {
        "question":    question,
        "answer":      b_now,
        "hint":        f"Let x = child's age now. Parent's age = {factor}x.",
        "hint2":       f"In {years} years: {factor}x + {years} = {int(a_now+years)}.",
        "hint3":       f"{factor}x = {int(a_now+years-years)} → x = {b_now}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_distance(difficulty: str) -> dict:
    """D = S × T problems."""
    speed = random.choice([40, 50, 60, 80, 100])
    time  = random.randint(2, 6)
    dist  = speed * time

    scenarios = [
        (
            f"A car travels at {speed} km/h for {time} hours. "
            f"How many kilometres does it travel?",
            dist,
            f"Distance = Speed × Time = {speed} × {time} = {dist} km",
        ),
        (
            f"A train travels {dist} km at {speed} km/h. "
            f"How many hours does the journey take?",
            time,
            f"Time = Distance ÷ Speed = {dist} ÷ {speed} = {time} hours",
        ),
    ]

    question, answer, explanation = random.choice(scenarios)

    return {
        "question":    question,
        "answer":      answer,
        "hint":        "Use the formula: Distance = Speed × Time.",
        "hint2":       f"Rearrange for what you need: D={speed}×{time} or T={dist}÷{speed}.",
        "hint3":       explanation,
        "explanation": explanation,
        "type":        "numeric",
    }