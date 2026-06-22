# =============================================================================
# content/geometry/polygons.py
# Teaching content for Polygons.
# =============================================================================

TOPIC_TITLE = "Polygons"

TOPIC_INTRO = (
    "A polygon is any closed flat shape with straight sides. From triangles "
    "to hexagons to octagons, understanding how to find interior angles, "
    "exterior angles, and areas of polygons is a core geometry skill."
)

CONCEPT_CARDS = [
    {
        "title": "Polygon Basics and Names",
        "body": (
            "A polygon is named by its number of sides:\n\n"
            "  3 sides — Triangle\n"
            "  4 sides — Quadrilateral\n"
            "  5 sides — Pentagon\n"
            "  6 sides — Hexagon\n"
            "  7 sides — Heptagon\n"
            "  8 sides — Octagon\n"
            "  10 sides — Decagon\n\n"
            "A REGULAR polygon has all sides equal AND all angles equal.\n"
            "An IRREGULAR polygon has sides or angles of different sizes."
        ),
        "formula": None,
        "example": "A regular hexagon has 6 equal sides and 6 equal angles.\n"
                   "A rectangle is a regular quadrilateral? No — sides differ.",
    },
    {
        "title": "Sum of Interior Angles",
        "body": (
            "For any polygon with n sides, the sum of interior angles is:\n\n"
            "    (n - 2) × 180°\n\n"
            "Why? Any polygon can be divided into triangles by drawing\n"
            "diagonals from one vertex. An n-sided polygon splits into\n"
            "(n - 2) triangles, each contributing 180°.\n\n"
            "For a REGULAR polygon, each interior angle is:\n"
            "    (n - 2) × 180° ÷ n"
        ),
        "formula": "Sum of interior angles = (n - 2) × 180°\nEach angle (regular) = (n-2)×180° ÷ n",
        "example": "Pentagon (n=5):  (5-2)×180 = 540°\n"
                   "Each angle of regular pentagon: 540÷5 = 108°",
    },
    {
        "title": "Exterior Angles",
        "body": (
            "An EXTERIOR angle is formed between one side of the polygon\n"
            "and the extension of the adjacent side.\n\n"
            "KEY FACT: The sum of ALL exterior angles of ANY polygon = 360°\n"
            "This is true for any convex polygon, regardless of sides.\n\n"
            "For a regular polygon with n sides:\n"
            "    Each exterior angle = 360° ÷ n\n\n"
            "Interior angle + exterior angle = 180° (they're supplementary)"
        ),
        "formula": "Sum of exterior angles = 360°\nEach exterior (regular) = 360° ÷ n",
        "example": "Regular hexagon:\n"
                   "Each exterior = 360 ÷ 6 = 60°\n"
                   "Each interior = 180 - 60 = 120°",
    },
    {
        "title": "Area of Rectangles, Squares, and Parallelograms",
        "body": (
            "RECTANGLE:\n"
            "    Area = length × width\n"
            "    Perimeter = 2(l + w)\n\n"
            "SQUARE (special rectangle):\n"
            "    Area = side²\n"
            "    Perimeter = 4 × side\n\n"
            "PARALLELOGRAM:\n"
            "    Area = base × height\n"
            "    (height is perpendicular to base, not the slant side)\n\n"
            "Note: A rectangle is a parallelogram with right angles."
        ),
        "formula": "Rectangle: A = l × w\nParallelogram: A = b × h",
        "example": "Rectangle 8 cm × 5 cm:\n"
                   "Area = 40 cm²,  Perimeter = 26 cm",
    },
    {
        "title": "Area of Trapezoids and Regular Polygons",
        "body": (
            "TRAPEZOID (one pair of parallel sides):\n"
            "    Area = ½ × (a + b) × h\n"
            "    where a and b are the parallel sides and h is the height\n\n"
            "RHOMBUS (all sides equal, opposite angles equal):\n"
            "    Area = ½ × d₁ × d₂\n"
            "    where d₁ and d₂ are the diagonals\n\n"
            "Always identify which formula applies before calculating."
        ),
        "formula": "Trapezoid: A = ½(a+b)h\nRhombus: A = ½d₁d₂",
        "example": "Trapezoid with parallel sides 6 and 10, height 4:\n"
                   "Area = ½ × (6+10) × 4 = ½ × 16 × 4 = 32 cm²",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Find the sum of interior angles of an octagon.",
        "steps": [
            ("An octagon has 8 sides, so n = 8",
             "n = 8"),
            ("Apply the formula",
             "Sum = (n - 2) × 180°"),
            ("Substitute",
             "Sum = (8 - 2) × 180° = 6 × 180°"),
            ("Calculate",
             "Sum = 1080°"),
        ],
        "check": "Each interior angle of a regular octagon = 1080 ÷ 8 = 135° ✓",
        "notes": "Memorise (n-2)×180 — it applies to ALL polygons.",
    },
    {
        "problem": "A regular polygon has each interior angle of 144°. How many sides does it have?",
        "steps": [
            ("Find the exterior angle",
             "Exterior = 180° - 144° = 36°"),
            ("Use: exterior angle = 360° ÷ n",
             "36 = 360 ÷ n"),
            ("Solve for n",
             "n = 360 ÷ 36 = 10"),
        ],
        "check": "(10-2)×180 = 1440°. Each angle = 1440÷10 = 144° ✓",
        "notes": "Working from the exterior angle is usually the fastest route.",
    },
    {
        "problem": "Find the area of a trapezoid with parallel sides 8 cm and 14 cm and height 6 cm.",
        "steps": [
            ("Write the formula",
             "Area = ½ × (a + b) × h"),
            ("Substitute",
             "Area = ½ × (8 + 14) × 6"),
            ("Simplify",
             "Area = ½ × 22 × 6"),
            ("Calculate",
             "Area = 66 cm²"),
        ],
        "check": "½ × 22 × 6 = 11 × 6 = 66 ✓",
        "notes": "The two parallel sides go into (a+b), and h is the perpendicular distance between them.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Using n instead of (n-2) in the interior angle formula",
        "example": "Sum = n × 180° instead of (n-2) × 180°",
        "fix":     "Always subtract 2 from the number of sides first.",
    },
    {
        "mistake": "Confusing interior and exterior angle formulas",
        "example": "Each interior = 360°÷n (that's the exterior formula)",
        "fix":     "Interior = (n-2)×180÷n. Exterior = 360÷n. They add to 180°.",
    },
    {
        "mistake": "Using slant height instead of perpendicular height for parallelograms",
        "example": "Area = base × slant side (WRONG)",
        "fix":     "Height must be perpendicular to the base — draw it in if unclear.",
    },
    {
        "mistake": "Adding instead of averaging the parallel sides in trapezoid formula",
        "example": "Area = (a+b)×h instead of ½(a+b)×h",
        "fix":     "The ½ in the trapezoid formula is essential — it averages the two parallel sides.",
    },
]

KEY_VOCABULARY = {
    "Polygon":          "A closed flat shape with straight sides.",
    "Regular Polygon":  "A polygon with all sides equal and all angles equal.",
    "Interior Angle":   "An angle inside the polygon at a vertex.",
    "Exterior Angle":   "The angle between a side and the extension of the adjacent side.",
    "Diagonal":         "A line segment connecting two non-adjacent vertices.",
    "Quadrilateral":    "A polygon with 4 sides.",
    "Trapezoid":        "A quadrilateral with exactly one pair of parallel sides.",
    "Parallelogram":    "A quadrilateral with two pairs of parallel sides.",
    "Rhombus":          "A parallelogram with all sides equal.",
    "Convex Polygon":   "A polygon where all interior angles are less than 180°.",
}