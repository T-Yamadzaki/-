"""Simple CLI calculator."""


def get_number(prompt: str) -> float:
    """Prompt until a valid number is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number, try again.")


def get_operation() -> str:
    """Prompt until a valid operation is entered."""
    valid_ops = {"+", "-", "*", "/"}
    while True:
        op = input("Operation (+, -, *, /): ").strip()
        if op in valid_ops:
            return op
        print("Invalid operation, try again.")


def calculate(a: float, b: float, op: str) -> float:
    """Calculate result for two numbers and an operator."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b
    raise ValueError("Unsupported operation.")


def main() -> None:
    """Run the calculator loop."""
    print("Calculator. Type 'q' to quit.")
    while True:
        first = input("First number (or q to quit): ").strip().lower()
        if first == "q":
            break
        try:
            a = float(first)
        except ValueError:
            print("Invalid number, try again.")
            continue

        b = get_number("Second number: ")
        op = get_operation()
        try:
            result = calculate(a, b, op)
        except ZeroDivisionError as exc:
            print(exc)
            continue
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
