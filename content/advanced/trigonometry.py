# =============================================================================
# content/advanced/trigonometry.py
# All teaching content for the Trigonometry topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Trigonometry"

TOPIC_INTRO = (
    "Trigonometry lets you find unknown sides and angles in right triangles. "
    "The SAT tests three primary ratios — sine, cosine, and tangent — using "
    "the mnemonic SOH-CAH-TOA. Once you know which ratio connects the "
    "sides you have to the side or angle you need, the calculation is straightforward."
)

CONCEPT_CARDS = [
    {
        "title": "SOH-CAH-TOA — The Three Trig Ratios",
        "body": (
            "In a right triangle, the three basic trig ratios relate a given "
            "acute angle θ to the sides of the triangle:\n\n"
            "  SOH:  sin θ = Opposite / Hypotenuse\n"
            "  CAH:  cos θ = Adjacent / Hypotenuse\n"
            "  TOA:  tan θ = Opposite / Adjacent\n\n"
            "The sides are always named RELATIVE to the angle θ:\n"
            "  Opposite — the side across from θ\n"
            "  Adjacent — the side next to θ (not the hypotenuse)\n"
            "  Hypotenuse — the longest side, always opposite the right angle"
        ),
        "formula": "sin θ = opp/hyp   cos θ = adj/hyp   tan θ = opp/adj",
        "example": "In a right triangle with θ = 30°, hypotenuse = 10:\n"
                   "opposite = 10 × sin 30° = 10 × 0.5 = 5\n"
                   "adjacent = 10 × cos 30° = 10 × 0.866 ≈ 8.66",
    },
    {
        "title": "Labelling the Sides of a Right Triangle",
        "body": (
            "Before you can use SOH-CAH-TOA, you must correctly label the sides "
            "with respect to the angle you are working with.\n\n"
            "Step 1 — Mark the right angle (90°).\n"
            "Step 2 — Mark the given angle θ.\n"
            "Step 3 — Label the sides:\n"
            "   • Hypotenuse: opposite the right angle (always the longest side)\n"
            "   • Opposite: directly across from θ\n"
            "   • Adjacent: next to θ (the non-hypotenuse side touching θ)\n\n"
            "WARNING: if you move θ to the other acute angle, Opposite and "
            "Adjacent swap — always re-label when the angle changes."
        ),
        "formula": None,
        "example": "Right triangle with angles 90°, 40°, 50°.\n"
                   "For θ = 40°:  opp = side across from 40°,  adj = side next to 40°\n"
                   "For θ = 50°:  opp = side across from 50°  (this was the adjacent before!)",
    },
    {
        "title": "Common Angle Values",
        "body": (
            "The SAT often uses 30°, 45°, and 60° because their trig values "
            "are exact fractions or simple radicals.\n\n"
            "  sin 30° = 0.5       cos 30° = √3/2 ≈ 0.866    tan 30° ≈ 0.577\n"
            "  sin 45° = √2/2 ≈ 0.707   cos 45° = √2/2 ≈ 0.707    tan 45° = 1\n"
            "  sin 60° = √3/2 ≈ 0.866   cos 60° = 0.5           tan 60° = √3 ≈ 1.732\n\n"
            "Memory trick for sine:\n"
            "  30° → √1/2 = 0.5\n"
            "  45° → √2/2 ≈ 0.707\n"
            "  60° → √3/2 ≈ 0.866\n"
            "Cosine values go in reverse order!"
        ),
        "formula": "sin 30°=0.5  sin 45°≈0.707  sin 60°≈0.866",
        "example": "A ladder at 60° reaches a wall. Ladder = 10 m.\n"
                   "Height = 10 × sin 60° = 10 × 0.866 = 8.66 m",
    },
    {
        "title": "Finding Missing Sides",
        "body": (
            "To find a missing side:\n\n"
            "1. Label the sides (opp, adj, hyp) relative to the given angle.\n"
            "2. Identify which two sides are involved (known + unknown).\n"
            "3. Select the ratio that uses those two sides (SOH, CAH, or TOA).\n"
            "4. Write the equation and solve for the unknown.\n\n"
            "If the unknown is on top:\n"
            "    unknown = known × trig ratio\n\n"
            "If the unknown is on the bottom:\n"
            "    unknown = known ÷ trig ratio"
        ),
        "formula": None,
        "example": "θ = 35°, adjacent = 12.  Find the opposite side.\n"
                   "tan 35° = opp / adj\n"
                   "opp = 12 × tan 35° = 12 × 0.700 = 8.40",
    },
    {
        "title": "Finding Missing Angles (Inverse Trig)",
        "body": (
            "If you know two sides and want the angle, use inverse trig functions:\n\n"
            "  θ = sin⁻¹(opp/hyp)\n"
            "  θ = cos⁻¹(adj/hyp)\n"
            "  θ = tan⁻¹(opp/adj)\n\n"
            "On a calculator, use the sin⁻¹, cos⁻¹, or tan⁻¹ buttons "
            "(also written arcsin, arccos, arctan).\n\n"
            "Important: always check that your calculator is in DEGREE mode, "
            "not radian mode, for the SAT."
        ),
        "formula": "θ = sin⁻¹(opp/hyp) = cos⁻¹(adj/hyp) = tan⁻¹(opp/adj)",
        "example": "opp = 6, hyp = 10\n"
                   "θ = sin⁻¹(6/10) = sin⁻¹(0.6) ≈ 36.87°",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "In a right triangle, the angle is 40° and the hypotenuse is 15. "
                   "Find the side opposite the 40° angle.",
        "steps": [
            ("Identify which sides are involved",
             "We have: hypotenuse = 15, angle = 40°.  Need: opposite side."),
            ("SOH uses opposite and hypotenuse — use sine",
             "sin 40° = opposite / hypotenuse"),
            ("Substitute known values",
             "sin 40° = opp / 15"),
            ("Multiply both sides by 15",
             "opp = 15 × sin 40°"),
            ("Calculate (sin 40° ≈ 0.6428)",
             "opp = 15 × 0.6428 ≈ 9.64"),
        ],
        "check": "sin 40° = 9.64/15 = 0.643 ≈ sin 40°  ✓",
        "notes": "When the unknown is in the numerator: unknown = denominator × ratio.",
    },
    {
        "problem": "A ramp rises 4 m over a horizontal distance of 10 m. "
                   "Find the angle of inclination.",
        "steps": [
            ("Identify the sides: opposite = 4 (rise), adjacent = 10 (run)",
             "We want the angle, and we have opp and adj."),
            ("TOA uses opposite and adjacent — use inverse tangent",
             "θ = tan⁻¹(opp / adj)"),
            ("Substitute values",
             "θ = tan⁻¹(4 / 10) = tan⁻¹(0.4)"),
            ("Calculate",
             "θ ≈ 21.8°"),
        ],
        "check": "tan 21.8° ≈ 0.4  and  0.4 = 4/10  ✓",
        "notes": "Inverse trig functions always give you the angle when you know two sides.",
    },
    {
        "problem": "In a right triangle with a 60° angle and adjacent side 7, find the hypotenuse.",
        "steps": [
            ("CAH uses adjacent and hypotenuse",
             "cos 60° = adjacent / hypotenuse"),
            ("Substitute (cos 60° = 0.5)",
             "0.5 = 7 / hyp"),
            ("Solve for hyp — multiply both sides by hyp, then divide by 0.5",
             "hyp = 7 / 0.5"),
            ("Calculate",
             "hyp = 14"),
        ],
        "check": "cos 60° = 7/14 = 0.5  ✓",
        "notes": "When the unknown is in the denominator, divide the known side by the trig ratio.",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Mislabelling Opposite and Adjacent",
        "example": "Using sin when tan is needed because opp/adj was accidentally used with hyp",
        "fix":     "Always re-label sides relative to the specific angle in the problem.",
    },
    {
        "mistake": "Using the wrong ratio",
        "example": "Using cos when you have opp and hyp (should use sin)",
        "fix":     "SOH=sin(opp/hyp), CAH=cos(adj/hyp), TOA=tan(opp/adj). Check which sides you have.",
    },
    {
        "mistake": "Calculator in radian mode instead of degree mode",
        "example": "sin(30) in radian mode ≈ −0.988 instead of 0.5",
        "fix":     "Always confirm your calculator is in degree mode before trig calculations.",
    },
    {
        "mistake": "Forgetting to use inverse trig when finding an angle",
        "example": "Writing θ = sin(0.5) instead of θ = sin⁻¹(0.5)",
        "fix":     "To find an angle from a ratio, use sin⁻¹, cos⁻¹, or tan⁻¹.",
    },
]

KEY_VOCABULARY = {
    "Sine":
        "sin θ = opposite ÷ hypotenuse (SOH).",
    "Cosine":
        "cos θ = adjacent ÷ hypotenuse (CAH).",
    "Tangent":
        "tan θ = opposite ÷ adjacent (TOA).",
    "Hypotenuse":
        "The longest side of a right triangle; always opposite the right angle.",
    "Opposite":
        "The side of a right triangle directly across from angle θ.",
    "Adjacent":
        "The side of a right triangle next to angle θ that is not the hypotenuse.",
    "SOH-CAH-TOA":
        "A mnemonic for the three trig ratios: Sine=Opp/Hyp, Cos=Adj/Hyp, Tan=Opp/Adj.",
    "Inverse Trig":
        "sin⁻¹, cos⁻¹, tan⁻¹ — used to find an angle when two sides are known.",
    "Right Triangle":
        "A triangle containing one 90° angle.",
    "Angle of Elevation/Depression":
        "The angle measured upward (elevation) or downward (depression) from horizontal.",
}
