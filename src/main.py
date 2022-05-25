def add(x: int, y: int) -> int:
    """
    Return the result of integer addition
    Parameters
    ----------
    x : int
        addition target2
    y : int
        addition target2
    Returns
    -------
    int
        Result of integer addition
    """
    return x + y


def main(name: str) -> int:
    """
    Standard-output Hello {name} and return length of name

    Parameters
    ----------
    name : str
        greeting target name

    Returns
    -------
    int
        length of greeting target name
    """

    print(f"Hello {name}")
    return len(name)


if __name__ == "__main__":

    name_length = main("Pyth")
    print(name_length)
