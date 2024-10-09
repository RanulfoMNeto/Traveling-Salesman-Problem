def nint(x):
    """Round a value to an integer.

    :param float x: Original value.
    :return: Rounded integer.
    :rtype: int
    """
    return int(x + 0.5)


def deltas(start, end):
    """Calculate the difference between corresponding elements of two sequences.

    :param list start: Starting values.
    :param list end: Ending values.
    :return: A generator with the differences.
    :rtype: generator
    """
    return (e - s for e, s in zip(end, start))
