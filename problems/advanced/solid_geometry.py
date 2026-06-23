# =============================================================================
# problems/advanced/solid_geometry.py
# Randomised problem generator for Solid Geometry (SAT Advanced).
# =============================================================================

import random

PI = 3.14


def generate(difficulty: str = "easy") -> dict:
    if difficulty == "easy":
        fn = random.choice([_type_volume_prism, _type_volume_cylinder])
    elif difficulty == "medium":
        fn = random.choice([_type_volume_cone, _type_surface_area_prism])
    else:
        fn = random.choice([_type_volume_sphere, _type_scale_volume])
    return fn(difficulty)


# ---------------------------------------------------------------------------

def _type_volume_prism(difficulty: str) -> dict:
    l = random.randint(2, 10)
    w = random.randint(2, 10)
    h = random.randint(2, 10)
    v = l * w * h

    question = (
        f"Find the volume of a rectangular prism with length {l}, "
        f"width {w}, and height {h}."
    )
    explanation = (
        f"V = l × w × h\n"
        f"  = {l} × {w} × {h}\n"
        f"  = {v}"
    )
    return {
        "question":    question,
        "answer":      v,
        "hint":        "Volume of rectangular prism = l × w × h.",
        "hint2":       f"V = {l} × {w} × {h}.",
        "hint3":       f"V = {v}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_volume_cylinder(difficulty: str) -> dict:
    r = random.randint(2, 8)
    h = random.randint(3, 12)
    v = round(PI * r * r * h, 2)

    question = (
        f"Find the volume of a cylinder with radius {r} and height {h}. "
        f"Use π = 3.14 and round to 2 decimal places."
    )
    explanation = (
        f"V = πr²h\n"
        f"  = 3.14 × {r}² × {h}\n"
        f"  = 3.14 × {r*r} × {h}\n"
        f"  = {v}"
    )
    return {
        "question":    question,
        "answer":      v,
        "hint":        "Volume of cylinder = πr²h.",
        "hint2":       f"V = 3.14 × {r}² × {h} = 3.14 × {r*r} × {h}.",
        "hint3":       f"V = {v}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_volume_cone(difficulty: str) -> dict:
    r = random.randint(2, 8)
    h = random.randint(3, 12)
    v = round((1/3) * PI * r * r * h, 2)

    question = (
        f"Find the volume of a cone with radius {r} and height {h}. "
        f"Use π = 3.14 and round to 2 decimal places."
    )
    explanation = (
        f"V = (1/3)πr²h\n"
        f"  = (1/3) × 3.14 × {r}² × {h}\n"
        f"  = (1/3) × 3.14 × {r*r} × {h}\n"
        f"  = (1/3) × {round(PI*r*r*h, 2)}\n"
        f"  = {v}"
    )
    return {
        "question":    question,
        "answer":      v,
        "hint":        "Volume of cone = (1/3)πr²h.",
        "hint2":       f"V = (1/3) × 3.14 × {r*r} × {h}.",
        "hint3":       f"V = {v}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_surface_area_prism(difficulty: str) -> dict:
    l = random.randint(2, 8)
    w = random.randint(2, 8)
    h = random.randint(2, 8)
    sa = 2 * (l*w + l*h + w*h)

    question = (
        f"Find the surface area of a rectangular prism with "
        f"length {l}, width {w}, and height {h}."
    )
    explanation = (
        f"SA = 2(lw + lh + wh)\n"
        f"   = 2({l}×{w} + {l}×{h} + {w}×{h})\n"
        f"   = 2({l*w} + {l*h} + {w*h})\n"
        f"   = 2 × {l*w + l*h + w*h}\n"
        f"   = {sa}"
    )
    return {
        "question":    question,
        "answer":      sa,
        "hint":        "SA = 2(lw + lh + wh).",
        "hint2":       f"= 2({l*w} + {l*h} + {w*h}) = 2 × {l*w+l*h+w*h}.",
        "hint3":       f"SA = {sa}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_volume_sphere(difficulty: str) -> dict:
    r = random.randint(2, 7)
    v = round((4/3) * PI * r**3, 2)

    question = (
        f"Find the volume of a sphere with radius {r}. "
        f"Use π = 3.14 and round to 2 decimal places."
    )
    explanation = (
        f"V = (4/3)πr³\n"
        f"  = (4/3) × 3.14 × {r}³\n"
        f"  = (4/3) × 3.14 × {r**3}\n"
        f"  = (4/3) × {round(PI * r**3, 2)}\n"
        f"  = {v}"
    )
    return {
        "question":    question,
        "answer":      v,
        "hint":        "Volume of sphere = (4/3)πr³.",
        "hint2":       f"V = (4/3) × 3.14 × {r}³ = (4/3) × 3.14 × {r**3}.",
        "hint3":       f"V = {v}.",
        "explanation": explanation,
        "type":        "numeric",
    }


def _type_scale_volume(difficulty: str) -> dict:
    """All dimensions scaled by k — find the new volume."""
    l = random.randint(2, 6)
    w = random.randint(2, 6)
    h = random.randint(2, 6)
    k = random.choice([2, 3])
    v_orig = l * w * h
    v_new  = v_orig * k**3

    question = (
        f"A rectangular prism has dimensions {l} × {w} × {h}. "
        f"All dimensions are multiplied by {k}. "
        f"What is the volume of the new prism?"
    )
    explanation = (
        f"New dimensions: {l*k} × {w*k} × {h*k}\n"
        f"New volume = {l*k} × {w*k} × {h*k}\n"
        f"= {v_new}\n\n"
        f"Alternatively: original volume = {v_orig}, scale factor = {k}\n"
        f"New volume = {v_orig} × {k}³ = {v_orig} × {k**3} = {v_new}"
    )
    return {
        "question":    question,
        "answer":      v_new,
        "hint":        "When all dimensions scale by k, volume scales by k³.",
        "hint2":       f"New volume = {v_orig} × {k}³ = {v_orig} × {k**3}.",
        "hint3":       f"New volume = {v_new}.",
        "explanation": explanation,
        "type":        "numeric",
    }
