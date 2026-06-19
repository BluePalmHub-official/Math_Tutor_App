# =============================================================================
# content/algebra/linear_equations.py
# All teaching content for the Linear Equations topic.
#
# This file contains ONLY knowledge — no GUI, no logic.
# learn_screen.py reads this and renders it into cards and worked examples.
#
# Structure:
#   TOPIC_TITLE        str
#   TOPIC_INTRO        str   — one paragraph overview shown before cards
#   CONCEPT_CARDS      list  — each card is one focused idea
#   WORKED_EXAMPLES    list  — step-by-step solved problems
#   COMMON_MISTAKES    list  — what to watch out for
#   KEY_VOCABULARY     dict  — glossary terms
# =============================================================================

TOPIC_TITLE = "Linear Equations"

TOPIC_INTRO = (
    "A linear equation is one of the most fundamental tools in algebra. "
    "Once you understand how to solve them, you can use the same logical "
    "steps to tackle much more complex problems. "
    "The core idea is simple: find the value of the unknown variable that "
    "makes the equation true."
)

# -----------------------------------------------------------------------------
# Concept Cards
# Each card is shown one at a time in learn_screen.py.
# The student taps Next to advance — they cannot skip ahead.
#
# Keys:
#   title   : card heading
#   body    : explanation text (keep each paragraph focused on ONE idea)
#   formula : optional — displayed in monospace in a highlighted box
#   example : optional — a quick inline example after the explanation
# -----------------------------------------------------------------------------

CONCEPT_CARDS = [
    {
        "title": "What is a Linear Equation?",
        "body": (
            "A linear equation is an equation where the variable (usually x) "
            "has no exponents — it appears only as x, never as x² or x³.\n\n"
            "The word 'linear' comes from 'line' — when you plot a linear "
            "equation on a graph, it always forms a straight line.\n\n"
            "The goal of solving a linear equation is always the same:\n"
            "get the variable alone on one side of the equals sign."
        ),
        "formula": "ax + b = c",
        "example": "Example:  3x + 5 = 14  is a linear equation.\n"
                   "          3x² + 5 = 14 is NOT — because of the x².",
    },
    {
        "title": "The Balance Rule — The Golden Rule of Algebra",
        "body": (
            "Think of an equation as a balance scale. Both sides are "
            "always equal — that's what the = sign means.\n\n"
            "The Golden Rule:\n"
            "Whatever you do to one side, you MUST do to the other side.\n\n"
            "If you add 5 to the left side, add 5 to the right side.\n"
            "If you divide the left side by 3, divide the right side by 3.\n\n"
            "As long as you follow this rule, the equation stays balanced "
            "and you will always reach the correct answer."
        ),
        "formula": "If  a = b,  then  a + c = b + c",
        "example": "3x + 5 = 14\n"
                   "Subtract 5 from BOTH sides:\n"
                   "3x + 5 - 5 = 14 - 5\n"
                   "3x = 9",
    },
    {
        "title": "Inverse Operations — Your Solving Tools",
        "body": (
            "To isolate the variable, you undo what is being done to it "
            "using the opposite (inverse) operation.\n\n"
            "Addition ↔ Subtraction\n"
            "  If something is added to x, subtract it from both sides.\n\n"
            "Multiplication ↔ Division\n"
            "  If x is multiplied by a number, divide both sides by that number.\n\n"
            "You always work in reverse order of operations:\n"
            "undo addition/subtraction FIRST, then multiplication/division."
        ),
        "formula": None,
        "example": "Solve:  2x - 7 = 3\n"
                   "Step 1 — undo subtraction: add 7 to both sides\n"
                   "         2x = 10\n"
                   "Step 2 — undo multiplication: divide both sides by 2\n"
                   "         x = 5",
    },
    {
        "title": "Collecting Like Terms",
        "body": (
            "Sometimes the variable appears on both sides of the equation, "
            "or there are multiple terms to simplify first.\n\n"
            "Like terms are terms that have the same variable (or are both "
            "plain numbers). You can add or subtract like terms.\n\n"
            "Strategy:\n"
            "1. Move all variable terms to one side.\n"
            "2. Move all number terms to the other side.\n"
            "3. Simplify each side.\n"
            "4. Divide to isolate the variable."
        ),
        "formula": None,
        "example": "Solve:  5x + 3 = 2x + 12\n"
                   "Subtract 2x from both sides:  3x + 3 = 12\n"
                   "Subtract 3 from both sides:   3x = 9\n"
                   "Divide both sides by 3:        x = 3",
    },
    {
        "title": "Always Check Your Answer",
        "body": (
            "After solving, substitute your answer back into the ORIGINAL "
            "equation to verify it is correct.\n\n"
            "If both sides equal the same number after substituting, "
            "your answer is correct.\n\n"
            "This step takes only a few seconds and will catch any "
            "arithmetic mistakes before they become bigger problems."
        ),
        "formula": None,
        "example": "Solution: x = 3  for  3x + 5 = 14\n"
                   "Check: 3(3) + 5 = 9 + 5 = 14  ✓\n"
                   "Both sides equal 14 — the answer is confirmed.",
    },
]

# -----------------------------------------------------------------------------
# Worked Examples
# Each example shows a full step-by-step solution.
# learn_screen.py reveals one step at a time — the student taps to see each.
#
# Keys:
#   problem : the equation to solve (shown upfront)
#   steps   : list of (description, working) tuples
#   check   : the substitution verification line
#   notes   : optional extra insight about this example
# -----------------------------------------------------------------------------

WORKED_EXAMPLES = [
    {
        "problem": "Solve:   3x + 5 = 14",
        "steps": [
            ("Identify what is being done to x",
             "x is multiplied by 3, then 5 is added"),
            ("Undo the addition — subtract 5 from both sides",
             "3x + 5 − 5  =  14 − 5"),
            ("Simplify both sides",
             "3x  =  9"),
            ("Undo the multiplication — divide both sides by 3",
             "3x ÷ 3  =  9 ÷ 3"),
            ("Solution",
             "x  =  3"),
        ],
        "check": "Substitute back:  3(3) + 5  =  9 + 5  =  14  ✓",
        "notes": "This is the most common type — one variable term, one constant on each side.",
    },
    {
        "problem": "Solve:   2x − 7 = 3",
        "steps": [
            ("Undo the subtraction — add 7 to both sides",
             "2x − 7 + 7  =  3 + 7"),
            ("Simplify",
             "2x  =  10"),
            ("Divide both sides by 2",
             "2x ÷ 2  =  10 ÷ 2"),
            ("Solution",
             "x  =  5"),
        ],
        "check": "Substitute back:  2(5) − 7  =  10 − 7  =  3  ✓",
        "notes": None,
    },
    {
        "problem": "Solve:   5x + 3 = 2x + 12",
        "steps": [
            ("Variable appears on both sides — collect variable terms",
             "Subtract 2x from both sides"),
            ("Result after subtracting 2x",
             "3x + 3  =  12"),
            ("Subtract 3 from both sides",
             "3x  =  9"),
            ("Divide both sides by 3",
             "x  =  3"),
        ],
        "check": "Substitute back:  5(3) + 3  =  18   and   2(3) + 12  =  18  ✓",
        "notes": "When the variable is on both sides, always move the smaller "
                 "variable term across first to keep the coefficient positive.",
    },
    {
        "problem": "Solve:   4(x − 2) = 12",
        "steps": [
            ("Expand the bracket first",
             "4x − 8  =  12"),
            ("Add 8 to both sides",
             "4x  =  20"),
            ("Divide both sides by 4",
             "x  =  5"),
        ],
        "check": "Substitute back:  4(5 − 2)  =  4(3)  =  12  ✓",
        "notes": "Always expand brackets before applying inverse operations.",
    },
]

# -----------------------------------------------------------------------------
# Common Mistakes
# Displayed as a warning panel at the end of the Learn phase.
# -----------------------------------------------------------------------------

COMMON_MISTAKES = [
    {
        "mistake": "Applying an operation to only one side",
        "example": "3x + 5 = 14  →  3x = 14  (forgot to subtract 5 from the right)",
        "fix":     "Always ask: 'Did I do this to BOTH sides?'",
    },
    {
        "mistake": "Sign errors when moving terms",
        "example": "2x − 7 = 3  →  2x = 3 − 7 = −4  (should be +7, not −7)",
        "fix":     "Use inverse operations: subtraction becomes addition, and vice versa.",
    },
    {
        "mistake": "Dividing only the variable term, not the whole side",
        "example": "3x + 6 = 15  →  x + 6 = 5  (divided only 3x by 3, not the 6)",
        "fix":     "Collect the variable alone BEFORE dividing: 3x = 9, then x = 3.",
    },
    {
        "mistake": "Forgetting to expand brackets",
        "example": "4(x − 2) = 12  →  4x − 2 = 12  (forgot to multiply −2 by 4)",
        "fix":     "Distribute the number outside to EVERY term inside the brackets.",
    },
    {
        "mistake": "Not checking the answer",
        "example": "Submitting x = 4 without substituting back to verify.",
        "fix":     "Always substitute your answer into the original equation.",
    },
]

# -----------------------------------------------------------------------------
# Key Vocabulary
# Displayed as a glossary panel accessible throughout the Learn phase.
# -----------------------------------------------------------------------------

KEY_VOCABULARY = {
    "Variable":
        "A letter (like x or y) that represents an unknown number we want to find.",
    "Coefficient":
        "The number multiplied by a variable. In 3x, the coefficient is 3.",
    "Constant":
        "A plain number with no variable attached. In 3x + 5, the constant is 5.",
    "Equation":
        "A mathematical statement that two expressions are equal, shown with an = sign.",
    "Inverse Operation":
        "The opposite operation used to undo another. "
        "Addition and subtraction are inverses. Multiplication and division are inverses.",
    "Isolate":
        "To get the variable alone on one side of the equation.",
    "Solution":
        "The value of the variable that makes the equation true.",
    "Substitution":
        "Replacing the variable with a number to check if an equation is true.",
    "Like Terms":
        "Terms that have the same variable (e.g. 3x and 5x) "
        "or are both plain numbers (e.g. 4 and 7). Only like terms can be combined.",
    "Expand":
        "Multiply a number or term outside brackets by everything inside. "
        "4(x − 2) expands to 4x − 8.",
}