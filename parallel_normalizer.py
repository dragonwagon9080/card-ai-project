import re

# =========================
# NORMALIZATION MAP
# =========================

PARALLEL_MAP = {
    # BASE
    "base": "Base",

    # SILVER / PRIZM FAMILY
    "silver": "Silver",
    "silver prizm": "Silver",
    "prizm silver": "Silver",
    "refractor silver": "Silver",

    # GOLD FAMILY
    "gold": "Gold",
    "gold refractor": "Gold",
    "gold prizm": "Gold",
    "gold chrome": "Gold",

    # BLUE FAMILY
    "blue": "Blue",
    "blue refractor": "Blue",
    "blue prizm": "Blue",

    # RED FAMILY
    "red": "Red",
    "red refractor": "Red",
    "red prizm": "Red",

    # BRONZE FAMILY
    "bronze": "Bronze",

    # PLATINUM FAMILY
    "platinum": "Platinum",
    "platinum refractor": "Platinum",
    "superfractor": "Platinum",

    # OTHER COMMON ONES
    "green": "Green",
    "orange": "Orange",
    "purple": "Purple",
    "black": "Black",
    "mojo": "Mojo",
    "wave": "Wave",
    "atomic": "Atomic",
}


def normalize_parallel(raw_parallel: str):
    """
    Converts messy AI output into standardized parallel label.
    """

    if not raw_parallel:
        return None

    text = raw_parallel.lower().strip()

    # direct match
    if text in PARALLEL_MAP:
        return PARALLEL_MAP[text]

    # fuzzy keyword matching
    for key in PARALLEL_MAP:
        if key in text:
            return PARALLEL_MAP[key]

    return "Unknown"