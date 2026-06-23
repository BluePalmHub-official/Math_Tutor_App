# =============================================================================
# content/advanced/circle_equations.py
# All teaching content for the Circle Equations topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Circle Equations"

TOPIC_INTRO = (
    "The SAT includes questions about circles placed in the coordinate plane. "
    "You need to find the center and radius directly from a circle equation, "
    "write equations given geometric information, and sometimes complete the "
    "square to convert a general-form equation into standard form."
)

CONCEPT_CARDS = [
    {
        "title": "Standard Equation of a Circle",
        "body": (
            "A circle in the coordinate plane is defined by its center (h, k) "
            "and its radius r. Every point on the circle is exactly r units from "
            "the center. This gives the standard equation:\n\n"
            "    (x − h)² + (y − k)² = r²\n\n"
            "Where:\n"
            "  (h, k) = center of the circle\n"
            "  r      = radius\n"
            "  r²     = the number on the right side\n\n"
            "Note: the equation uses r² on the right side, NOT r. "
            "You must take the square root to find the actual radius."
        ),
        "formula": "(x − h)² + (y − k)² = r²",
        "example": "(x − 3)² + (y + 1)² = 25\n"
                   "Center: (3, −1),  r² = 25,  radius = 5",
    },
    {
        "title": "Reading Center and Radius from the Equation",
        "body": (
            "Given  (x − h)² + (y − k)² = r², read off:\n\n"
            "  Center = (h, k)\n"
            "  Radius = √(r²)\n\n"
            "SIGN TRAP: the equation subtracts h and k. This means:\n"
            "  (x − 3)²  → h = +3   (center x is +3)\n"
            "  (x + 3)²  → h = −3   (because x − (−3) = x + 3)\n"
            "  (y − 5)²  → k = +5\n"
            "  (y + 5)²  → k = −5\n\n"
            "Always flip the sign of what appears in the bracket to get the "
            "center coordinates."
        ),
        "formula": "(x − h)² + (y − k)² = r²  →  center (h,k), radius √r²",
        "example": "(x + 2)² + (y − 6)² = 49\n"
                   "h = −2 (flip sign from +2),  k = 6\n"
                   "Center: (−2, 6),  radius = √49 = 7",
    },
    {
        "title": "Writing Equations from Given Information",
        "body": (
            "To write a circle equation, you need the center and the radius.\n\n"
            "Step 1 — Identify (h, k) and r.\n"
            "Step 2 — Substitute into  (x − h)² + (y − k)² = r².\n"
            "Step 3 — Square the radius.\n\n"
            "Common SAT setup: given center and a point on the circle.\n"
            "  → Use the distance formula to find r:\n"
            "       r = √[(x₂−x₁)² + (y₂−y₁)²]"
        ),
        "formula": "r = √[(x₂−x₁)² + (y₂−y₁)²]",
        "example": "Center (2, −3), radius 4:\n"
                   "(x−2)² + (y+3)² = 16",
    },
    {
        "title": "Completing the Square to Find Standard Form",
        "body": (
            "Some SAT questions give a circle equation in general form:\n"
            "    x² + y² + Dx + Ey + F = 0\n\n"
            "To convert to standard form:\n"
            "Step 1 — Group x-terms and y-terms, move F to the right.\n"
            "Step 2 — Complete the square for x: add (D/2)² to both sides.\n"
            "Step 3 — Complete the square for y: add (E/2)² to both sides.\n"
            "Step 4 — Factor each group as a perfect square.\n"
            "Step 5 — Read off center and radius."
        ),
        "formula": "x² + Dx + (D/2)²  =  (x + D/2)²",
        "example": "x² + y² − 6x + 4y − 3 = 0\n"
                   "Group: (x²−6x) + (y²+4y) = 3\n"
                   "Complete: (x−3)²−9 + (y+2)²−4 = 3\n"
                   "(x−3)² + (y+2)² = 16  →  center (3,−2), r=4",
    },
    {
        "title": "Area and Circumference from the Equation",
        "body": (
            "Once you have the radius from the circle equation, "
            "you can calculate area and circumference:\n\n"
            "    Area         =  π r²\n"
            "    Circumference =  2 π r\n\n"
            "On the SAT, π ≈ 3.14159. The exam usually keeps answers in "
            "terms of π (e.g., '16π') rather than as decimals.\n\n"
            "Quick workflow:\n"
            "  1. Extract r² from the equation.\n"
            "  2. Area = π × r²   (use r² directly — no need to take √ first)\n"
            "  3. For circumference, first find r = √(r²)"
        ),
        "formula": "Area = πr²   Circumference = 2πr",
        "example": "(x−1)² + (y+3)² = 36\n"
                   "r² = 36,  r = 6\n"
                   "Area = 36π ≈ 113.1\n"
                   "Circumference = 12π ≈ 37.7",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Find the center and radius of (x + 5)² + (y − 2)² = 81.",
        "steps": [
            ("Compare with standard form (x − h)² + (y − k)² = r²",
             "(x + 5)² means (x − (−5))²,  so h = −5\n"
             "(y − 2)² means k = 2"),
            ("Read r²",
             "r² = 81"),
            ("Calculate radius",
             "r = √81 = 9"),
            ("State the answer",
             "Center: (−5, 2),  Radius: 9"),
        ],
        "check": "Distance from (−5,2) to point (4,2) = 9.  (4−(−5))²+(2−2)² = 81  ✓",
        "notes": "The sign of h is OPPOSITE to the sign shown in the equation.",
    },
    {
        "problem": "Write the equation of a circle with center (−1, 4) and radius 6.",
        "steps": [
            ("Standard form: (x − h)² + (y − k)² = r²",
             "h = −1,  k = 4,  r = 6"),
            ("Substitute h and k",
             "(x − (−1))² + (y − 4)² = 6²"),
            ("Simplify",
             "(x + 1)² + (y − 4)² = 36"),
        ],
        "check": "Check center: −1 from (x+1)² ✓  and  4 from (y−4)² ✓  r²=36 ✓",
        "notes": None,
    },
    {
        "problem": "Convert to standard form and find the center and radius:\n"
                   "x² + y² − 4x + 6y − 12 = 0",
        "steps": [
            ("Group and move constant to right side",
             "(x² − 4x) + (y² + 6y) = 12"),
            ("Complete the square for x:  (−4/2)² = 4",
             "(x² − 4x + 4) + (y² + 6y) = 12 + 4"),
            ("Complete the square for y:  (6/2)² = 9",
             "(x² − 4x + 4) + (y² + 6y + 9) = 12 + 4 + 9"),
            ("Factor each group",
             "(x − 2)² + (y + 3)² = 25"),
            ("Read off center and radius",
             "Center: (2, −3),  r = √25 = 5"),
        ],
        "check": "Expand (x−2)²+(y+3)²−25: x²−4x+4+y²+6y+9−25 = x²+y²−4x+6y−12  ✓",
        "notes": "Whatever you add to complete the square must also be added to the right side.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Sign error when reading the center",
        "example": "(x − 3)² gives h = −3 instead of h = 3",
        "fix":     "The center is (h, k) where the equation is (x − h)². The sign flips from what's written.",
    },
    {
        "mistake": "Reporting r² instead of r as the radius",
        "example": "(x−1)² + (y−2)² = 49 → radius = 49 instead of 7",
        "fix":     "Always take the square root of the right-hand side to get the radius.",
    },
    {
        "mistake": "Forgetting to add the completing-the-square value to the right side",
        "example": "(x²−4x+4) + y² = 12 (forgot to add 4 to the right side)",
        "fix":     "Adding a number to the left side requires adding the same number to the right side.",
    },
    {
        "mistake": "Confusing standard form of a circle with standard form of a parabola",
        "example": "Writing x² + y² = r as the circle equation",
        "fix":     "Circle: (x−h)² + (y−k)² = r².  Both x and y are squared and added.",
    },
]

KEY_VOCABULARY = {
    "Standard Form (Circle)":
        "(x − h)² + (y − k)² = r²; shows center and radius directly.",
    "Center":
        "The fixed interior point (h, k) equidistant from all points on the circle.",
    "Radius":
        "The distance from the center to any point on the circle; r = √(r²).",
    "General Form":
        "x² + y² + Dx + Ey + F = 0; must complete the square to find center and radius.",
    "Completing the Square":
        "Adding (b/2)² to form a perfect square trinomial: x² + bx + (b/2)² = (x + b/2)².",
    "Distance Formula":
        "d = √[(x₂−x₁)² + (y₂−y₁)²]; used to find radius from center and a point on the circle.",
    "Diameter":
        "A chord passing through the center; diameter = 2r.",
    "Circumference":
        "The perimeter of a circle; C = 2πr.",
    "Area (Circle)":
        "A = πr².",
    "r²":
        "The constant on the right side of the standard circle equation; take √ to get radius.",
}
