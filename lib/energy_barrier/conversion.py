r"""
A selection of useful routines to convert quantities.
"""


def field_to_tesla(strength, unit):
    r"""
    Scale the unit to Tesla
    :param strength: the quanity.
    :param unit: the
    :return: field strength in Tesla
    """
    mu0 = 1.25663706E-6  # (m kg) / (s^2 A^2)
    if unit == "T":
        return strength
    elif unit == "mT":
        return strength * 1E-3
    elif unit == "uT":
        return strength * 1E-6
    elif unit == "nT":
        return strength * 1E-9
    elif unit == "A/m":
        return strength * mu0
    else:
        raise ValueError(f"Unknown unit '{unit}'")
