# =============================================================================
# content/geometry/coordinate_geometry.py
# Teaching content for Coordinate Geometry.
# =============================================================================

TOPIC_TITLE = "Coordinate Geometry"

TOPIC_INTRO = (
    "Coordinate geometry (also called analytic geometry) connects algebra "
    "and geometry by placing shapes on a coordinate plane. You can find "
    "distances, midpoints, and equations of lines using simple formulas."
)

CONCEPT_CARDS = [
    {
        "title": "The Coordinate Plane",
        "body": (
            "The coordinate plane has two axes:\n"
            "  x-axis: horizontal (left-right)\n"
            "  y-axis: vertical (up-down)\n\n"
            "They intersect at the ORIGIN (0, 0).\n\n"
            "Every point is written as (x, y):\n"
            "  x tells you how far LEFT or RIGHT from the origin\n"
            "  y tells you how far UP or DOWN\n\n"
            "The plane is divided into 4 quadrants (I, II, III, IV)\n"
            "going anti-clockwise from top-right."
        ),
        "formula": "Point = (x, y)",
        "example": "Point A(3, 4): go 3 right, 4 up\n"
                   "Point B(-2, 5): go 2 left, 5 up\n"
                   "Point C(-1, -3): go 1 left, 3 down",
    },
    {
        "title": "The Distance Formula",
        "body": (
            "To find the distance between two points A(x₁, y₁) and B(x₂, y₂):\n\n"
            "    d = √[(x₂ - x₁)² + (y₂ - y₁)²]\n\n"
            "This comes directly from the Pythagorean theorem —\n"
            "the horizontal and vertical gaps form the legs of a right triangle,\n"
            "and the distance is the hypotenuse.\n\n"
            "Steps:\n"
            "1. Subtract x-coordinates: (x₂ - x₁)\n"
            "2. Subtract y-coordinates: (y₂ - y₁)\n"
            "3. Square both differences\n"
            "4. Add and take the square root"
        ),
        "formula": "d = √[(x₂-x₁)² + (y₂-y₁)²]",
        "example": "Distance from A(1,2) to B(4,6):\n"
                   "d = √[(4-1)² + (6-2)²]\n"
                   "  = √[9 + 16]\n"
                   "  = √25 = 5",
    },
    {
        "title": "The Midpoint Formula",
        "body": (
            "The midpoint of a line segment is exactly halfway between\n"
            "the two endpoints.\n\n"
            "Midpoint M of segment from A(x₁,y₁) to B(x₂,y₂):\n\n"
            "    M = ((x₁+x₂)/2,  (y₁+y₂)/2)\n\n"
            "Simply average the x-coordinates and average the y-coordinates.\n\n"
            "Think of it as: what's halfway between x₁ and x₂?\n"
            "The average: (x₁+x₂)/2."
        ),
        "formula": "M = ((x₁+x₂)/2, (y₁+y₂)/2)",
        "example": "Midpoint of A(2,4) and B(8,10):\n"
                   "M = ((2+8)/2, (4+10)/2)\n"
                   "  = (5, 7)",
    },
    {
        "title": "Gradient (Slope) of a Line",
        "body": (
            "The GRADIENT (or slope) measures how steep a line is.\n\n"
            "    m = (y₂ - y₁) / (x₂ - x₁)\n\n"
            "    m = rise / run\n\n"
            "Positive gradient: line goes up left to right\n"
            "Negative gradient: line goes down left to right\n"
            "Zero gradient: horizontal line\n"
            "Undefined gradient: vertical line\n\n"
            "Parallel lines have EQUAL gradients.\n"
            "Perpendicular lines: m₁ × m₂ = -1"
        ),
        "formula": "m = (y₂-y₁) / (x₂-x₁)",
        "example": "Gradient from A(1,2) to B(5,10):\n"
                   "m = (10-2)/(5-1) = 8/4 = 2",
    },
    {
        "title": "Equation of a Line",
        "body": (
            "The equation of a straight line:\n\n"
            "SLOPE-INTERCEPT FORM:\n"
            "    y = mx + c\n"
            "    m = gradient, c = y-intercept (where line crosses y-axis)\n\n"
            "To write the equation given a point and gradient:\n"
            "1. Substitute the known point (x,y) and gradient m into y = mx + c\n"
            "2. Solve for c\n"
            "3. Write the full equation\n\n"
            "Given two points: find m first, then use y = mx + c."
        ),
        "formula": "y = mx + c",
        "example": "Line through (2,5) with gradient 3:\n"
                   "5 = 3(2) + c\n"
                   "5 = 6 + c\n"
                   "c = -1\n"
                   "Equation: y = 3x - 1",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "Find the distance between A(1, 1) and B(4, 5).",
        "steps": [
            ("Write the distance formula",
             "d = √[(x₂-x₁)² + (y₂-y₁)²]"),
            ("Substitute coordinates",
             "d = √[(4-1)² + (5-1)²]"),
            ("Calculate differences and square",
             "d = √[3² + 4²] = √[9 + 16]"),
            ("Simplify",
             "d = √25 = 5"),
        ],
        "check": "3-4-5 is a Pythagorean triple ✓",
        "notes": "Recognising Pythagorean triples saves time.",
    },
    {
        "problem": "Find the midpoint of the segment from P(3, 7) to Q(9, 1).",
        "steps": [
            ("Write the midpoint formula",
             "M = ((x₁+x₂)/2, (y₁+y₂)/2)"),
            ("Substitute",
             "M = ((3+9)/2, (7+1)/2)"),
            ("Calculate",
             "M = (12/2, 8/2)"),
            ("Simplify",
             "M = (6, 4)"),
        ],
        "check": "Is (6,4) halfway? P to M: √[(6-3)²+(4-7)²]=√18. M to Q: √[(9-6)²+(1-4)²]=√18 ✓",
        "notes": "Just average the coordinates separately.",
    },
    {
        "problem": "Find the gradient of the line through A(2, 3) and B(6, 11).",
        "steps": [
            ("Write the gradient formula",
             "m = (y₂-y₁) / (x₂-x₁)"),
            ("Substitute",
             "m = (11-3) / (6-2)"),
            ("Calculate",
             "m = 8 / 4 = 2"),
        ],
        "check": "Rise = 8, Run = 4. For every 1 right, go 2 up. Check: 3+2(2)=7≠11... let's check: from x=2 to x=6 is 4, so rise=4×2=8. 3+8=11 ✓",
        "notes": "Always subtract in the same order: (y₂-y₁) with point 2 first, (x₂-x₁) with point 2 first.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Subtracting coordinates in different orders",
        "example": "m = (y₂-y₁)/(x₁-x₂) — mixing the order",
        "fix":     "Be consistent: always (y₂-y₁)/(x₂-x₁). Pick one point as '1' and stick with it.",
    },
    {
        "mistake": "Forgetting to square before adding in distance formula",
        "example": "d = √[(x₂-x₁) + (y₂-y₁)] — missing the squares",
        "fix":     "Both differences MUST be squared: d = √[(x₂-x₁)² + (y₂-y₁)²].",
    },
    {
        "mistake": "Using the wrong formula for midpoint",
        "example": "M = (x₂-x₁, y₂-y₁) — that's a displacement, not a midpoint",
        "fix":     "Midpoint = AVERAGE: add coordinates and divide by 2.",
    },
    {
        "mistake": "Confusing gradient with y-intercept in y = mx + c",
        "example": "For y = 3x + 5, saying gradient is 5 and y-intercept is 3",
        "fix":     "In y = mx + c: m is the gradient (coefficient of x) and c is the y-intercept.",
    },
]

KEY_VOCABULARY = {
    "Coordinate Plane": "A grid formed by a horizontal x-axis and vertical y-axis meeting at the origin.",
    "Origin":           "The point (0,0) where the x and y axes intersect.",
    "Ordered Pair":     "A point written as (x,y). The x always comes first.",
    "Gradient/Slope":   "Measure of steepness: m = rise/run = (y₂-y₁)/(x₂-x₁).",
    "y-intercept":      "Where the line crosses the y-axis (x=0). The 'c' in y=mx+c.",
    "Distance Formula": "d = √[(x₂-x₁)²+(y₂-y₁)²]. Uses the Pythagorean theorem.",
    "Midpoint Formula": "M = ((x₁+x₂)/2, (y₁+y₂)/2). Average of each coordinate.",
    "Parallel Lines":   "Lines with equal gradients that never meet.",
    "Perpendicular":    "Lines that meet at 90°. Their gradients multiply to give -1.",
    "Collinear":        "Three or more points that lie on the same straight line.",
}