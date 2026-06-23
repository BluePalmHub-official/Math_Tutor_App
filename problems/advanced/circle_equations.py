# =============================================================================
# problems/advanced/circle_equations.py
# Randomised problem generator for Circle Equations (SAT Advanced).
# =============================================================================

import random

PI = 3.14159


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_radius, _type_center_x])
    elif difficulty == "medium":
        fn = random.choice([_type_center_y, _type_area_from_equation])
    else:
        fn = random.choice([_type_circumference, _type_radius_from_general])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_radius(difficulty: str) -> dict:
    """Find radius from (x-h)²+(y-k)²=r²."""
    h   = random.randint(-6, 6)
    k   = random.randint(-6, 6)
    r   = random.randint(2, 10)
    r2  = r * r

    h_str = f"x − {h}" if h >= 0 else f"x + {abs(h)}"
    k_str = f"y − {k}" if k >= 0 else f"y + {abs(k)}"

    question = (
        f"Find the radius of the circle:\n"
        f"   ({h_str})² + ({k_str})² = {r2}"
    )
    explanation = (
        f"Standard form: (x − h)² + (y − k)² = r²\n"
        f"r² = {r2}\n"
        f"r = √{r2} = {r}"
    )
    return {
        "question":    question,
        "answer":      r,
        "hint":        "The radius is the square root of the right-hand side.",
        "hint2":       f"r² = {r2}.  Take the square root.",
        "hint3":       f"r = √{r2} = {r}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_center_x(difficulty: str) -> dict:
    """Find x-coordinate of center."""
    h  = random.randint(-7, 7)
    k  = random.randint(-7, 7)
    r  = random.randint(2, 9)
    r2 = r * r

    h_str = f"x − {h}" if h >= 0 else f"x + {abs(h)}"
    k_str = f"y − {k}" if k >= 0 else f"y + {abs(k)}"

    question = (
        f"What is the x-coordinate of the center of:\n"
        f"   ({h_str})² + ({k_str})² = {r2}?"
    )
    explanation = (
        f"Standard form: (x − h)² + (y − k)² = r²\n"
        f"The bracket ({h_str}) equals (x − {h}), so h = {h}.\n"
        f"x-coordinate of center = {h}"
    )
    return {
        "question":    question,
        "answer":      h,
        "hint":        "The center is (h, k) where the equation is (x − h)²+(y − k)²=r².",
        "hint2":       f"({h_str}) = (x − {h}), so h = {h}.",
        "hint3":       f"x-coordinate = {h}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_center_y(difficulty: str) -> dict:
    """Find y-coordinate of center."""
    h  = random.randint(-7, 7)
    k  = random.randint(-7, 7)
    r  = random.randint(2, 9)
    r2 = r * r

    h_str = f"x − {h}" if h >= 0 else f"x + {abs(h)}"
    k_str = f"y − {k}" if k >= 0 else f"y + {abs(k)}"

    question = (
        f"What is the y-coordinate of the center of:\n"
        f"   ({h_str})² + ({k_str})² = {r2}?"
    )
    explanation = (
        f"Standard form: (x − h)² + (y − k)² = r²\n"
        f"The bracket ({k_str}) = (y − {k}), so k = {k}.\n"
        f"y-coordinate of center = {k}"
    )
    return {
        "question":    question,
        "answer":      k,
        "hint":        "The center is (h, k). Read k from the y bracket.",
        "hint2":       f"({k_str}) = (y − {k}), so k = {k}.",
        "hint3":       f"y-coordinate = {k}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_area_from_equation(difficulty: str) -> dict:
    """Find area (in terms of a multiple of pi) from equation."""
    h  = random.randint(-5, 5)
    k  = random.randint(-5, 5)
    r  = random.randint(2, 8)
    r2 = r * r
    # Express area as a number (r²π rounded to 2 dp using π=3.14)
    area = round(PI * r2, 2)

    h_str = f"x − {h}" if h >= 0 else f"x + {abs(h)}"
    k_str = f"y − {k}" if k >= 0 else f"y + {abs(k)}"

    question = (
        f"Find the area of the circle (use π = 3.14, round to 2 dp):\n"
        f"   ({h_str})² + ({k_str})² = {r2}"
    )
    explanation = (
        f"r² = {r2},  so r = {r}\n"
        f"Area = π r² = 3.14 × {r2} = {area}"
    )
    return {
        "question":    question,
        "answer":      area,
        "hint":        "Area = πr². Read r² from the right-hand side of the equation.",
        "hint2":       f"r² = {r2}.  Area = 3.14 × {r2}.",
        "hint3":       f"Area = {area}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_circumference(difficulty: str) -> dict:
    """Find circumference from circle equation."""
    h  = random.randint(-5, 5)
    k  = random.randint(-5, 5)
    r  = random.randint(2, 8)
    r2 = r * r
    c  = round(2 * PI * r, 2)

    h_str = f"x − {h}" if h >= 0 else f"x + {abs(h)}"
    k_str = f"y − {k}" if k >= 0 else f"y + {abs(k)}"

    question = (
        f"Find the circumference of the circle (use π = 3.14, round to 2 dp):\n"
        f"   ({h_str})² + ({k_str})² = {r2}"
    )
    explanation = (
        f"r² = {r2},  so r = √{r2} = {r}\n"
        f"Circumference = 2πr = 2 × 3.14 × {r} = {c}"
    )
    return {
        "question":    question,
        "answer":      c,
        "hint":        "First find r = √(right-hand side), then use C = 2πr.",
        "hint2":       f"r = √{r2} = {r}.  C = 2 × 3.14 × {r}.",
        "hint3":       f"C = {c}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_radius_from_general(difficulty: str) -> dict:
    """Complete the square to find radius from general form."""
    h  = random.randint(-4, 4)
    k  = random.randint(-4, 4)
    r  = random.randint(3, 7)
    r2 = r * r

    # General form: x²+y²-2h·x-2k·y + (h²+k²-r²) = 0
    D = -2 * h
    E = -2 * k
    F = h * h + k * k - r2

    d_str = f" + {D}x" if D > 0 else (f" − {abs(D)}x" if D != 0 else "")
    e_str = f" + {E}y" if E > 0 else (f" − {abs(E)}y" if E != 0 else "")
    f_str = f" + {F}" if F > 0 else (f" − {abs(F)}" if F != 0 else "")

    question = (
        f"Find the radius of the circle:\n"
        f"   x² + y²{d_str}{e_str}{f_str} = 0"
    )
    add_x  = (D // 2) ** 2 if D % 2 == 0 else 0  # always works since D = -2h
    add_y  = (E // 2) ** 2 if E % 2 == 0 else 0
    explanation = (
        f"Complete the square:\n"
        f"(x² {d_str}) + (y² {e_str}) = {-F}\n"
        f"(x + {D//2})² − {add_x} + (y + {E//2})² − {add_y} = {-F}\n"
        f"(x − {h})² + (y − {k})² = {-F} + {add_x} + {add_y}\n"
        f"(x − {h})² + (y − {k})² = {r2}\n"
        f"r = √{r2} = {r}"
    )
    return {
        "question":    question,
        "answer":      r,
        "hint":        "Rearrange to standard form by completing the square for x and y.",
        "hint2":       f"Group: (x²{d_str}) + (y²{e_str}) = {-F}.",
        "hint3":       f"After completing the square: r² = {r2}, so r = {r}.",
        "explanation": explanation,
        "type":        "numeric",
    }
