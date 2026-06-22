# =============================================================================
# content/geometry/circles.py
# Teaching content for Circles.
# =============================================================================

TOPIC_TITLE = "Circles"

TOPIC_INTRO = (
    "Circles appear everywhere in mathematics and the real world. "
    "Understanding the key measurements — circumference, area, arc length, "
    "and sector area — all depend on a single constant: π (pi ≈ 3.14159)."
)

CONCEPT_CARDS = [
    {
        "title": "Circle Vocabulary",
        "body": (
            "CENTRE: the middle point equidistant from all points on the circle.\n\n"
            "RADIUS (r): the distance from the centre to any point on the circle.\n\n"
            "DIAMETER (d): the distance across the circle through the centre.\n"
            "    d = 2r  (diameter is always twice the radius)\n\n"
            "CIRCUMFERENCE: the perimeter (distance around) the circle.\n\n"
            "CHORD: a line segment connecting two points on the circle.\n\n"
            "ARC: part of the circumference.\n\n"
            "SECTOR: a pie-slice shaped region (two radii + an arc)."
        ),
        "formula": "d = 2r",
        "example": "Circle with radius 5 cm:\n"
                   "Diameter = 2 × 5 = 10 cm",
    },
    {
        "title": "Circumference of a Circle",
        "body": (
            "The circumference is the distance all the way around the circle.\n\n"
            "π (pi) is the ratio of any circle's circumference to its diameter.\n"
            "π ≈ 3.14159...  (use 3.14 or the π button on your calculator)\n\n"
            "Two equivalent formulas:\n"
            "    C = π × d      (using diameter)\n"
            "    C = 2π × r     (using radius)\n\n"
            "Both give the same answer since d = 2r."
        ),
        "formula": "C = πd = 2πr",
        "example": "Circle with radius 7 cm:\n"
                   "C = 2 × π × 7 = 14π ≈ 43.98 cm",
    },
    {
        "title": "Area of a Circle",
        "body": (
            "The area of a circle is:\n\n"
            "    A = π × r²\n\n"
            "Note: the formula uses the RADIUS, not the diameter.\n"
            "If given the diameter, halve it first: r = d/2\n\n"
            "Area is always in SQUARE units (cm², m², etc.).\n"
            "Circumference is in LINEAR units (cm, m, etc.).\n\n"
            "Common error: using d instead of r in the area formula."
        ),
        "formula": "A = πr²",
        "example": "Circle with radius 6 cm:\n"
                   "A = π × 6² = 36π ≈ 113.1 cm²",
    },
    {
        "title": "Arc Length",
        "body": (
            "An arc is a portion of the circumference.\n"
            "Its length depends on the angle at the centre (the arc angle θ).\n\n"
            "Arc length = (θ/360°) × circumference\n"
            "           = (θ/360°) × 2πr\n\n"
            "Think of it as a FRACTION of the full circumference.\n"
            "A semicircle (180°) has arc = half the circumference.\n"
            "A quarter circle (90°) has arc = quarter of the circumference."
        ),
        "formula": "Arc length = (θ/360) × 2πr",
        "example": "Circle r=10 cm, arc angle = 90°:\n"
                   "Arc = (90/360) × 2π×10 = ¼ × 20π = 5π ≈ 15.71 cm",
    },
    {
        "title": "Sector Area",
        "body": (
            "A sector is the pie-slice shaped region between two radii and an arc.\n\n"
            "Sector area = (θ/360°) × full circle area\n"
            "            = (θ/360°) × πr²\n\n"
            "Just like arc length, it's a FRACTION of the full circle.\n\n"
            "The fraction θ/360 appears in both:\n"
            "  Arc length:   (θ/360) × 2πr\n"
            "  Sector area:  (θ/360) × πr²"
        ),
        "formula": "Sector area = (θ/360) × πr²",
        "example": "Circle r=6 cm, sector angle = 60°:\n"
                   "Sector = (60/360) × π×36 = (1/6) × 36π = 6π ≈ 18.85 cm²",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Find the circumference and area of a circle with diameter 12 cm. Use π = 3.14.",
        "steps": [
            ("Find the radius",
             "r = d ÷ 2 = 12 ÷ 2 = 6 cm"),
            ("Find circumference",
             "C = 2πr = 2 × 3.14 × 6 = 37.68 cm"),
            ("Find area",
             "A = πr² = 3.14 × 6² = 3.14 × 36 = 113.04 cm²"),
        ],
        "check": "C ≈ 37.68 cm (linear units), A ≈ 113.04 cm² (square units) ✓",
        "notes": "Always halve the diameter to get the radius before applying formulas.",
    },
    {
        "problem": "Find the arc length of a sector with radius 10 cm and angle 72°. Use π = 3.14.",
        "steps": [
            ("Write the arc length formula",
             "Arc = (θ/360) × 2πr"),
            ("Substitute values",
             "Arc = (72/360) × 2 × 3.14 × 10"),
            ("Simplify the fraction",
             "72/360 = 1/5"),
            ("Calculate",
             "Arc = (1/5) × 62.8 = 12.56 cm"),
        ],
        "check": "72° is 1/5 of 360°. Full circumference = 2π×10 ≈ 62.8. 62.8÷5 = 12.56 ✓",
        "notes": "Simplify θ/360 to a simple fraction first — makes the arithmetic easier.",
    },
    {
        "problem": "A sector has radius 9 cm and angle 120°. Find its area. Use π = 3.14.",
        "steps": [
            ("Write sector area formula",
             "Sector area = (θ/360) × πr²"),
            ("Substitute",
             "= (120/360) × 3.14 × 9²"),
            ("Simplify",
             "120/360 = 1/3,  and  9² = 81"),
            ("Calculate",
             "= (1/3) × 3.14 × 81 = (1/3) × 254.34 = 84.78 cm²"),
        ],
        "check": "120° = 1/3 of 360°. Full area = 3.14×81 = 254.34. ÷3 ≈ 84.78 ✓",
        "notes": "Both arc and sector formulas use the same θ/360 fraction.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Using diameter instead of radius in area formula",
        "example": "A = π × 12² instead of A = π × 6² for a circle with diameter 12",
        "fix":     "ALWAYS halve the diameter to get r before using A = πr².",
    },
    {
        "mistake": "Confusing circumference (linear) and area (square) units",
        "example": "Writing circumference as 50 cm² or area as 50 cm",
        "fix":     "Circumference → cm or m. Area → cm² or m². Units reveal the formula.",
    },
    {
        "mistake": "Forgetting to square r in the area formula",
        "example": "A = π × r instead of A = π × r²",
        "fix":     "The formula is A = πr². The radius must be squared.",
    },
    {
        "mistake": "Using the wrong fraction for sectors",
        "example": "Using θ/180 instead of θ/360",
        "fix":     "A full circle is 360°. The fraction of the circle is always θ/360.",
    },
]

KEY_VOCABULARY = {
    "Radius":        "Distance from centre to edge of circle (r). Half the diameter.",
    "Diameter":      "Distance across circle through the centre (d = 2r).",
    "Circumference": "The perimeter (distance around) a circle. C = 2πr.",
    "Pi (π)":        "The ratio of circumference to diameter ≈ 3.14159.",
    "Arc":           "A portion of the circumference.",
    "Sector":        "A pie-slice region bounded by two radii and an arc.",
    "Chord":         "A line segment connecting two points on a circle.",
    "Tangent":       "A line that touches the circle at exactly one point.",
    "Arc Angle":     "The angle at the centre of a circle that subtends the arc.",
    "Semicircle":    "Half a circle — arc angle is 180°.",
}