# =============================================================================
# problems/advanced/similar_triangles.py
# Randomised problem generator for Similar Triangles (SAT Advanced).
# =============================================================================

import random


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_find_missing_side, _type_scale_factor])
    elif difficulty == "medium":
        fn = random.choice([_type_proportion_solve, _type_indirect_measurement])
    else:
        fn = random.choice([_type_area_ratio, _type_perimeter_ratio])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_find_missing_side(difficulty: str) -> dict:
    """Given ratio a/b = c/?, find ?"""
    a = random.randint(2, 8)
    b = random.randint(2, 4) * a   # b is a multiple of a for clean answer
    c = random.randint(3, 10)
    x = b * c // a                  # integer answer guaranteed

    question = (
        f"△ABC ~ △DEF.\n"
        f"AB = {a},  DE = {b},  BC = {c}.\n"
        f"Find EF."
    )
    explanation = (
        f"Similar triangles: AB/DE = BC/EF\n"
        f"{a}/{b} = {c}/EF\n"
        f"Cross-multiply:  {a} × EF = {b} × {c} = {b*c}\n"
        f"EF = {b*c} / {a} = {x}"
    )
    return {
        "question":    question,
        "answer":      x,
        "hint":        "Set up a proportion: AB/DE = BC/EF.",
        "hint2":       f"{a}/{b} = {c}/EF  →  cross-multiply: {a} × EF = {b*c}.",
        "hint3":       f"EF = {b*c} / {a} = {x}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_scale_factor(difficulty: str) -> dict:
    """Find scale factor from two corresponding sides."""
    small = random.randint(3, 8)
    mult  = random.randint(2, 4)
    large = small * mult
    scale = mult  # integer scale factor

    question = (
        f"Two similar triangles have corresponding sides {small} and {large}.\n"
        f"What is the scale factor from the smaller to the larger triangle?"
    )
    explanation = (
        f"Scale factor = larger side / smaller side\n"
        f"= {large} / {small}\n"
        f"= {scale}"
    )
    return {
        "question":    question,
        "answer":      scale,
        "hint":        "Scale factor = larger corresponding side ÷ smaller corresponding side.",
        "hint2":       f"Scale factor = {large} / {small}.",
        "hint3":       f"Scale factor = {scale}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_proportion_solve(difficulty: str) -> dict:
    """More complex proportion — not an integer multiple."""
    p = random.randint(4, 9)
    q = random.randint(4, 9)
    r = random.randint(4, 9)
    # answer s = r*q/p; choose values so s is integer
    p = random.choice([2, 3, 4, 5, 6])
    q = p * random.randint(1, 4)    # q multiple of p
    r = random.randint(3, 12)
    s = r * q // p

    question = (
        f"△PQR ~ △STU.\n"
        f"PQ = {p},  ST = {q},  QR = {r}.\n"
        f"Find TU."
    )
    explanation = (
        f"Set up proportion: PQ/ST = QR/TU\n"
        f"{p}/{q} = {r}/TU\n"
        f"TU = {r} × {q} / {p} = {r*q} / {p} = {s}"
    )
    return {
        "question":    question,
        "answer":      s,
        "hint":        "PQ/ST = QR/TU.  Cross-multiply and solve.",
        "hint2":       f"TU = {r} × {q} / {p} = {r*q} / {p}.",
        "hint3":       f"TU = {s}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_indirect_measurement(difficulty: str) -> dict:
    """Shadow/height indirect measurement."""
    pole_h = random.choice([1, 2, 3])
    pole_s = random.choice([2, 3, 4])
    obj_s  = pole_s * random.randint(4, 10)
    obj_h  = pole_h * obj_s // pole_s

    question = (
        f"A {pole_h} m pole casts a shadow of {pole_s} m. "
        f"At the same time, a tree casts a shadow of {obj_s} m. "
        f"How tall is the tree?"
    )
    explanation = (
        f"The pole and tree form similar right triangles:\n"
        f"height / shadow = constant\n"
        f"{pole_h} / {pole_s} = h / {obj_s}\n"
        f"h = {pole_h} × {obj_s} / {pole_s}\n"
        f"h = {pole_h * obj_s} / {pole_s}\n"
        f"h = {obj_h} m"
    )
    return {
        "question":    question,
        "answer":      obj_h,
        "hint":        "height / shadow = same ratio for both objects.",
        "hint2":       f"{pole_h}/{pole_s} = h/{obj_s}  →  h = {pole_h} × {obj_s} / {pole_s}.",
        "hint3":       f"h = {obj_h} m.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_area_ratio(difficulty: str) -> dict:
    """Area scales by scale factor squared."""
    k    = random.randint(2, 5)
    area_small = random.choice([9, 16, 25, 36, 4])
    area_large = area_small * k * k

    question = (
        f"Two similar triangles have corresponding sides in ratio 1 : {k}. "
        f"The smaller triangle has area {area_small} cm². "
        f"Find the area of the larger triangle."
    )
    explanation = (
        f"Area ratio = (side ratio)²\n"
        f"Area ratio = {k}² = {k*k}\n"
        f"Larger area = {area_small} × {k*k} = {area_large} cm²"
    )
    return {
        "question":    question,
        "answer":      area_large,
        "hint":        "Area scales by the square of the scale factor.",
        "hint2":       f"Scale factor = {k}, so area ratio = {k}² = {k*k}.",
        "hint3":       f"Larger area = {area_small} × {k*k} = {area_large} cm².",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_perimeter_ratio(difficulty: str) -> dict:
    """Perimeter scales by scale factor (linearly)."""
    k     = random.randint(2, 5)
    p_s   = random.randint(12, 30)
    p_l   = p_s * k

    question = (
        f"Two similar triangles have sides in ratio 1 : {k}. "
        f"The smaller triangle has perimeter {p_s} cm. "
        f"Find the perimeter of the larger triangle."
    )
    explanation = (
        f"Perimeter scales by the same ratio as the sides.\n"
        f"Larger perimeter = smaller perimeter × {k}\n"
        f"= {p_s} × {k} = {p_l} cm"
    )
    return {
        "question":    question,
        "answer":      p_l,
        "hint":        "Perimeters scale by the same factor as the sides.",
        "hint2":       f"Larger perimeter = {p_s} × {k}.",
        "hint3":       f"Perimeter = {p_l} cm.",
        "explanation": explanation,
        "type":        "numeric",
    }
