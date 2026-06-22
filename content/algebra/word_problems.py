# =============================================================================
# content/algebra/word_problems.py
# Teaching content for the Word Problems topic.
# =============================================================================

TOPIC_TITLE = "Word Problems"

TOPIC_INTRO = (
    "Word problems are where algebra meets real life. The skill is not "
    "the calculation — it's translating English sentences into mathematical "
    "equations. Once you have the equation, you already know how to solve it."
)

CONCEPT_CARDS = [
    {
        "title": "The 5-Step Method for Any Word Problem",
        "body": (
            "Follow these five steps every time:\n\n"
            "Step 1 — READ carefully. Read the problem twice.\n\n"
            "Step 2 — IDENTIFY what you need to find. "
            "Give it a variable name (usually x).\n\n"
            "Step 3 — TRANSLATE. Convert each sentence into math.\n\n"
            "Step 4 — SOLVE the equation.\n\n"
            "Step 5 — CHECK. Does the answer make sense "
            "in the context of the problem?"
        ),
        "formula": "Words → Equation → Solve → Check",
        "example": "Problem: A number doubled plus 3 equals 11. Find the number.\n"
                   "Let x = the number\n"
                   "Equation: 2x + 3 = 11\n"
                   "Solve: x = 4\n"
                   "Check: 2(4) + 3 = 11 ✓",
    },
    {
        "title": "Key Words and Their Math Meanings",
        "body": (
            "These words tell you which operation to use:\n\n"
            "ADDITION (+):\n"
            "  sum, total, more than, increased by, added to\n\n"
            "SUBTRACTION (−):\n"
            "  difference, less than, decreased by, fewer, minus\n\n"
            "MULTIPLICATION (×):\n"
            "  product, times, double, triple, of (with fractions/percents)\n\n"
            "DIVISION (÷):\n"
            "  quotient, divided by, split equally, per, ratio\n\n"
            "EQUALS (=):\n"
            "  is, are, was, equals, gives, results in"
        ),
        "formula": None,
        "example": "'5 more than a number' → x + 5\n"
                   "'twice a number less 4' → 2x - 4\n"
                   "'a number divided by 3 is 7' → x/3 = 7",
    },
    {
        "title": "Number Problems",
        "body": (
            "Number problems ask you to find an unknown number "
            "based on relationships described in words.\n\n"
            "Common setups:\n"
            "  Consecutive integers: x, x+1, x+2\n"
            "  Consecutive even/odd: x, x+2, x+4\n"
            "  One number is n times another: one=x, other=nx\n\n"
            "Strategy: Let x be the unknown. Write expressions "
            "for all other quantities in terms of x."
        ),
        "formula": None,
        "example": "The sum of three consecutive integers is 48.\n"
                   "Let x, x+1, x+2 be the integers.\n"
                   "x + (x+1) + (x+2) = 48\n"
                   "3x + 3 = 48\n"
                   "x = 15\n"
                   "Integers: 15, 16, 17",
    },
    {
        "title": "Age Problems",
        "body": (
            "Age problems involve relationships between ages "
            "now and at some point in the past or future.\n\n"
            "Key strategy:\n"
            "  Let x = someone's age NOW\n"
            "  Past age = x - years ago\n"
            "  Future age = x + years hence\n"
            "  If A is 3 times older than B: A = 3B\n\n"
            "Always define what x represents clearly "
            "before setting up the equation."
        ),
        "formula": None,
        "example": "Maria is 3 times as old as her brother.\n"
                   "In 5 years, she will be twice his age.\n"
                   "Let brother = x, Maria = 3x\n"
                   "In 5 years: 3x+5 = 2(x+5)\n"
                   "3x+5 = 2x+10\n"
                   "x = 5  (brother is 5, Maria is 15)",
    },
    {
        "title": "Distance–Speed–Time Problems",
        "body": (
            "The fundamental formula:\n"
            "    Distance = Speed × Time\n"
            "    (D = S × T)\n\n"
            "From this: S = D/T  and  T = D/S\n\n"
            "Common setups:\n"
            "  Two objects moving toward each other: "
            "combined speed = S₁ + S₂\n"
            "  Same distance, different speeds: "
            "D₁ = D₂\n"
            "  Round trip: time out + time back = total time\n\n"
            "Always use consistent units (km/h and km, or m/s and m)."
        ),
        "formula": "D = S × T",
        "example": "Two cars start 300 km apart and drive toward each other.\n"
                   "Car A: 60 km/h, Car B: 40 km/h.\n"
                   "Time to meet: 300 / (60+40) = 300/100 = 3 hours",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "The sum of two consecutive integers is 47. Find them.",
        "steps": [
            ("Define variables",
             "Let x = first integer\nThen x + 1 = second integer"),
            ("Write the equation",
             "x + (x + 1) = 47"),
            ("Simplify and solve",
             "2x + 1 = 47\n2x = 46\nx = 23"),
            ("State both answers",
             "The integers are 23 and 24"),
        ],
        "check": "23 + 24 = 47 ✓  and  24 = 23 + 1 ✓",
        "notes": "Always state what x represents at the start.",
    },
    {
        "problem": "A shirt costs $12 more than a hat. Together they cost $48. Find each price.",
        "steps": [
            ("Define variables",
             "Let h = cost of hat\nThen h + 12 = cost of shirt"),
            ("Write the equation",
             "h + (h + 12) = 48"),
            ("Simplify and solve",
             "2h + 12 = 48\n2h = 36\nh = 18"),
            ("Find both prices",
             "Hat = $18, Shirt = $18 + $12 = $30"),
        ],
        "check": "$18 + $30 = $48 ✓  and  $30 − $18 = $12 ✓",
        "notes": "Read the question carefully — it asks for BOTH prices.",
    },
    {
        "problem": "A train travels at 80 km/h for 3 hours. How far does it travel?",
        "steps": [
            ("Identify the formula",
             "Distance = Speed × Time"),
            ("Substitute values",
             "D = 80 × 3"),
            ("Calculate",
             "D = 240 km"),
        ],
        "check": "240 ÷ 80 = 3 hours ✓",
        "notes": "D = S × T is the foundation of all distance problems.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Not defining what x represents",
        "example": "Writing x + 5 = 12 without saying what x is",
        "fix":     "Always start with 'Let x = ...' before writing any equation.",
    },
    {
        "mistake": "Confusing 'less than' direction",
        "example": "'5 less than x' written as 5 - x instead of x - 5",
        "fix":     "'5 less than x' means x - 5. The quantity comes before 'less than'.",
    },
    {
        "mistake": "Not checking the answer in the original problem",
        "example": "Getting x = 7 but not verifying it satisfies the word problem",
        "fix":     "Substitute back into the WORDS of the problem, not just the equation.",
    },
    {
        "mistake": "Mixing units in distance problems",
        "example": "Using km/h for speed and minutes for time",
        "fix":     "Convert all units to match before substituting into D = S × T.",
    },
]

KEY_VOCABULARY = {
    "Variable":           "A letter representing the unknown quantity you want to find.",
    "Define":             "State clearly what your variable represents before using it.",
    "Translate":          "Convert a word or phrase into a mathematical symbol or expression.",
    "Consecutive":        "Following one after another. Consecutive integers: 5, 6, 7.",
    "Sum":                "The result of addition.",
    "Difference":         "The result of subtraction.",
    "Product":            "The result of multiplication.",
    "Quotient":           "The result of division.",
    "D = S × T":          "Distance equals Speed multiplied by Time.",
    "Verify / Check":     "Substitute your answer back into the original problem to confirm it works.",
}