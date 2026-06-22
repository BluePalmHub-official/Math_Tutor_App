# =============================================================================
# content/algebra/inequalities.py
# Teaching content for the Inequalities topic.
# =============================================================================

TOPIC_TITLE = "Inequalities"

TOPIC_INTRO = (
    "An inequality is like an equation, but instead of an equals sign "
    "it uses a comparison symbol. Solving an inequality gives you a "
    "range of values rather than a single answer — and one special rule "
    "changes everything when you multiply or divide by a negative number."
)

CONCEPT_CARDS = [
    {
        "title": "What is an Inequality?",
        "body": (
            "An inequality compares two expressions using one of four symbols:\n\n"
            "  >   greater than\n"
            "  <   less than\n"
            "  ≥   greater than or equal to\n"
            "  ≤   less than or equal to\n\n"
            "The solution is not a single number but a set of numbers — "
            "all values of x that make the inequality true."
        ),
        "formula": "ax + b > c    or    ax + b ≤ c",
        "example": "x > 3  means x can be 4, 5, 6, 100 ... any number greater than 3.",
    },
    {
        "title": "Solving Inequalities — Same as Equations (Almost)",
        "body": (
            "You solve inequalities the same way as equations:\n"
            "use inverse operations to isolate the variable.\n\n"
            "Add or subtract the same value from both sides.\n"
            "Multiply or divide both sides by the same positive number.\n\n"
            "The inequality symbol stays the same — UNLESS you multiply "
            "or divide by a negative number (see next card)."
        ),
        "formula": "If  a > b  and  c > 0,  then  a + c > b + c",
        "example": "Solve:  x + 4 > 9\n"
                   "Subtract 4:  x > 5\n"
                   "Solution: all numbers greater than 5.",
    },
    {
        "title": "The Critical Rule — Flipping the Sign",
        "body": (
            "This is the ONE rule that is different from equations:\n\n"
            "When you multiply or divide BOTH sides by a NEGATIVE number, "
            "the inequality symbol FLIPS direction.\n\n"
            "> becomes <\n"
            "< becomes >\n"
            "≥ becomes ≤\n"
            "≤ becomes ≥\n\n"
            "Why? Think about it: 2 < 6, but -2 > -6. "
            "Multiplying by -1 reverses the order."
        ),
        "formula": "If  a > b  and  c < 0,  then  ac < bc",
        "example": "Solve:  -2x < 8\n"
                   "Divide both sides by -2 (FLIP the sign!):\n"
                   "x > -4",
    },
    {
        "title": "Writing and Graphing Solutions",
        "body": (
            "Solutions to inequalities can be written in two ways:\n\n"
            "Inequality notation:  x > 3\n"
            "Interval notation:    (3, ∞)\n\n"
            "On a number line:\n"
            "  Open circle  ○  means the endpoint is NOT included (> or <)\n"
            "  Closed circle ●  means the endpoint IS included (≥ or ≤)\n"
            "  Arrow shows the direction of all valid values."
        ),
        "formula": None,
        "example": "x ≥ 3:\n"
                   "  ●────────►\n"
                   "  3\n\n"
                   "x < 3:\n"
                   "  ◄────────○\n"
                   "           3",
    },
    {
        "title": "Compound Inequalities",
        "body": (
            "A compound inequality combines two inequalities:\n\n"
            "'AND' compound:  a < x < b\n"
            "  x must satisfy BOTH conditions simultaneously.\n"
            "  Example:  2 < x ≤ 7  means x is between 2 and 7.\n\n"
            "Solve each part the same way, keeping the variable in the middle."
        ),
        "formula": "a < x + b < c\n→  a - b < x < c - b",
        "example": "Solve:  1 < x + 3 < 8\n"
                   "Subtract 3 from all parts:\n"
                   "-2 < x < 5",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Solve:   3x - 6 > 9",
        "steps": [
            ("Add 6 to both sides",
             "3x - 6 + 6  >  9 + 6"),
            ("Simplify",
             "3x  >  15"),
            ("Divide both sides by 3 (positive — sign stays)",
             "x  >  5"),
        ],
        "check": "Test x = 6:  3(6) - 6 = 12 > 9  ✓\n"
                 "Test x = 4:  3(4) - 6 = 6 > 9  ✗ (correctly excluded)",
        "notes": "Always test a value inside AND outside the solution to verify.",
    },
    {
        "problem": "Solve:   -2x + 4 ≤ 10",
        "steps": [
            ("Subtract 4 from both sides",
             "-2x + 4 - 4  ≤  10 - 4"),
            ("Simplify",
             "-2x  ≤  6"),
            ("Divide by -2  — FLIP the inequality sign!",
             "x  ≥  -3"),
        ],
        "check": "Test x = 0:  -2(0) + 4 = 4 ≤ 10  ✓\n"
                 "Test x = -4:  -2(-4) + 4 = 12 ≤ 10  ✗ (correctly excluded)",
        "notes": "The flip is the most common place to lose marks. "
                 "Dividing by a negative ALWAYS flips the sign.",
    },
    {
        "problem": "Solve:   2 < 3x - 1 ≤ 11",
        "steps": [
            ("Add 1 to all three parts",
             "2 + 1  <  3x  ≤  11 + 1"),
            ("Simplify",
             "3  <  3x  ≤  12"),
            ("Divide all parts by 3",
             "1  <  x  ≤  4"),
        ],
        "check": "Test x = 2:  2 < 3(2)-1=5 ≤ 11  ✓\n"
                 "Test x = 0:  2 < 3(0)-1=-1  ✗ (correctly excluded)",
        "notes": "For compound inequalities, apply every operation to ALL three parts.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Forgetting to flip the inequality when dividing by a negative",
        "example": "-3x > 9  →  x > -3  (WRONG — should be x < -3)",
        "fix":     "Every time you divide or multiply by a negative number, flip the sign.",
    },
    {
        "mistake": "Flipping the sign when dividing by a positive number",
        "example": "3x > 9  →  x < 3  (WRONG — sign should stay as >)",
        "fix":     "Only flip when the number you divide/multiply by is NEGATIVE.",
    },
    {
        "mistake": "Using the wrong circle type on a number line",
        "example": "x ≥ 3 drawn with an open circle at 3",
        "fix":     "≥ and ≤ use closed circles ●. > and < use open circles ○.",
    },
    {
        "mistake": "Not applying operations to ALL parts of a compound inequality",
        "example": "2 < x + 1 < 8  →  1 < x < 8  (forgot to subtract 1 from 8)",
        "fix":     "Whatever you do to one part, do to ALL three parts.",
    },
]

KEY_VOCABULARY = {
    "Inequality":       "A mathematical statement comparing two expressions using <, >, ≤, or ≥.",
    "Solution Set":     "All values of the variable that make the inequality true.",
    "Greater Than":     "The symbol > means the left side is larger. Example: 5 > 3.",
    "Less Than":        "The symbol < means the left side is smaller. Example: 2 < 7.",
    "At Least":         "Means ≥ (greater than or equal to). 'x is at least 5' means x ≥ 5.",
    "At Most":          "Means ≤ (less than or equal to). 'x is at most 10' means x ≤ 10.",
    "Flip the Sign":    "Reversing the inequality direction when multiplying/dividing by a negative.",
    "Compound Inequality": "Two inequalities joined by AND or OR. Example: 2 < x ≤ 7.",
    "Open Circle":      "Used on a number line for > or < (endpoint not included).",
    "Closed Circle":    "Used on a number line for ≥ or ≤ (endpoint included).",
}