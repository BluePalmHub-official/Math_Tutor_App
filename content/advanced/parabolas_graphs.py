# =============================================================================
# content/advanced/parabolas_graphs.py
# All teaching content for the Parabolas & Graphs topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Parabolas & Graphs"

TOPIC_INTRO = (
    "A parabola is the U-shaped graph of a quadratic function. "
    "The SAT tests your ability to move between different forms of a "
    "quadratic, identify key features like the vertex and axis of symmetry, "
    "and find where the parabola crosses the x-axis."
)

CONCEPT_CARDS = [
    {
        "title": "Standard Form:  y = ax² + bx + c",
        "body": (
            "The standard form of a quadratic is:\n"
            "    y = ax² + bx + c\n\n"
            "What each part tells you:\n"
            "  a  determines the direction and width:\n"
            "     • a > 0 → parabola opens UP (minimum point at vertex)\n"
            "     • a < 0 → parabola opens DOWN (maximum point at vertex)\n"
            "     • |a| large → narrow parabola    |a| small → wide parabola\n\n"
            "  c  is the y-intercept (the value of y when x = 0)\n\n"
            "The axis of symmetry and vertex require more calculation — "
            "see the next two cards."
        ),
        "formula": "y = ax² + bx + c",
        "example": "y = 2x² − 4x + 1\n"
                   "a=2 (opens up, narrow), c=1 (y-intercept is 1)",
    },
    {
        "title": "Vertex Form:  y = a(x − h)² + k",
        "body": (
            "Vertex form makes the vertex immediately visible:\n"
            "    y = a(x − h)² + k\n\n"
            "The vertex is at  (h, k).\n\n"
            "IMPORTANT: the sign inside the bracket is subtracted, so:\n"
            "  y = (x − 3)² + 5   →  vertex at (3, 5)\n"
            "  y = (x + 2)² − 1   →  vertex at (−2, −1)   ← sign flips!\n\n"
            "Vertex form also tells you the minimum/maximum value immediately:\n"
            "  If a > 0, the minimum value of y is k.\n"
            "  If a < 0, the maximum value of y is k."
        ),
        "formula": "y = a(x − h)² + k   →   vertex at (h, k)",
        "example": "y = −2(x − 1)² + 8\n"
                   "vertex = (1, 8),  opens down,  maximum value = 8",
    },
    {
        "title": "Axis of Symmetry",
        "body": (
            "Every parabola has a vertical axis of symmetry — a vertical line "
            "that divides it into two mirror-image halves.\n\n"
            "From standard form  y = ax² + bx + c:\n"
            "    x = −b / (2a)\n\n"
            "From vertex form  y = a(x − h)² + k:\n"
            "    x = h\n\n"
            "The axis passes through the vertex. The x-coordinate of the vertex "
            "equals the axis of symmetry."
        ),
        "formula": "Axis of symmetry:  x = −b/(2a)",
        "example": "y = 3x² − 12x + 5\n"
                   "a=3, b=−12\n"
                   "Axis: x = −(−12)/(2×3) = 12/6 = 2",
    },
    {
        "title": "Finding the Vertex",
        "body": (
            "The vertex is the turning point of the parabola — the minimum "
            "if a > 0 and the maximum if a < 0.\n\n"
            "From standard form:\n"
            "  Step 1:  x-coordinate = −b/(2a)\n"
            "  Step 2:  substitute that x back into the equation to find y\n\n"
            "From vertex form:\n"
            "  Read off (h, k) directly.\n\n"
            "SAT shortcut: if a question asks for the minimum or maximum value "
            "of a quadratic, find the y-coordinate of the vertex."
        ),
        "formula": "Vertex x = −b/(2a),  Vertex y = f(−b/(2a))",
        "example": "y = x² − 6x + 2\n"
                   "x = −(−6)/(2·1) = 3\n"
                   "y = 3² − 6(3) + 2 = 9 − 18 + 2 = −7\n"
                   "Vertex: (3, −7)",
    },
    {
        "title": "X-intercepts (Roots / Zeros)",
        "body": (
            "The x-intercepts are where the parabola crosses the x-axis (where y = 0).\n\n"
            "Methods to find x-intercepts:\n\n"
            "  1. Factoring:  set y = 0, factor, solve each bracket.\n\n"
            "  2. Quadratic formula:\n"
            "       x = (−b ± √(b²−4ac)) / (2a)\n\n"
            "  3. Square root (only for vertex form with no linear term):\n"
            "       a(x−h)² = −k  →  solve for x.\n\n"
            "The discriminant b²−4ac tells you how many x-intercepts exist:\n"
            "  > 0  →  two x-intercepts\n"
            "  = 0  →  one x-intercept (vertex touches x-axis)\n"
            "  < 0  →  no real x-intercepts"
        ),
        "formula": "x = (−b ± √(b²−4ac)) / 2a",
        "example": "y = x² − 5x + 6\n"
                   "0 = (x−2)(x−3)  →  x = 2  or  x = 3",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "For y = 2x² − 8x + 3, find the axis of symmetry and vertex.",
        "steps": [
            ("Identify a and b from standard form",
             "a = 2,  b = −8"),
            ("Axis of symmetry formula",
             "x = −b/(2a) = −(−8)/(2×2) = 8/4 = 2"),
            ("Find the vertex y-coordinate — substitute x = 2",
             "y = 2(2)² − 8(2) + 3 = 8 − 16 + 3 = −5"),
            ("Vertex",
             "(2, −5)"),
        ],
        "check": "Check: 2(2)² − 8(2) + 3 = 8 − 16 + 3 = −5  ✓",
        "notes": "The axis of symmetry is always the x-coordinate of the vertex.",
    },
    {
        "problem": "Write y = x² − 4x + 7 in vertex form.",
        "steps": [
            ("Complete the square — take half the x coefficient and square it",
             "Half of −4 is −2;  (−2)² = 4"),
            ("Add and subtract 4 inside the expression",
             "y = (x² − 4x + 4) + 7 − 4"),
            ("Factor the perfect square trinomial",
             "y = (x − 2)² + 3"),
            ("Read off the vertex",
             "h = 2, k = 3  →  vertex is (2, 3)"),
        ],
        "check": "Expand (x−2)²+3 = x²−4x+4+3 = x²−4x+7  ✓",
        "notes": "Completing the square converts standard form to vertex form.",
    },
    {
        "problem": "Find the x-intercepts of y = x² − 7x + 10.",
        "steps": [
            ("Set y = 0",
             "0 = x² − 7x + 10"),
            ("Factor: find two numbers that multiply to 10 and add to −7",
             "−2 × −5 = 10  and  −2 + (−5) = −7"),
            ("Write in factored form",
             "0 = (x − 2)(x − 5)"),
            ("Set each factor equal to zero",
             "x − 2 = 0  →  x = 2\n"
             "x − 5 = 0  →  x = 5"),
        ],
        "check": "Check x=2:  4 − 14 + 10 = 0  ✓   Check x=5:  25 − 35 + 10 = 0  ✓",
        "notes": None,
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Getting the vertex wrong from vertex form due to sign error",
        "example": "y = (x + 3)² − 1 → vertex (3, −1) instead of (−3, −1)",
        "fix":     "y = (x − h)² + k.  In (x + 3), h = −3 because x − (−3) = x + 3.",
    },
    {
        "mistake": "Forgetting to substitute x back to find the vertex y-coordinate",
        "example": "Saying vertex is (2, ?) after finding x = 2 but not computing y",
        "fix":     "Substitute x = −b/(2a) into the original equation to find the y-coordinate.",
    },
    {
        "mistake": "Confusing minimum value with the x-coordinate of the vertex",
        "example": "Vertex at (3, −7); answering minimum value = 3 instead of −7",
        "fix":     "The minimum (or maximum) value is the y-coordinate of the vertex.",
    },
    {
        "mistake": "Using the discriminant formula wrong (forgetting the −4ac part)",
        "example": "Writing discriminant = b² instead of b² − 4ac",
        "fix":     "Discriminant = b² − 4ac.  All three terms (b², 4, a, c) are needed.",
    },
]

KEY_VOCABULARY = {
    "Parabola":
        "The U-shaped (or ∩-shaped) graph of a quadratic function.",
    "Vertex":
        "The turning point of a parabola; the minimum if a>0, maximum if a<0.",
    "Axis of Symmetry":
        "The vertical line x = −b/(2a) that divides the parabola into two mirror halves.",
    "Standard Form":
        "y = ax² + bx + c; a ≠ 0.",
    "Vertex Form":
        "y = a(x − h)² + k; vertex is immediately visible as (h, k).",
    "X-intercepts":
        "Points where the parabola crosses the x-axis (where y = 0); also called roots or zeros.",
    "Y-intercept":
        "The point where the parabola crosses the y-axis; equal to c in standard form.",
    "Discriminant":
        "b² − 4ac; determines the number of real x-intercepts.",
    "Completing the Square":
        "An algebraic method to rewrite a quadratic in vertex form.",
    "Minimum/Maximum":
        "The smallest (a>0) or largest (a<0) value of y; equal to the vertex y-coordinate k.",
}
