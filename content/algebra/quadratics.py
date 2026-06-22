# =============================================================================
# content/algebra/quadratics.py
# Teaching content for the Quadratics topic.
# =============================================================================

TOPIC_TITLE = "Quadratics"

TOPIC_INTRO = (
    "A quadratic equation contains a variable raised to the power of 2 (x²). "
    "Unlike linear equations which have one solution, quadratics can have "
    "two solutions, one solution, or no real solutions. "
    "You will learn three methods to solve them."
)

CONCEPT_CARDS = [
    {
        "title": "What is a Quadratic Equation?",
        "body": (
            "A quadratic equation has the standard form:\n\n"
            "    ax² + bx + c = 0\n\n"
            "where a ≠ 0. The highest power of x is 2.\n\n"
            "Every quadratic equation can have:\n"
            "  • Two distinct solutions (most common)\n"
            "  • One repeated solution (special case)\n"
            "  • No real solutions (negative discriminant)"
        ),
        "formula": "ax² + bx + c = 0",
        "example": "x² - 5x + 6 = 0  is a quadratic  (a=1, b=-5, c=6)\n"
                   "x² + 4 = 0       has no real solutions",
    },
    {
        "title": "Method 1 — Factoring",
        "body": (
            "Factoring works when you can find two numbers that:\n"
            "  • Multiply to give c  (the constant)\n"
            "  • Add to give b  (the coefficient of x)\n\n"
            "Write the quadratic as a product of two brackets:\n"
            "    (x + p)(x + q) = 0\n\n"
            "Then use the Zero Product Rule:\n"
            "If two things multiply to give zero, at least one must be zero.\n"
            "So  x + p = 0  OR  x + q = 0."
        ),
        "formula": "x² + bx + c = (x + p)(x + q)\nwhere p × q = c  and  p + q = b",
        "example": "x² - 5x + 6 = 0\n"
                   "Need two numbers: multiply to 6, add to -5\n"
                   "Answer: -2 and -3  (since -2 × -3 = 6, -2 + -3 = -5)\n"
                   "(x - 2)(x - 3) = 0\n"
                   "x = 2  or  x = 3",
    },
    {
        "title": "Method 2 — The Quadratic Formula",
        "body": (
            "When factoring is difficult or impossible, use the quadratic formula.\n"
            "It works for ANY quadratic equation.\n\n"
            "Given  ax² + bx + c = 0:\n\n"
            "Identify a, b, and c from the equation.\n"
            "Substitute into the formula.\n"
            "Calculate carefully — especially the discriminant (b² - 4ac)."
        ),
        "formula": "x = (-b ± √(b² - 4ac)) / (2a)",
        "example": "x² - 5x + 6 = 0  →  a=1, b=-5, c=6\n"
                   "x = (5 ± √(25 - 24)) / 2\n"
                   "x = (5 ± 1) / 2\n"
                   "x = 3  or  x = 2",
    },
    {
        "title": "The Discriminant — How Many Solutions?",
        "body": (
            "The discriminant D = b² - 4ac tells you how many solutions exist\n"
            "before you do any further calculation:\n\n"
            "D > 0  →  Two distinct real solutions\n"
            "D = 0  →  One repeated solution (x = -b/2a)\n"
            "D < 0  →  No real solutions\n\n"
            "Always calculate the discriminant first as a quick check."
        ),
        "formula": "D = b² - 4ac",
        "example": "x² - 4x + 4 = 0:  D = 16 - 16 = 0  (one solution)\n"
                   "x² + x + 1 = 0:   D = 1 - 4 = -3   (no real solutions)\n"
                   "x² - 5x + 6 = 0:  D = 25 - 24 = 1  (two solutions)",
    },
    {
        "title": "Method 3 — Completing the Square",
        "body": (
            "Completing the square rewrites the quadratic in the form:\n"
            "    (x + h)² = k\n\n"
            "Steps:\n"
            "1. Move the constant to the right side\n"
            "2. Add (b/2)² to both sides\n"
            "3. Factor the left as a perfect square\n"
            "4. Take the square root of both sides (± both sides)\n"
            "5. Solve for x\n\n"
            "This method always works and is especially useful "
            "when the quadratic formula gives messy numbers."
        ),
        "formula": "x² + bx  →  (x + b/2)² - (b/2)²",
        "example": "x² - 6x + 5 = 0\n"
                   "x² - 6x = -5\n"
                   "x² - 6x + 9 = -5 + 9  (add (6/2)² = 9)\n"
                   "(x - 3)² = 4\n"
                   "x - 3 = ±2\n"
                   "x = 5  or  x = 1",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Solve by factoring:   x² - 7x + 12 = 0",
        "steps": [
            ("Find two numbers: multiply to 12, add to -7",
             "Factors of 12: (1,12), (2,6), (3,4)\nNeed: multiply=12, add=-7\nAnswer: -3 and -4"),
            ("Write as factored form",
             "(x - 3)(x - 4) = 0"),
            ("Apply Zero Product Rule",
             "x - 3 = 0   OR   x - 4 = 0"),
            ("Solve each",
             "x = 3   OR   x = 4"),
        ],
        "check": "x=3: 9 - 21 + 12 = 0 ✓   x=4: 16 - 28 + 12 = 0 ✓",
        "notes": "Always verify BOTH solutions by substituting back.",
    },
    {
        "problem": "Solve using the quadratic formula:   2x² + 3x - 2 = 0",
        "steps": [
            ("Identify a, b, c",
             "a = 2,   b = 3,   c = -2"),
            ("Calculate the discriminant",
             "D = b² - 4ac = 9 - 4(2)(-2) = 9 + 16 = 25"),
            ("Apply the formula",
             "x = (-3 ± √25) / (2 × 2) = (-3 ± 5) / 4"),
            ("Find both solutions",
             "x = (-3 + 5)/4 = 2/4 = 0.5\nx = (-3 - 5)/4 = -8/4 = -2"),
        ],
        "check": "x=0.5: 2(0.25)+3(0.5)-2=0.5+1.5-2=0 ✓\nx=-2: 2(4)+3(-2)-2=8-6-2=0 ✓",
        "notes": "The ± gives you both solutions. Work each branch separately.",
    },
    {
        "problem": "Solve by completing the square:   x² + 4x - 5 = 0",
        "steps": [
            ("Move constant to right",
             "x² + 4x = 5"),
            ("Add (4/2)² = 4 to both sides",
             "x² + 4x + 4 = 5 + 4 = 9"),
            ("Factor the perfect square",
             "(x + 2)² = 9"),
            ("Take square root of both sides",
             "x + 2 = ±3"),
            ("Solve both cases",
             "x = 1   or   x = -5"),
        ],
        "check": "x=1: 1+4-5=0 ✓   x=-5: 25-20-5=0 ✓",
        "notes": "Add (b/2)² to BOTH sides to keep the equation balanced.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Forgetting the ± in the quadratic formula",
        "example": "Writing x = (-b + √D) / 2a and missing the second solution",
        "fix":     "The ± always gives two branches. Work both: one with + and one with -.",
    },
    {
        "mistake": "Sign errors when identifying b and c",
        "example": "For x² - 5x + 6, writing b = 5 instead of b = -5",
        "fix":     "Write the equation in standard form ax²+bx+c=0, then read off a, b, c with signs.",
    },
    {
        "mistake": "Only finding one solution when factoring",
        "example": "(x-2)(x-3)=0 → only writing x=2",
        "fix":     "Set EACH factor to zero separately. There are two equations, giving two solutions.",
    },
    {
        "mistake": "Adding (b/2)² to only one side when completing the square",
        "example": "x²+6x+9=5 instead of x²+6x+9=5+9",
        "fix":     "Whatever you add to the left, add the same to the right.",
    },
]

KEY_VOCABULARY = {
    "Quadratic Equation": "An equation where the highest power of x is 2. Standard form: ax²+bx+c=0.",
    "Coefficient":        "The number in front of a variable. In 3x², the coefficient is 3.",
    "Factoring":          "Rewriting an expression as a product of simpler expressions.",
    "Zero Product Rule":  "If A×B=0, then A=0 or B=0 (or both).",
    "Discriminant":       "b²-4ac. Tells you how many real solutions a quadratic has.",
    "Quadratic Formula":  "x = (-b ± √(b²-4ac)) / (2a). Works for any quadratic.",
    "Completing the Square": "Rewriting x²+bx as (x+b/2)² minus a constant.",
    "Perfect Square":     "An expression like (x+3)² that comes from squaring a binomial.",
    "Roots / Solutions":  "The values of x that satisfy the equation (make it equal zero).",
    "Vertex":             "The turning point of a parabola, at x = -b/(2a).",
}