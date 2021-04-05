
def num(s):
    """
    Simple conversion method for turning a string into an int or float depending on value
    """
    try:
        val = int(s) if int(s) == float(s) else float(s)
    except ValueError:
        try:
            val = float(s)
        except ValueError:
            raise ValueError(f"{s} cannot be converted into a integer or float.")

    return val
