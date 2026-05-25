def normalize_set(year, set_name, sport, brand):

    if not set_name:
        return None

    text = f"{year} {brand} {set_name} {sport}".lower()

    # normalize common variations
    text = text.replace("topps 3", "topps series 3")
    text = text.replace("topps three", "topps series 3")
    text = text.replace("topps chrome", "topps chrome")
    text = text.replace("panini prizm", "prizm")

    return text