# =============================================================================
# content/geometry/angles_lines.py
# Teaching content for Angles & Lines.
# =============================================================================

TOPIC_TITLE = "Angles & Lines"

TOPIC_INTRO = (
    "Angles are formed when two lines meet at a point. Understanding the "
    "relationships between angles — especially when lines are parallel — "
    "is fundamental to all of geometry. Most angle problems reduce to "
    "applying a small set of rules consistently."
)

CONCEPT_CARDS = [
    {
        "title": "Types of Angles",
        "body": (
            "Angles are measured in degrees (°).\n\n"
            "Acute angle:    0° < angle < 90°\n"
            "Right angle:    exactly 90°  (shown with a small square)\n"
            "Obtuse angle:   90° < angle < 180°\n"
            "Straight angle: exactly 180°  (a straight line)\n"
            "Reflex angle:   180° < angle < 360°\n\n"
            "A full rotation is 360°."
        ),
        "formula": "Acute < 90° < Obtuse < 180° < Reflex < 360°",
        "example": "45° is acute\n90° is a right angle\n135° is obtuse\n270° is reflex",
    },
    {
        "title": "Complementary and Supplementary Angles",
        "body": (
            "COMPLEMENTARY angles add up to 90°.\n"
            "  If two angles are complementary and one is 35°,\n"
            "  the other is 90° - 35° = 55°.\n\n"
            "SUPPLEMENTARY angles add up to 180°.\n"
            "  If two angles are supplementary and one is 110°,\n"
            "  the other is 180° - 110° = 70°.\n\n"
            "Memory trick: C comes before S alphabetically,\n"
            "and 90 comes before 180."
        ),
        "formula": "Complementary: a + b = 90°\nSupplementary: a + b = 180°",
        "example": "Find the complement of 28°:\n"
                   "90° - 28° = 62°\n\n"
                   "Find the supplement of 115°:\n"
                   "180° - 115° = 65°",
    },
    {
        "title": "Vertically Opposite Angles",
        "body": (
            "When two straight lines cross, they form 4 angles.\n"
            "The angles OPPOSITE each other (across the intersection)\n"
            "are called vertically opposite angles.\n\n"
            "KEY FACT: Vertically opposite angles are ALWAYS EQUAL.\n\n"
            "Also, adjacent angles at an intersection are supplementary\n"
            "(they add up to 180° because they form a straight line)."
        ),
        "formula": "Vertically opposite angles are equal",
        "example": "Two lines cross. One angle is 70°.\n"
                   "The opposite angle is also 70°.\n"
                   "The other two angles are each 180° - 70° = 110°.",
    },
    {
        "title": "Parallel Lines and a Transversal",
        "body": (
            "When a line (transversal) crosses two parallel lines,\n"
            "it creates 8 angles with special relationships:\n\n"
            "CORRESPONDING angles: same position at each crossing — EQUAL\n"
            "  (like F-shape between the lines)\n\n"
            "ALTERNATE angles: on opposite sides of the transversal — EQUAL\n"
            "  (like Z-shape or N-shape between the lines)\n\n"
            "CO-INTERIOR (same-side interior) angles: — ADD TO 180°\n"
            "  (like C-shape between the lines)"
        ),
        "formula": "Corresponding = equal\nAlternate = equal\nCo-interior = 180°",
        "example": "Parallel lines, transversal creates 65° at top.\n"
                   "Corresponding angle below: 65°\n"
                   "Alternate angle: 65°\n"
                   "Co-interior angle: 180° - 65° = 115°",
    },
    {
        "title": "Angles on a Straight Line and at a Point",
        "body": (
            "ANGLES ON A STRAIGHT LINE:\n"
            "All angles on one side of a straight line add up to 180°.\n\n"
            "ANGLES AT A POINT:\n"
            "All angles around a single point add up to 360°.\n\n"
            "These two facts, combined with the parallel line rules,\n"
            "let you find any unknown angle in a diagram."
        ),
        "formula": "Angles on line = 180°\nAngles at point = 360°",
        "example": "Three angles on a straight line: 40°, x°, 80°\n"
                   "40 + x + 80 = 180\n"
                   "x = 60°",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Two angles are supplementary. One angle is 3x + 20° and the other is x + 40°. Find x.",
        "steps": [
            ("Supplementary angles add to 180°",
             "(3x + 20) + (x + 40) = 180"),
            ("Simplify the left side",
             "4x + 60 = 180"),
            ("Subtract 60 from both sides",
             "4x = 120"),
            ("Divide by 4",
             "x = 30"),
        ],
        "check": "3(30)+20=110°  and  30+40=70°  → 110+70=180° ✓",
        "notes": "Always write the angle relationship equation first.",
    },
    {
        "problem": "A transversal crosses two parallel lines. One angle is 4x + 15°. Its co-interior angle is 2x + 45°. Find x.",
        "steps": [
            ("Co-interior angles add to 180°",
             "(4x + 15) + (2x + 45) = 180"),
            ("Simplify",
             "6x + 60 = 180"),
            ("Subtract 60",
             "6x = 120"),
            ("Divide by 6",
             "x = 20"),
        ],
        "check": "4(20)+15=95° and 2(20)+45=85° → 95+85=180° ✓",
        "notes": "Co-interior is the only parallel-line pair that adds to 180°. Corresponding and alternate are equal.",
    },
    {
        "problem": "Find the vertically opposite angle to (5x - 10)° if its vertical pair is (3x + 30)°.",
        "steps": [
            ("Vertically opposite angles are equal",
             "5x - 10 = 3x + 30"),
            ("Subtract 3x from both sides",
             "2x - 10 = 30"),
            ("Add 10",
             "2x = 40"),
            ("Divide by 2",
             "x = 20"),
        ],
        "check": "5(20)-10=90° and 3(20)+30=90° ✓ — both equal 90°",
        "notes": "Set the two expressions equal to each other, then solve.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Confusing complementary (90°) and supplementary (180°)",
        "example": "Writing a + b = 180° for complementary angles",
        "fix":     "C for Complementary = 90°. S for Supplementary = 180°. C comes before S.",
    },
    {
        "mistake": "Thinking co-interior angles are equal instead of supplementary",
        "example": "Setting co-interior angles equal when they should add to 180°",
        "fix":     "Only corresponding and alternate angles are equal. Co-interior angles add to 180°.",
    },
    {
        "mistake": "Forgetting to check if lines are actually parallel before using parallel line rules",
        "example": "Applying alternate angle rule when lines are not stated to be parallel",
        "fix":     "Parallel line rules ONLY apply when lines are explicitly stated to be parallel.",
    },
    {
        "mistake": "Not using all angles on a straight line = 180°",
        "example": "Missing an intermediate step that requires the straight line rule",
        "fix":     "Whenever you see angles on the same side of a line, their sum is 180°.",
    },
]

KEY_VOCABULARY = {
    "Acute Angle":         "An angle less than 90°.",
    "Right Angle":         "An angle of exactly 90°.",
    "Obtuse Angle":        "An angle between 90° and 180°.",
    "Straight Angle":      "An angle of exactly 180° — a straight line.",
    "Complementary":       "Two angles that add to 90°.",
    "Supplementary":       "Two angles that add to 180°.",
    "Vertically Opposite": "Equal angles formed opposite each other when two lines cross.",
    "Transversal":         "A line that crosses two or more other lines.",
    "Corresponding":       "Equal angles in the same position at parallel line crossings (F-shape).",
    "Alternate":           "Equal angles on opposite sides of a transversal (Z-shape).",
    "Co-interior":         "Angles between parallel lines on the same side — add to 180° (C-shape).",
}