def infer_parallel(set_key, print_run):

    if not set_key:
        return "Unknown"

    set_key = set_key.lower()

    # TOPPS CHROME EXAMPLE RULESET
    if "topps chrome" in set_key:

        if not print_run:
            return "Base Refractor"

        if print_run <= 199:
            return "Bronze"
        if print_run <= 150:
            return "Blue"
        if print_run <= 99:
            return "Green"
        if print_run <= 50:
            return "Gold"
        if print_run <= 25:
            return "Red"
        if print_run <= 10:
            return "Orange"
        if print_run <= 5:
            return "Black"
        if print_run == 1:
            return "Superfractor"

    return "Unknown"