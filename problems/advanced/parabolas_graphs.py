# =============================================================================
# problems/advanced/parabolas_graphs.py
# Randomised problem generator for Parabolas & Graphs (SAT Advanced).
# =============================================================================

import random


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_vertex_from_vertex_form, _type_y_intercept])
    elif difficulty == "medium":
        fn = random.choice([_type_axis_of_symmetry, _type_vertex_y_from_standard])
    else:
        fn = random.choice([_type_vertex_x_from_standard, _type_min_max_value])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_vertex_from_vertex_form(difficulty: str) -> dict:
    """Find vertex x-coordinate from y = a(x-h)^2 + k."""
    h = random.randint(-6, 6)
    k = random.randint(-8, 8)
    a = random.choice([-3, -2, -1, 1, 2, 3])

    # Format: y = a(x − h)² + k   or   y = a(x + |h|)² + k
    if h >= 0:
        bracket = f"(x − {h})" if h != 0 else "x"
    else:
        bracket = f"(x + {abs(h)})"

    if a == 1:
        a_str = ""
    elif a == -1:
        a_str = "−"
    elif a < 0:
        a_str = f"−{abs(a)}"
    else:
        a_str = str(a)

    k_str = f" + {k}" if k > 0 else (f" − {abs(k)}" if k < 0 else "")
    eq = f"y = {a_str}{bracket}²{k_str}"

    question = f"What is the x-coordinate of the vertex of  {eq}?"
    explanation = (
        f"The equation is in vertex form y = a(x − h)² + k.\n"
        f"The vertex is at (h, k).\n"
        f"h = {h}   (note: sign inside the bracket is flipped)\n"
        f"Vertex x-coordinate = {h}"
    )
    return {
        "question":    question,
        "answer":      h,
        "hint":        "In y = a(x − h)² + k, the vertex is at (h, k).",
        "hint2":       f"h is the value that makes the bracket zero. In {bracket}, that is {h}.",
        "hint3":       f"Vertex x-coordinate = {h}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_y_intercept(difficulty: str) -> dict:
    """Find y-intercept (c) from y = ax² + bx + c."""
    a = random.choice([-3, -2, -1, 1, 2, 3])
    b = random.randint(-6, 6)
    c = random.randint(-10, 10)

    b_str = f" + {b}x" if b > 0 else (f" − {abs(b)}x" if b != 0 else "")
    c_str = f" + {c}" if c > 0 else (f" − {abs(c)}" if c != 0 else "")
    eq    = f"y = {a}x²{b_str}{c_str}"

    question = f"What is the y-intercept of the parabola  {eq}?"
    explanation = (
        f"The y-intercept occurs where x = 0.\n"
        f"Substitute x = 0:\n"
        f"y = {a}(0)² + {b}(0) + {c}\n"
        f"y = {c}"
    )
    return {
        "question":    question,
        "answer":      c,
        "hint":        "Substitute x = 0 into the equation.",
        "hint2":       f"y = {a}(0)² + {b}(0) + {c} = {c}.",
        "hint3":       f"y-intercept = {c}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_axis_of_symmetry(difficulty: str) -> dict:
    """Find axis of symmetry x = −b/(2a) from standard form."""
    a = random.choice([1, 2, 3, -1, -2, -3])
    # Choose x for the axis so answer is integer: axis = -b/(2a) = integer
    axis = random.randint(-5, 5)
    b    = -2 * a * axis   # ensures -b/(2a) = axis
    c    = random.randint(-10, 10)

    b_str = f" + {b}x" if b > 0 else (f" − {abs(b)}x" if b != 0 else "")
    c_str = f" + {c}" if c > 0 else (f" − {abs(c)}" if c != 0 else "")
    eq    = f"y = {a}x²{b_str}{c_str}"

    question = f"Find the axis of symmetry of the parabola  {eq}."
    explanation = (
        f"Axis of symmetry: x = −b/(2a)\n"
        f"a = {a},  b = {b}\n"
        f"x = −({b}) / (2 × {a})\n"
        f"x = {-b} / {2*a}\n"
        f"x = {axis}"
    )
    return {
        "question":    question,
        "answer":      axis,
        "hint":        "Axis of symmetry: x = −b/(2a).",
        "hint2":       f"a = {a}, b = {b}. Compute −({b}) / (2 × {a}).",
        "hint3":       f"x = {-b} / {2*a} = {axis}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_vertex_y_from_standard(difficulty: str) -> dict:
    """Find vertex y-coordinate from standard form."""
    a    = random.choice([1, 2, -1, -2])
    axis = random.randint(-4, 4)
    b    = -2 * a * axis
    c    = random.randint(-10, 10)
    vy   = a * axis * axis + b * axis + c  # vertex y

    b_str = f" + {b}x" if b > 0 else (f" − {abs(b)}x" if b != 0 else "")
    c_str = f" + {c}" if c > 0 else (f" − {abs(c)}" if c != 0 else "")
    eq    = f"y = {a}x²{b_str}{c_str}"

    question = (
        f"For the parabola  {eq},\n"
        f"the axis of symmetry is x = {axis}.\n"
        f"Find the y-coordinate of the vertex."
    )
    explanation = (
        f"Substitute x = {axis} into the equation:\n"
        f"y = {a}({axis})² + {b}({axis}) + {c}\n"
        f"y = {a * axis**2} + {b * axis} + {c}\n"
        f"y = {vy}"
    )
    return {
        "question":    question,
        "answer":      vy,
        "hint":        "The vertex y is found by substituting the axis of symmetry into the equation.",
        "hint2":       f"y = {a}({axis})² + {b}({axis}) + {c}.",
        "hint3":       f"y = {a * axis**2 + b * axis} + {c} = {vy}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_vertex_x_from_standard(difficulty: str) -> dict:
    """Find vertex x-coordinate from standard form."""
    a    = random.choice([1, 2, 3, -1, -2, -3])
    axis = random.randint(-5, 5)
    b    = -2 * a * axis
    c    = random.randint(-10, 10)

    b_str = f" + {b}x" if b > 0 else (f" − {abs(b)}x" if b != 0 else "")
    c_str = f" + {c}" if c > 0 else (f" − {abs(c)}" if c != 0 else "")
    eq    = f"y = {a}x²{b_str}{c_str}"

    question = (
        f"Find the x-coordinate of the vertex of the parabola  {eq}."
    )
    explanation = (
        f"x-coordinate of vertex = −b/(2a)\n"
        f"= −({b}) / (2 × {a})\n"
        f"= {-b} / {2*a}\n"
        f"= {axis}"
    )
    return {
        "question":    question,
        "answer":      axis,
        "hint":        "Vertex x = −b/(2a).",
        "hint2":       f"= −({b}) / (2 × {a}) = {-b}/{2*a}.",
        "hint3":       f"Vertex x = {axis}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_min_max_value(difficulty: str) -> dict:
    """Find minimum or maximum y-value (vertex y-coordinate)."""
    a    = random.choice([1, 2, -1, -2])
    axis = random.randint(-4, 4)
    b    = -2 * a * axis
    c    = random.randint(-8, 8)
    vy   = a * axis * axis + b * axis + c

    min_or_max = "minimum" if a > 0 else "maximum"

    b_str = f" + {b}x" if b > 0 else (f" − {abs(b)}x" if b != 0 else "")
    c_str = f" + {c}" if c > 0 else (f" − {abs(c)}" if c != 0 else "")
    eq    = f"y = {a}x²{b_str}{c_str}"

    question = f"What is the {min_or_max} value of  {eq}?"
    explanation = (
        f"The {min_or_max} value is the y-coordinate of the vertex.\n"
        f"Step 1: Axis of symmetry x = −b/(2a) = {-b}/{2*a} = {axis}\n"
        f"Step 2: y = {a}({axis})² + {b}({axis}) + {c}\n"
        f"y = {a*axis**2} + {b*axis} + {c} = {vy}\n"
        f"The {min_or_max} value is {vy}."
    )
    return {
        "question":    question,
        "answer":      vy,
        "hint":        f"The {min_or_max} value is the y-coordinate of the vertex.",
        "hint2":       f"Find vertex x = −b/(2a) = {axis}, then substitute into the equation.",
        "hint3":       f"y = {vy}.",
        "explanation": explanation,
        "type":        "numeric",
    }
