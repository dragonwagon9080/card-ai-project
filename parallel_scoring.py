# =========================
# RARITY / VALUE SCORING
# =========================

PARALLEL_SCORE = {
    "Base": 1,
    "Bronze": 2,
    "Silver": 3,
    "Blue": 4,
    "Green": 5,
    "Red": 6,
    "Orange": 7,
    "Gold": 8,
    "Black": 9,
    "Mojo": 9,
    "Atomic": 9,
    "Wave": 9,
    "Purple": 10,
    "Platinum": 11,
    "Superfractor": 12,
    "Unknown": 0
}


def score_parallel(parallel: str):
    """
    Returns rarity/value score (higher = rarer / more desirable)
    """

    if not parallel:
        return 0

    return PARALLEL_SCORE.get(parallel, 0)