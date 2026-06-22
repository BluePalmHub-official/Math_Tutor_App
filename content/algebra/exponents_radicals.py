# =============================================================================
# content/algebra/exponents_radicals.py
# Teaching content for the Exponents & Radicals topic.
# =============================================================================

TOPIC_TITLE = "Exponents & Radicals"

TOPIC_INTRO = (
    "Exponents are a shorthand for repeated multiplication, and radicals "
    "(square roots, cube roots) are their inverse. Mastering the laws of "
    "exponents lets you simplify complex expressions quickly and confidently."
)

CONCEPT_CARDS = [
    {
        "title": "What is an Exponent?",
        "body": (
            "An exponent tells you how many times to multiply a base by itself.\n\n"
            "    bⁿ  means  b × b × b × ... × b  (n times)\n\n"
            "b is the BASE — the number being multiplied.\n"
            "n is the EXPONENT (or power) — how many times.\n\n"
            "Special cases:\n"
            "  b¹ = b          (any number to the power 1 is itself)\n"
            "  b⁰ = 1          (any non-zero number to the power 0 is 1)\n"
            "  b⁻ⁿ = 1/bⁿ     (negative exponent means reciprocal)"
        ),
        "formula": "bⁿ = b × b × b × ... (n times)",
        "example": "2³ = 2 × 2 × 2 = 8\n"
                   "5⁰ = 1\n"
                   "3⁻² = 1/3² = 1/9",
    },
    {
        "title": "Laws of Exponents — Multiplying and Dividing",
        "body": (
            "When the BASES are the same, you can combine exponents:\n\n"
            "PRODUCT RULE (multiplying):\n"
            "    bᵐ × bⁿ = bᵐ⁺ⁿ\n"
            "    Add the exponents.\n\n"
            "QUOTIENT RULE (dividing):\n"
            "    bᵐ ÷ bⁿ = bᵐ⁻ⁿ\n"
            "    Subtract the exponents.\n\n"
            "These rules ONLY work when the bases are identical."
        ),
        "formula": "bᵐ × bⁿ = bᵐ⁺ⁿ      bᵐ ÷ bⁿ = bᵐ⁻ⁿ",
        "example": "2³ × 2⁴ = 2⁷ = 128\n"
                   "5⁶ ÷ 5² = 5⁴ = 625\n"
                   "x⁵ × x³ = x⁸",
    },
    {
        "title": "Laws of Exponents — Powers",
        "body": (
            "POWER OF A POWER:\n"
            "    (bᵐ)ⁿ = bᵐⁿ\n"
            "    Multiply the exponents.\n\n"
            "POWER OF A PRODUCT:\n"
            "    (ab)ⁿ = aⁿbⁿ\n"
            "    Distribute the exponent to each factor.\n\n"
            "POWER OF A QUOTIENT:\n"
            "    (a/b)ⁿ = aⁿ/bⁿ\n"
            "    Apply the exponent to numerator and denominator."
        ),
        "formula": "(bᵐ)ⁿ = bᵐⁿ      (ab)ⁿ = aⁿbⁿ",
        "example": "(2³)⁴ = 2¹² = 4096\n"
                   "(3x)² = 9x²\n"
                   "(2/3)³ = 8/27",
    },
    {
        "title": "Square Roots and Cube Roots",
        "body": (
            "A RADICAL is the inverse of an exponent.\n\n"
            "Square root: √b is the number that squared gives b.\n"
            "    √9 = 3  because  3² = 9\n\n"
            "Cube root: ³√b is the number that cubed gives b.\n"
            "    ³√8 = 2  because  2³ = 8\n\n"
            "Simplifying radicals:\n"
            "    √(a × b) = √a × √b\n"
            "Look for perfect square factors to pull out."
        ),
        "formula": "√(a × b) = √a × √b",
        "example": "√48 = √(16 × 3) = √16 × √3 = 4√3\n"
                   "√75 = √(25 × 3) = 5√3",
    },
    {
        "title": "Fractional Exponents",
        "body": (
            "Fractional exponents connect exponents and radicals:\n\n"
            "    b^(1/n) = ⁿ√b   (the nth root of b)\n"
            "    b^(m/n) = (ⁿ√b)ᵐ = ⁿ√(bᵐ)\n\n"
            "This means all the exponent laws apply to roots too.\n\n"
            "Simplification strategy:\n"
            "1. Convert radicals to fractional exponents\n"
            "2. Apply exponent laws\n"
            "3. Convert back if needed"
        ),
        "formula": "b^(1/n) = ⁿ√b      b^(m/n) = (ⁿ√b)ᵐ",
        "example": "8^(1/3) = ³√8 = 2\n"
                   "4^(3/2) = (√4)³ = 2³ = 8\n"
                   "27^(2/3) = (³√27)² = 3² = 9",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Simplify:   2³ × 2⁵",
        "steps": [
            ("Check bases are the same",
             "Both bases are 2 — product rule applies"),
            ("Add the exponents",
             "2³ × 2⁵ = 2^(3+5) = 2⁸"),
            ("Calculate",
             "2⁸ = 256"),
        ],
        "check": "2³=8, 2⁵=32, 8×32=256  and  2⁸=256  ✓",
        "notes": "The product rule only works when the bases are the same.",
    },
    {
        "problem": "Simplify:   √72",
        "steps": [
            ("Find the largest perfect square factor of 72",
             "72 = 36 × 2  (36 is a perfect square)"),
            ("Split the radical",
             "√72 = √36 × √2"),
            ("Simplify √36",
             "= 6√2"),
        ],
        "check": "(6√2)² = 36 × 2 = 72  ✓",
        "notes": "Always look for the LARGEST perfect square factor for the most efficient simplification.",
    },
    {
        "problem": "Simplify:   (x³)⁴ ÷ x⁵",
        "steps": [
            ("Apply power of a power rule to (x³)⁴",
             "(x³)⁴ = x^(3×4) = x¹²"),
            ("Apply quotient rule",
             "x¹² ÷ x⁵ = x^(12-5)"),
            ("Simplify",
             "= x⁷"),
        ],
        "check": "Substitute x=2: (8)⁴÷2⁵=4096÷32=128=2⁷  ✓",
        "notes": "Work through one rule at a time — don't rush combining steps.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Adding bases instead of exponents",
        "example": "2³ × 2⁴ = 4⁷  (WRONG — bases stay the same)",
        "fix":     "Keep the base unchanged. Only ADD the exponents: 2³ × 2⁴ = 2⁷.",
    },
    {
        "mistake": "Applying product rule when bases differ",
        "example": "2³ × 3⁴ = 6⁷  (WRONG — different bases)",
        "fix":     "Product/quotient rules only work with IDENTICAL bases. Calculate each separately.",
    },
    {
        "mistake": "Forgetting b⁰ = 1",
        "example": "5⁰ = 0  (WRONG)",
        "fix":     "Any non-zero number to the power 0 equals 1. Always.",
    },
    {
        "mistake": "Not finding the largest perfect square when simplifying radicals",
        "example": "√72 = √(4×18) = 2√18  (not fully simplified)",
        "fix":     "Find the LARGEST perfect square factor. √72 = √(36×2) = 6√2.",
    },
]

KEY_VOCABULARY = {
    "Base":               "The number being raised to a power. In 3⁴, the base is 3.",
    "Exponent/Power":     "How many times the base multiplies itself. In 3⁴, the exponent is 4.",
    "Product Rule":       "bᵐ × bⁿ = bᵐ⁺ⁿ. Add exponents when multiplying same bases.",
    "Quotient Rule":      "bᵐ ÷ bⁿ = bᵐ⁻ⁿ. Subtract exponents when dividing same bases.",
    "Power Rule":         "(bᵐ)ⁿ = bᵐⁿ. Multiply exponents when raising a power to a power.",
    "Zero Exponent":      "b⁰ = 1 for any b ≠ 0.",
    "Negative Exponent":  "b⁻ⁿ = 1/bⁿ. A negative exponent means take the reciprocal.",
    "Radical":            "A root symbol √. The square root is most common.",
    "Perfect Square":     "A number that is the square of an integer: 1,4,9,16,25,36...",
    "Fractional Exponent":"b^(m/n) = (ⁿ√b)ᵐ. Links exponents and roots.",
}