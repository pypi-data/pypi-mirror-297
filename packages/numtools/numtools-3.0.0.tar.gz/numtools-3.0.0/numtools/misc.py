"""non classifiable tools"""

import numpy as np


def safe_isnan(value, extend_to_None=True):
    """
    Make np.isnan working on any type.

    >>> test = {False: False, "": False, None: True, 1: False, np.nan:True}
    >>> for test, exp in test.items():
    ...     assert safe_isnan(test) == exp

    None can be checked as `np.NaN` depending on `extend_to_None`:

    >>> safe_isnan(None, extend_to_None=False)
    False
    >>> safe_isnan(None, extend_to_None=True)  # default
    True
    >>> safe_isnan(""), safe_isnan(0)
    (False, False)
    """
    try:
        return np.isnan(value)
    except TypeError:
        if value is None and extend_to_None:
            return True
        return False


def replace_nan(value, default=None):
    """
    >>> replace_nan(5)
    5
    >>> replace_nan(np.nan)
    >>> replace_nan(np.nan, 0)
    0
    """
    if safe_isnan(value, extend_to_None=False):
        return default
    return value


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
