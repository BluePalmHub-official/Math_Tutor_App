# =============================================================================
# content/advanced/linear_functions.py
# All teaching content for the Linear Functions topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Linear Functions"

TOPIC_INTRO = (
    "Linear functions are the backbone of the SAT Math section. "
    "Every question about slope, rate of change, intercepts, or "
    "lines on a graph traces back to these same foundational ideas. "
    "Master these and you gain a fast, reliable toolkit for a large "
    "chunk of the exam."
)

CONCEPT_CARDS = [
    {
        "title": "Slope — Rise Over Run",
        "body": (
            "Slope measures how steeply a line rises or falls. "
            "It is always calculated the same way:\n\n"
            "    slope = rise ÷ run = (change in y) ÷ (change in x)\n\n"
            "Given two points (x₁, y₁) and (x₂, y₂):\n"
            "    m = (y₂ − y₁) ÷ (x₂ − x₁)\n\n"
            "Positive slope → line goes up left to right.\n"
            "Negative slope → line goes down left to right.\n"
            "Zero slope → horizontal line.\n"
            "Undefined slope → vertical line."
        ),
        "formula": "m = (y₂ − y₁) / (x₂ − x₁)",
        "example": "Points (1, 2) and (4, 8):\n"
                   "m = (8 − 2) / (4 − 1) = 6 / 3 = 2",
    },
    {
        "title": "Slope-Intercept Form:  y = mx + b",
        "body": (
            "This is the most useful form of a line equation on the SAT.\n\n"
            "    m = slope (how steep the line is)\n"
            "    b = y-intercept (where the line crosses the y-axis)\n\n"
            "To read a line equation instantly:\n"
            "  • The coefficient of x is the slope.\n"
            "  • The constant term is the y-intercept.\n\n"
            "Example:  y = 3x − 5\n"
            "  slope = 3,   y-intercept = −5\n\n"
            "If an equation is NOT in this form (e.g., 2x + 3y = 12), "
            "rearrange it by solving for y before reading m and b."
        ),
        "formula": "y = mx + b",
        "example": "Rearrange:  2x + 3y = 12\n"
                   "Subtract 2x:  3y = −2x + 12\n"
                   "Divide by 3:  y = −(2/3)x + 4\n"
                   "Slope = −2/3,  y-intercept = 4",
    },
    {
        "title": "Finding the Equation from Two Points",
        "body": (
            "Given two points, you can always write the equation of the line.\n\n"
            "Step 1 — Calculate the slope:\n"
            "    m = (y₂ − y₁) / (x₂ − x₁)\n\n"
            "Step 2 — Substitute m and one point (x₁, y₁) into y = mx + b:\n"
            "    y₁ = m · x₁ + b\n\n"
            "Step 3 — Solve for b.\n\n"
            "Step 4 — Write the equation:  y = mx + b"
        ),
        "formula": None,
        "example": "Points (2, 5) and (6, 13):\n"
                   "m = (13−5)/(6−2) = 8/4 = 2\n"
                   "Use (2, 5):  5 = 2(2) + b  →  b = 1\n"
                   "Equation:  y = 2x + 1",
    },
    {
        "title": "X-intercepts and Y-intercepts",
        "body": (
            "The y-intercept is where the line crosses the y-axis.\n"
            "  At the y-intercept, x = 0.\n"
            "  Substitute x = 0 into the equation and solve for y.\n\n"
            "The x-intercept is where the line crosses the x-axis.\n"
            "  At the x-intercept, y = 0.\n"
            "  Substitute y = 0 into the equation and solve for x.\n\n"
            "SAT tip: many questions describe a line's intercepts as a "
            "way to test whether you know which variable equals zero at "
            "each crossing point."
        ),
        "formula": "y-intercept: set x = 0\nx-intercept: set y = 0",
        "example": "Line:  y = 3x − 6\n"
                   "y-intercept: x=0  →  y = −6  →  (0, −6)\n"
                   "x-intercept: y=0  →  0 = 3x−6  →  x = 2  →  (2, 0)",
    },
    {
        "title": "Parallel and Perpendicular Lines",
        "body": (
            "Parallel lines have the SAME slope and never intersect.\n\n"
            "Perpendicular lines cross at a 90° angle. Their slopes are "
            "negative reciprocals of each other.\n\n"
            "If slope = m, the perpendicular slope = −1/m.\n\n"
            "To find the perpendicular slope:\n"
            "  1. Flip the fraction (reciprocal).\n"
            "  2. Change the sign.\n\n"
            "SAT questions often ask you to write the equation of a line "
            "parallel or perpendicular to a given line through a given point."
        ),
        "formula": "Parallel: same m\nPerpendicular: m₂ = −1/m₁",
        "example": "Line y = 2x + 3  (slope = 2)\n"
                   "Parallel slope: 2\n"
                   "Perpendicular slope: −1/2",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Find the slope and y-intercept of the line 4x − 2y = 10.",
        "steps": [
            ("The equation is not in y = mx + b form — rearrange it",
             "Start with:  4x − 2y = 10"),
            ("Subtract 4x from both sides",
             "−2y = −4x + 10"),
            ("Divide every term by −2",
             "y = 2x − 5"),
            ("Read off slope and y-intercept",
             "slope m = 2,   y-intercept b = −5"),
        ],
        "check": "Plug in (0, −5): 4(0) − 2(−5) = 10  ✓",
        "notes": "Always rearrange to y = mx + b before trying to read slope and intercept.",
    },
    {
        "problem": "Write the equation of the line through (1, 3) and (4, 9).",
        "steps": [
            ("Calculate the slope using the two points",
             "m = (9 − 3) / (4 − 1) = 6 / 3 = 2"),
            ("Substitute m = 2 and point (1, 3) into y = mx + b",
             "3 = 2(1) + b"),
            ("Solve for b",
             "b = 3 − 2 = 1"),
            ("Write the final equation",
             "y = 2x + 1"),
        ],
        "check": "Check (4, 9):  y = 2(4) + 1 = 9  ✓",
        "notes": "Either point works for substituting in Step 2 — you get the same b either way.",
    },
    {
        "problem": "Find the slope of a line perpendicular to y = −(3/4)x + 7.",
        "steps": [
            ("Identify the slope of the given line",
             "m = −3/4"),
            ("The perpendicular slope is the negative reciprocal",
             "Flip: 4/3,  then change sign: +4/3"),
            ("Perpendicular slope",
             "m_perp = 4/3"),
        ],
        "check": "Check: (−3/4) × (4/3) = −12/12 = −1  ✓ (perpendicular slopes multiply to −1)",
        "notes": "Two slopes are perpendicular if and only if their product equals −1.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Swapping Δy and Δx in the slope formula",
        "example": "Points (1,2) and (4,8): writing (4−1)/(8−2) = 3/6 = 0.5 instead of 2",
        "fix":     "Always put y-values on top (numerator) and x-values on bottom (denominator).",
    },
    {
        "mistake": "Setting the wrong variable to zero for intercepts",
        "example": "Finding the x-intercept of y = 3x − 6 by setting x = 0 (gets y-intercept instead)",
        "fix":     "x-intercept → set y = 0.   y-intercept → set x = 0.",
    },
    {
        "mistake": "Forgetting to change the sign when finding perpendicular slope",
        "example": "Given slope 2, writing perpendicular slope as 1/2 instead of −1/2",
        "fix":     "Perpendicular = negative reciprocal. Both flip AND sign change are required.",
    },
    {
        "mistake": "Not rearranging to y = mx + b before reading slope",
        "example": "Reading 2x + 3y = 12 as slope = 2 (it is actually −2/3 after rearranging)",
        "fix":     "Solve for y first. Only then read the coefficient of x as the slope.",
    },
]

KEY_VOCABULARY = {
    "Slope":
        "A number that describes the steepness and direction of a line. m = rise/run.",
    "Y-intercept":
        "The point where a line crosses the y-axis; found by setting x = 0.",
    "X-intercept":
        "The point where a line crosses the x-axis; found by setting y = 0.",
    "Slope-Intercept Form":
        "y = mx + b, where m is the slope and b is the y-intercept.",
    "Linear Function":
        "A function whose graph is a straight line, with no exponents on the variable.",
    "Parallel Lines":
        "Lines with equal slopes that never intersect.",
    "Perpendicular Lines":
        "Lines that meet at 90°; their slopes are negative reciprocals (m₁ × m₂ = −1).",
    "Negative Reciprocal":
        "Flip the fraction and change the sign. The perpendicular slope of 2/3 is −3/2.",
    "Rate of Change":
        "Another name for slope; describes how much y changes for every 1 unit increase in x.",
    "Point-Slope Form":
        "y − y₁ = m(x − x₁); useful for writing an equation when you know slope and one point.",
}
