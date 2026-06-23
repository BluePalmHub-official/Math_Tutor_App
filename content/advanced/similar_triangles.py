# =============================================================================
# content/advanced/similar_triangles.py
# All teaching content for the Similar Triangles topic (SAT Advanced).
# =============================================================================

TOPIC_TITLE = "Similar Triangles"

TOPIC_INTRO = (
    "Similar triangles have the same shape but not necessarily the same size. "
    "Their corresponding angles are equal and their corresponding sides are "
    "proportional. This proportionality is the key tool: once you know any "
    "side in one triangle and the scale factor between the triangles, you can "
    "find any unknown side in either triangle."
)

CONCEPT_CARDS = [
    {
        "title": "What Makes Triangles Similar?",
        "body": (
            "Two triangles are similar if they have the same three angle measures. "
            "Because the angles of any triangle always sum to 180°, you only need "
            "to know that two angles match — the third angle is forced to match as well.\n\n"
            "Three similarity criteria:\n"
            "  AA  — Angle-Angle: two angles of one triangle equal two angles of another.\n"
            "  SSS — Side-Side-Side: all three pairs of sides are proportional.\n"
            "  SAS — Side-Angle-Side: two pairs of proportional sides with the same included angle.\n\n"
            "The SAT almost exclusively uses AA similarity."
        ),
        "formula": "△ABC ~ △DEF means ∠A=∠D, ∠B=∠E, ∠C=∠F",
        "example": "If ∠A = 40° and ∠B = 60°, then ∠C = 80°.\n"
                   "Another triangle with ∠D = 40° and ∠E = 60° is similar.",
    },
    {
        "title": "AA Similarity — The Most Useful Criterion",
        "body": (
            "AA (Angle-Angle) is the fastest way to prove similarity: "
            "if two angles in one triangle equal two angles in another, "
            "the triangles are similar.\n\n"
            "On the SAT, you often use:\n"
            "  • Shared angles (a vertex angle appears in both triangles)\n"
            "  • Parallel lines creating equal corresponding or alternate angles\n"
            "  • Right angle + one shared acute angle\n\n"
            "Once you establish similarity, you can set up a proportion "
            "between corresponding sides."
        ),
        "formula": "If ∠A = ∠D and ∠B = ∠E  →  △ABC ~ △DEF",
        "example": "A tree casts a 12 m shadow. A 2 m pole casts a 3 m shadow.\n"
                   "Both objects and their shadows form similar right triangles.\n"
                   "Height/shadow = 2/3  →  tree height = 12 × (2/3) = 8 m",
    },
    {
        "title": "Corresponding Sides and Their Ratios",
        "body": (
            "When two triangles are similar, their sides correspond in a fixed order. "
            "The notation △ABC ~ △DEF tells you exactly which sides correspond:\n\n"
            "    AB corresponds to DE\n"
            "    BC corresponds to EF\n"
            "    AC corresponds to DF\n\n"
            "The ratio of any pair of corresponding sides is always the same "
            "— this ratio is called the scale factor.\n\n"
            "    AB/DE = BC/EF = AC/DF = k  (the scale factor)"
        ),
        "formula": "AB/DE = BC/EF = AC/DF",
        "example": "△ABC ~ △DEF with AB=6, DE=9, BC=4.\n"
                   "Scale factor: 6/9 = 2/3\n"
                   "EF = BC ÷ (2/3) = 4 × (3/2) = 6",
    },
    {
        "title": "Setting Up Proportions to Find Missing Sides",
        "body": (
            "The most common SAT question type: two similar triangles with some "
            "sides labelled and one side unknown.\n\n"
            "Method:\n"
            "1. Confirm the triangles are similar (AA or given).\n"
            "2. Identify which sides correspond to each other.\n"
            "3. Write the proportion:\n"
            "       known₁ / known₂ = unknown₁ / unknown₂\n"
            "4. Cross-multiply and solve.\n\n"
            "Always match sides in the SAME position (short to short, "
            "long to long) from each triangle."
        ),
        "formula": "a/b = c/x  →  x = b·c/a",
        "example": "△PQR ~ △STU.  PQ=5, ST=10, QR=8. Find TU.\n"
                   "5/10 = 8/TU  →  TU = (8×10)/5 = 16",
    },
    {
        "title": "Scale Factor and Its Uses",
        "body": (
            "The scale factor k is the ratio of any pair of corresponding sides:\n"
            "    k = large side / small side  (or small/large)\n\n"
            "Key relationships:\n"
            "  • Sides scale by factor k.\n"
            "  • Perimeters scale by factor k.\n"
            "  • Areas scale by factor k².\n\n"
            "SAT tip: if two similar triangles have a side-length ratio of 2:3, "
            "their areas are in ratio 4:9."
        ),
        "formula": "If sides ratio = k, then areas ratio = k²",
        "example": "Two similar triangles with sides 4 and 6.\n"
                   "Scale factor k = 6/4 = 1.5\n"
                   "Area ratio = 1.5² = 2.25  (larger area = 2.25× smaller area)",
    },
]

WORKED_EXAMPLES = [
    {
        "problem": "△ABC ~ △DEF.  AB = 8, DE = 12, BC = 6.  Find EF.",
        "steps": [
            ("The triangles are similar — write the proportion using corresponding sides",
             "AB/DE = BC/EF"),
            ("Substitute known values",
             "8/12 = 6/EF"),
            ("Cross-multiply",
             "8 × EF = 12 × 6 = 72"),
            ("Divide both sides by 8",
             "EF = 72 / 8 = 9"),
        ],
        "check": "Check ratio: AB/DE = 8/12 = 2/3.  BC/EF = 6/9 = 2/3.  ✓",
        "notes": "The proportion always uses the same ratio of sides across both triangles.",
    },
    {
        "problem": "A 1.5 m vertical stick casts a shadow 2 m long at the same time "
                   "that a building casts a shadow 30 m long. "
                   "How tall is the building?",
        "steps": [
            ("The stick and building form similar right triangles (same sun angle)",
             "height / shadow = constant for both"),
            ("Set up the proportion",
             "1.5 / 2 = h / 30"),
            ("Cross-multiply",
             "2h = 1.5 × 30 = 45"),
            ("Solve for h",
             "h = 45 / 2 = 22.5 m"),
        ],
        "check": "Check: 1.5/2 = 0.75  and  22.5/30 = 0.75  ✓",
        "notes": "Indirect measurement problems always use similar triangles formed by the sun angle.",
    },
    {
        "problem": "Two similar triangles have corresponding sides 5 and 8. "
                   "The smaller triangle has area 25 cm². "
                   "Find the area of the larger triangle.",
        "steps": [
            ("Find the scale factor",
             "k = 8/5 = 1.6"),
            ("Areas scale by k²",
             "k² = 1.6² = 2.56"),
            ("Larger area = smaller area × k²",
             "Area = 25 × 2.56 = 64 cm²"),
        ],
        "check": "Check ratio of areas: 64/25 = 2.56 = (8/5)²  ✓",
        "notes": "Sides scale linearly (×k) but areas scale quadratically (×k²).",
    },
]

COMMON_MISTAKES = [
    {
        "mistake": "Matching wrong corresponding sides",
        "example": "In △ABC ~ △DEF, comparing AB with EF instead of AB with DE",
        "fix":     "Use the order in the similarity statement: A↔D, B↔E, C↔F.",
    },
    {
        "mistake": "Using the wrong ratio direction",
        "example": "Writing large/small on one side but small/large on the other",
        "fix":     "Keep the same triangle on the same side of every fraction in the proportion.",
    },
    {
        "mistake": "Confusing side scale factor with area scale factor",
        "example": "If sides are 3:5, saying areas are also 3:5",
        "fix":     "Area scale factor = (side scale factor)². Sides 3:5 → areas 9:25.",
    },
    {
        "mistake": "Not confirming similarity before using the proportion",
        "example": "Assuming two triangles are similar because they 'look similar' in a diagram",
        "fix":     "Always state the criterion used (AA, SSS, or SAS) or verify angles are equal.",
    },
]

KEY_VOCABULARY = {
    "Similar Triangles":
        "Triangles with the same shape (equal angles) but not necessarily the same size.",
    "Corresponding Sides":
        "Sides in the same position across two similar triangles; they are proportional.",
    "Corresponding Angles":
        "Angles in the same position across two similar triangles; they are equal.",
    "Scale Factor":
        "The ratio of a side in one triangle to its corresponding side in the other triangle.",
    "AA Similarity":
        "Two triangles are similar if two pairs of angles are equal.",
    "Proportion":
        "An equation stating that two ratios are equal, e.g., a/b = c/d.",
    "Cross-Multiplication":
        "In a/b = c/d, multiply diagonally to get ad = bc.",
    "Ratio":
        "A comparison of two numbers by division.",
    "Indirect Measurement":
        "Using similar triangle properties to find lengths that are difficult to measure directly.",
    "Congruent Triangles":
        "Triangles that are identical in both shape and size (scale factor = 1).",
}
