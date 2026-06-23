# =============================================================================
# content/advanced/solid_geometry.py
# All teaching content for the Solid Geometry topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Solid Geometry"

TOPIC_INTRO = (
    "Solid geometry covers three-dimensional shapes — prisms, cylinders, cones, "
    "spheres, and pyramids. The SAT provides the key formulas on the reference sheet, "
    "so success depends on identifying the correct formula and substituting accurately. "
    "Pay close attention to whether you are given the radius or the diameter."
)

CONCEPT_CARDS = [
    {
        "title": "Volume of Prisms and Rectangular Solids",
        "body": (
            "A prism has two identical flat bases connected by rectangular faces.\n\n"
            "Rectangular prism (box):\n"
            "    V = length × width × height  =  l × w × h\n\n"
            "General prism rule:\n"
            "    V = Area of base × height\n\n"
            "This rule works for ANY prism — triangular prisms, "
            "hexagonal prisms, etc. Just calculate the base area first.\n\n"
            "Surface Area of a rectangular prism:\n"
            "    SA = 2(lw + lh + wh)"
        ),
        "formula": "V = lwh   SA = 2(lw + lh + wh)",
        "example": "Box: l=5, w=4, h=3\n"
                   "V = 5×4×3 = 60 units³\n"
                   "SA = 2(20+15+12) = 2(47) = 94 units²",
    },
    {
        "title": "Volume of a Cylinder",
        "body": (
            "A cylinder has two circular bases of radius r and height h.\n\n"
            "    V = π r² h\n\n"
            "Think of it as: area of circular base (πr²) × height (h).\n\n"
            "Lateral Surface Area (curved side only):\n"
            "    LSA = 2πrh\n\n"
            "Total Surface Area (curved side + two circular ends):\n"
            "    TSA = 2πrh + 2πr²\n\n"
            "SAT watch-out: if the problem gives diameter, remember r = d/2."
        ),
        "formula": "V = πr²h",
        "example": "Cylinder: r=3, h=7\n"
                   "V = π × 9 × 7 = 63π ≈ 197.9 units³",
    },
    {
        "title": "Volume of a Cone",
        "body": (
            "A cone has a circular base and tapers to a point (apex).\n\n"
            "    V = (1/3) × π r² × h\n\n"
            "A cone has exactly one-third the volume of a cylinder with "
            "the same base radius and height. This fraction (1/3) is easy "
            "to forget — always include it.\n\n"
            "r = radius of the circular base\n"
            "h = perpendicular height (from base to apex — NOT the slant height)"
        ),
        "formula": "V = (1/3)πr²h",
        "example": "Cone: r=6, h=5\n"
                   "V = (1/3) × π × 36 × 5 = 60π ≈ 188.5 units³",
    },
    {
        "title": "Volume of a Sphere",
        "body": (
            "A sphere is a perfectly round solid — like a ball.\n\n"
            "    V = (4/3) × π × r³\n\n"
            "Two common errors:\n"
            "  1. Using diameter instead of radius — remember r = d/2.\n"
            "  2. Forgetting the (4/3) fraction.\n\n"
            "Surface Area of a sphere:\n"
            "    SA = 4πr²\n\n"
            "Memory trick: Sphere volume starts with 4 (in 4/3) and sphere "
            "surface area also starts with 4πr²."
        ),
        "formula": "V = (4/3)πr³   SA = 4πr²",
        "example": "Sphere: r=3\n"
                   "V = (4/3) × π × 27 = 36π ≈ 113.1 units³\n"
                   "SA = 4π × 9 = 36π ≈ 113.1 units²",
    },
    {
        "title": "Volume of a Pyramid",
        "body": (
            "A pyramid has a polygonal base and triangular faces meeting at an apex.\n\n"
            "    V = (1/3) × base area × height\n\n"
            "For a rectangular pyramid:\n"
            "    V = (1/3) × l × w × h\n\n"
            "Like the cone, a pyramid is (1/3) of the corresponding prism.\n\n"
            "Scale factor and volume:\n"
            "If all dimensions of a solid are scaled by a factor k, "
            "the volume scales by k³. This is a common SAT question type."
        ),
        "formula": "V = (1/3) × base area × h",
        "example": "Square pyramid: base 4×4, height 6\n"
                   "V = (1/3) × 16 × 6 = 32 units³",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "A cylinder has a diameter of 8 and a height of 10. "
                   "Find its volume in terms of π.",
        "steps": [
            ("Find the radius from the diameter",
             "r = diameter / 2 = 8 / 2 = 4"),
            ("Write the cylinder volume formula",
             "V = πr²h"),
            ("Substitute r = 4 and h = 10",
             "V = π × 4² × 10 = π × 16 × 10"),
            ("Simplify",
             "V = 160π"),
        ],
        "check": "160π ≈ 502.7 cubic units.",
        "notes": "Always convert diameter to radius before substituting.",
    },
    {
        "problem": "A cone has radius 5 and height 9. "
                   "Find its volume rounded to 2 decimal places. Use π = 3.14.",
        "steps": [
            ("Write the cone volume formula",
             "V = (1/3)πr²h"),
            ("Substitute r = 5, h = 9",
             "V = (1/3) × 3.14 × 25 × 9"),
            ("Calculate step by step",
             "= (1/3) × 3.14 × 225\n"
             "= (1/3) × 706.5"),
            ("Divide by 3",
             "V = 235.5 units³"),
        ],
        "check": "235.5 × 3 = 706.5 = 3.14 × 225  ✓",
        "notes": "Remember the 1/3 — cones hold one-third the volume of a same-sized cylinder.",
    },
    {
        "problem": "A rectangular prism has dimensions 6 × 4 × 3. "
                   "All dimensions are doubled. By what factor does the volume increase?",
        "steps": [
            ("Original volume",
             "V₁ = 6 × 4 × 3 = 72"),
            ("New dimensions: 12 × 8 × 6",
             "V₂ = 12 × 8 × 6 = 576"),
            ("Factor of increase",
             "576 / 72 = 8"),
            ("Verify using scale factor rule",
             "Scale factor = 2,  volume factor = 2³ = 8  ✓"),
        ],
        "check": "576/72 = 8  ✓",
        "notes": "When all dimensions are scaled by k, volume scales by k³ (not k).",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Using diameter instead of radius in volume formulas",
        "example": "Cylinder with diameter 10: writing V = π × 10² × h instead of π × 5² × h",
        "fix":     "Always halve the diameter first: r = diameter ÷ 2.",
    },
    {
        "mistake": "Forgetting the (1/3) factor for cones and pyramids",
        "example": "Cone volume = πr²h instead of (1/3)πr²h",
        "fix":     "Cones and pyramids are exactly 1/3 of their corresponding cylinder/prism.",
    },
    {
        "mistake": "Confusing surface area with volume",
        "example": "The question asks for volume but you calculate SA = 2(lw+lh+wh)",
        "fix":     "Volume is in cubic units (units³). Surface area is in square units (units²).",
    },
    {
        "mistake": "Thinking volume scales by k (not k³) when dimensions change",
        "example": "Doubling all sides → volume doubles (×2) instead of ×8 (= 2³)",
        "fix":     "Volume scales by the cube of the scale factor: if k=2, volume × 2³ = 8.",
    },
]

KEY_VOCABULARY = {
    "Volume":
        "The amount of 3D space a solid occupies, measured in cubic units.",
    "Surface Area":
        "The total area of all outer faces of a solid, measured in square units.",
    "Prism":
        "A 3D solid with two identical parallel bases; V = base area × height.",
    "Cylinder":
        "A prism with circular bases; V = πr²h.",
    "Cone":
        "A solid with a circular base tapering to a point; V = (1/3)πr²h.",
    "Sphere":
        "A perfectly round solid; V = (4/3)πr³.",
    "Pyramid":
        "A solid with a polygonal base tapering to an apex; V = (1/3) × base area × h.",
    "Radius":
        "The distance from the center to the edge of a circle or sphere.",
    "Diameter":
        "Twice the radius; d = 2r.",
    "Scale Factor":
        "When all dimensions of a solid are multiplied by k, volume is multiplied by k³.",
}
