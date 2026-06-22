# =============================================================================
# content/geometry/triangles.py
# Teaching content for Triangles.
# =============================================================================

TOPIC_TITLE = "Triangles"

TOPIC_INTRO = (
    "Triangles are the building blocks of all geometry. Every polygon can "
    "be divided into triangles, and many real-world structures rely on their "
    "strength and stability. Understanding triangle properties — angles, sides, "
    "area, and the Pythagorean theorem — is essential for all further geometry."
)

CONCEPT_CARDS = [
    {
        "title": "Triangle Angle Sum",
        "body": (
            "The three interior angles of ANY triangle always add up to 180°.\n\n"
            "This is true for every triangle — no exceptions.\n\n"
            "You can use this to find a missing angle:\n"
            "Missing angle = 180° - (sum of the other two angles)\n\n"
            "An exterior angle of a triangle equals the sum of the two\n"
            "non-adjacent interior angles (exterior angle theorem)."
        ),
        "formula": "Angle A + Angle B + Angle C = 180°",
        "example": "A triangle has angles 50° and 70°.\n"
                   "Third angle = 180° - 50° - 70° = 60°",
    },
    {
        "title": "Types of Triangles",
        "body": (
            "By ANGLES:\n"
            "  Acute triangle:    all angles < 90°\n"
            "  Right triangle:    one angle = 90°\n"
            "  Obtuse triangle:   one angle > 90°\n\n"
            "By SIDES:\n"
            "  Equilateral:  all 3 sides equal, all angles = 60°\n"
            "  Isosceles:    2 sides equal, base angles equal\n"
            "  Scalene:      no sides equal, no angles equal\n\n"
            "Isosceles key fact: the two base angles are always equal."
        ),
        "formula": "Equilateral: all angles = 60°\nIsosceles: base angles equal",
        "example": "Isosceles triangle with apex angle 40°:\n"
                   "Base angles = (180° - 40°) / 2 = 70° each",
    },
    {
        "title": "The Pythagorean Theorem",
        "body": (
            "In a RIGHT-ANGLED triangle only:\n\n"
            "The square of the hypotenuse equals the sum of the\n"
            "squares of the other two sides.\n\n"
            "The HYPOTENUSE is always the longest side,\n"
            "opposite the right angle.\n\n"
            "Use it to:\n"
            "  Find the hypotenuse: c = √(a² + b²)\n"
            "  Find a leg: a = √(c² - b²)"
        ),
        "formula": "a² + b² = c²\n(c = hypotenuse)",
        "example": "Right triangle with legs 3 and 4:\n"
                   "c² = 3² + 4² = 9 + 16 = 25\n"
                   "c = √25 = 5",
    },
    {
        "title": "Area of a Triangle",
        "body": (
            "The area of a triangle is:\n\n"
            "    Area = ½ × base × height\n\n"
            "The HEIGHT must be perpendicular (at 90°) to the BASE.\n"
            "It doesn't have to be a side of the triangle — it can be\n"
            "drawn from a vertex straight down to the base.\n\n"
            "For any triangle, you can choose any side as the base,\n"
            "as long as you use the corresponding perpendicular height."
        ),
        "formula": "Area = ½ × b × h",
        "example": "Base = 10 cm, height = 6 cm:\n"
                   "Area = ½ × 10 × 6 = 30 cm²",
    },
    {
        "title": "Perimeter of a Triangle",
        "body": (
            "The PERIMETER is the total distance around the outside —\n"
            "simply add all three sides together.\n\n"
            "For special triangles:\n"
            "  Equilateral: P = 3 × side\n"
            "  Isosceles:   P = 2 × equal side + base\n\n"
            "Common Pythagorean triples (memorise these!):\n"
            "  3, 4, 5\n"
            "  5, 12, 13\n"
            "  8, 15, 17\n"
            "  Their multiples also work: 6, 8, 10 / 9, 12, 15"
        ),
        "formula": "Perimeter = a + b + c",
        "example": "Triangle with sides 7, 8, 9:\n"
                   "Perimeter = 7 + 8 + 9 = 24 cm",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "A right triangle has legs of 5 cm and 12 cm. Find the hypotenuse.",
        "steps": [
            ("Write the Pythagorean theorem",
             "a² + b² = c²"),
            ("Substitute the known values",
             "5² + 12² = c²"),
            ("Calculate each square",
             "25 + 144 = c²  →  169 = c²"),
            ("Take the square root",
             "c = √169 = 13 cm"),
        ],
        "check": "5² + 12² = 25 + 144 = 169 = 13² ✓",
        "notes": "5, 12, 13 is a Pythagorean triple — worth memorising.",
    },
    {
        "problem": "An isosceles triangle has an apex angle of 50°. Find each base angle.",
        "steps": [
            ("Angles in a triangle sum to 180°",
             "50° + base angle + base angle = 180°"),
            ("The two base angles are equal (isosceles)",
             "50° + 2 × base angle = 180°"),
            ("Subtract 50°",
             "2 × base angle = 130°"),
            ("Divide by 2",
             "base angle = 65°"),
        ],
        "check": "50° + 65° + 65° = 180° ✓",
        "notes": "In an isosceles triangle, the two base angles are always equal.",
    },
    {
        "problem": "Find the area of a triangle with base 14 cm and height 9 cm.",
        "steps": [
            ("Write the area formula",
             "Area = ½ × base × height"),
            ("Substitute values",
             "Area = ½ × 14 × 9"),
            ("Calculate",
             "Area = ½ × 126 = 63 cm²"),
        ],
        "check": "½ × 14 × 9 = 7 × 9 = 63 ✓",
        "notes": "Remember the height must be perpendicular to the base.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Forgetting that triangle angles must sum to 180°",
        "example": "Accepting a triangle with angles 90°, 95°, 40° (sums to 225°)",
        "fix":     "Always verify: angle A + angle B + angle C = 180°.",
    },
    {
        "mistake": "Using a side instead of the perpendicular height in area formula",
        "example": "Area = ½ × 8 × 6 using a slanted side of 6 instead of vertical height",
        "fix":     "The height MUST be perpendicular to the base. Draw it in if not shown.",
    },
    {
        "mistake": "Applying Pythagorean theorem to non-right triangles",
        "example": "Using a² + b² = c² on an obtuse triangle",
        "fix":     "Pythagorean theorem ONLY works for right-angled triangles.",
    },
    {
        "mistake": "Confusing hypotenuse with other sides",
        "example": "Treating a leg as the hypotenuse in c² = a² + b²",
        "fix":     "Hypotenuse is always opposite the right angle and always the longest side.",
    },
]

KEY_VOCABULARY = {
    "Hypotenuse":        "The longest side of a right triangle, opposite the right angle.",
    "Leg":               "Either of the two shorter sides of a right triangle.",
    "Equilateral":       "A triangle with all three sides equal and all angles 60°.",
    "Isosceles":         "A triangle with exactly two equal sides and two equal base angles.",
    "Scalene":           "A triangle with no equal sides and no equal angles.",
    "Apex Angle":        "The angle between the two equal sides of an isosceles triangle.",
    "Base Angles":       "The two equal angles at the base of an isosceles triangle.",
    "Pythagorean Triple":"A set of three integers satisfying a²+b²=c², like 3,4,5.",
    "Perimeter":         "The total length around the outside of a shape.",
    "Perpendicular":     "At exactly 90° to another line.",
}