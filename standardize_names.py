
def standardizeColumnNames(s):
    s = s.lower().replace(" ", "_")
    s = s.replace("?", "")
    s = s.replace(":", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = s.replace("/", "")
    s = s.replace("-", "_")
    s = s.replace(",", "")
    s = s.replace(".", "")
    s = s.replace("°", "")
    s = s.replace("’", "")
    s = s.replace("‘", "")
    s = s.replace("”", "")
    s = s.replace(">", "plus")
    s = s.replace("<", "minus")
    s = s.replace("=", "equals")
    s = s.replace("+", "plus")
    s = s.replace("-", "minus")
    if s[0].isdigit():
        s = "num_" + s
    return s