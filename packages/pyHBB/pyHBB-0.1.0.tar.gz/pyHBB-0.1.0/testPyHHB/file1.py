from huffpress.press.compress import compress


def greet1(name: str) -> str:
    long_str = "This is the start of a very long text"
    comp_long_str = compress(long_str)
    print(comp_long_str)

    return f"Hi {name}! I am from file1"