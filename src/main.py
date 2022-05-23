def main(name: str) -> int:
    """
    Standard-output Hello {name} and return length of name

    Parameters
    ----------
    name: str
        greeting target name

    Returns
    -------
    length of name: int
        length of greeting target name
    """
    print(f"Hello {name}")
    return len(name)


if __name__ == "__main__":

    name_length = main("Python")
    print(name_length)
