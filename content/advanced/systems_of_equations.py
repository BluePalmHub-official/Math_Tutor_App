# =============================================================================
# content/advanced/systems_of_equations.py
# All teaching content for the Systems of Equations topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Systems of Equations"

TOPIC_INTRO = (
    "A system of equations is simply two (or more) equations that must be "
    "true at the same time. The solution is the one point (x, y) that "
    "satisfies every equation in the system. The SAT tests systems frequently "
    "— both with algebra and through word problems."
)

CONCEPT_CARDS = [
    {
        "title": "What is a System of Equations?",
        "body": (
            "A system is a set of two equations with two unknowns (usually x and y). "
            "The solution is the ordered pair (x, y) that makes BOTH equations true "
            "simultaneously.\n\n"
            "Graphically, the solution is the point where the two lines intersect.\n\n"
            "There are three possible outcomes:\n"
            "  1. One solution — the lines cross at exactly one point.\n"
            "  2. No solution — the lines are parallel (same slope, different intercepts).\n"
            "  3. Infinite solutions — the lines are identical (same slope and intercept)."
        ),
        "formula": None,
        "example": "System:  y = 2x + 1  and  y = x + 3\n"
                   "Solution: set equal  2x + 1 = x + 3\n"
                   "          x = 2,  y = 5   →   (2, 5)",
    },
    {
        "title": "Substitution Method",
        "body": (
            "Use substitution when one equation already has a variable isolated "
            "(or is easy to isolate).\n\n"
            "Steps:\n"
            "1. Isolate one variable in one equation.\n"
            "2. Substitute that expression into the other equation.\n"
            "3. Solve the resulting single-variable equation.\n"
            "4. Substitute back to find the other variable.\n"
            "5. Check both answers in both original equations."
        ),
        "formula": None,
        "example": "y = 3x − 1  …(1)\n"
                   "2x + y = 9  …(2)\n"
                   "Sub (1) into (2):  2x + (3x−1) = 9\n"
                   "5x − 1 = 9  →  x = 2\n"
                   "y = 3(2)−1 = 5   →  (2, 5)",
    },
    {
        "title": "Elimination Method",
        "body": (
            "Use elimination when neither variable is isolated, especially "
            "when coefficients line up nicely.\n\n"
            "Steps:\n"
            "1. Align the equations so like terms are in the same column.\n"
            "2. Multiply one (or both) equations so that one variable has "
            "   opposite coefficients (+3x and −3x).\n"
            "3. Add the two equations together. One variable cancels.\n"
            "4. Solve for the remaining variable.\n"
            "5. Substitute back to find the other variable."
        ),
        "formula": None,
        "example": "3x + 2y = 12  …(1)\n"
                   "x − 2y = 4   …(2)\n"
                   "Add equations: 4x = 16  →  x = 4\n"
                   "Sub into (2): 4 − 2y = 4  →  y = 0",
    },
    {
        "title": "Number of Solutions",
        "body": (
            "When you work through a system, the algebra will tell you how many "
            "solutions exist.\n\n"
            "Exactly one solution:\n"
            "  You find a specific value for x (and then for y).\n\n"
            "No solution:\n"
            "  The variable terms cancel and you get a false statement like 0 = 5.\n"
            "  This means the lines are parallel and never cross.\n\n"
            "Infinite solutions:\n"
            "  The variable terms cancel and you get a true statement like 0 = 0.\n"
            "  This means the two equations describe the same line.\n\n"
            "On the SAT, identifying 'no solution' vs 'infinite solutions' is "
            "a common question type."
        ),
        "formula": None,
        "example": "3x + y = 6\n"
                   "6x + 2y = 5\n"
                   "Multiply eq 1 by 2: 6x + 2y = 12\n"
                   "Subtract: 0 = −7  →  No solution (parallel lines)",
    },
    {
        "title": "Setting Up Systems from Word Problems",
        "body": (
            "Many SAT word problems are really just systems of equations in disguise.\n\n"
            "Strategy:\n"
            "1. Choose two variables (e.g., x and y) for the two unknowns.\n"
            "2. Write two equations — one for each given relationship or constraint.\n"
            "3. Solve using substitution or elimination.\n"
            "4. Answer the specific question asked (often just one variable).\n\n"
            "Common setups:\n"
            "  • Total count + total cost → two equations\n"
            "  • Speed / distance / time problems\n"
            "  • Mixture problems"
        ),
        "formula": None,
        "example": "Tickets cost $5 (child) and $8 (adult).\n"
                   "48 tickets sold for $294 total.\n"
                   "Let c = child, a = adult:\n"
                   "c + a = 48  and  5c + 8a = 294\n"
                   "Solve: c = 26, a = 22",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Solve the system:  y = 2x − 3   and   3x + y = 12",
        "steps": [
            ("Equation 1 already has y isolated — use substitution",
             "y = 2x − 3"),
            ("Substitute into Equation 2",
             "3x + (2x − 3) = 12"),
            ("Simplify and solve for x",
             "5x − 3 = 12   →   5x = 15   →   x = 3"),
            ("Substitute x = 3 back into y = 2x − 3",
             "y = 2(3) − 3 = 3"),
            ("Solution",
             "(x, y) = (3, 3)"),
        ],
        "check": "Check in Eq 2:  3(3) + 3 = 9 + 3 = 12  ✓",
        "notes": "Always substitute back into the simpler original equation to find the second variable.",
    },
    {
        "problem": "Solve:  2x + 3y = 11   and   4x − 3y = 7",
        "steps": [
            ("The y-coefficients are already opposite (+3y and −3y)",
             "Add the two equations directly"),
            ("Add equations together",
             "6x = 18   →   x = 3"),
            ("Substitute x = 3 into Equation 1",
             "2(3) + 3y = 11   →   6 + 3y = 11"),
            ("Solve for y",
             "3y = 5   →   y = 5/3"),
            ("Solution",
             "(x, y) = (3, 5/3)"),
        ],
        "check": "Check in Eq 2:  4(3) − 3(5/3) = 12 − 5 = 7  ✓",
        "notes": "Elimination is fastest when one variable cancels by simply adding the equations.",
    },
    {
        "problem": "An orchard sells apples for $2 each and pears for $3 each. "
                   "A customer buys 15 pieces of fruit and pays $38. "
                   "How many apples did they buy?",
        "steps": [
            ("Define variables",
             "Let a = apples,  p = pears"),
            ("Write two equations from the problem",
             "a + p = 15   (total count)\n"
             "2a + 3p = 38   (total cost)"),
            ("From Eq 1, isolate a:  a = 15 − p. Substitute into Eq 2",
             "2(15 − p) + 3p = 38"),
            ("Simplify",
             "30 − 2p + 3p = 38   →   p = 8"),
            ("Find a",
             "a = 15 − 8 = 7"),
        ],
        "check": "Check: 7 + 8 = 15  ✓  and  2(7)+3(8) = 14+24 = 38  ✓",
        "notes": "The question asks only for apples — but you still need both equations to solve it.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Forgetting to find both variables",
        "example": "Solving and getting x = 3 but not substituting back to find y",
        "fix":     "A system solution is an ordered pair (x, y). Always find both values.",
    },
    {
        "mistake": "Multiplying only some terms when scaling for elimination",
        "example": "Scaling 2x + 3y = 11 by 2 → writing 4x + 3y = 11 (forgetting to scale 3y and 11)",
        "fix":     "Every term in the equation must be multiplied, including the right-hand side.",
    },
    {
        "mistake": "Not checking the answer in both equations",
        "example": "Checking only in Equation 1 and missing an error in Equation 2",
        "fix":     "Substitute your (x, y) into both original equations to confirm both are satisfied.",
    },
    {
        "mistake": "Misidentifying no-solution vs infinite-solution cases",
        "example": "Getting 0 = 0 and saying 'no solution' when it actually means infinite solutions",
        "fix":     "0 = 0 (true) → infinite solutions.  0 = k (false, k ≠ 0) → no solution.",
    },
]

KEY_VOCABULARY = {
    "System of Equations":
        "Two or more equations that must all be satisfied simultaneously.",
    "Solution":
        "The ordered pair (x, y) that satisfies every equation in the system.",
    "Substitution":
        "Replacing a variable with an equivalent expression from another equation.",
    "Elimination":
        "Adding or subtracting equations to cancel one variable.",
    "Consistent System":
        "A system that has at least one solution.",
    "Inconsistent System":
        "A system with no solution; the graphs are parallel lines.",
    "Dependent System":
        "A system with infinitely many solutions; both equations describe the same line.",
    "Coefficient":
        "The number multiplied by a variable (e.g., in 3x, the coefficient is 3).",
    "Ordered Pair":
        "A pair of numbers (x, y) representing a point in the coordinate plane.",
    "Linear System":
        "A system where every equation is linear (no exponents on variables).",
}
