from functions.get_file_content import get_file_content


def main():
    # Big lorem file – should be truncated and end with the truncation message
    lorem = get_file_content("calculator", "lorem.txt")
    print(len(lorem))
    print(lorem[-200:])  # just to see the end, not the whole thing

    # Regular files
    main_py = get_file_content("calculator", "main.py")
    print(main_py)

    calc_py = get_file_content("calculator", "pkg/calculator.py")
    print(calc_py)

    # Paths that should cause errors
    outside = get_file_content("calculator", "/bin/cat")
    print(outside)

    missing = get_file_content("calculator", "pkg/does_not_exist.py")
    print(missing)


if __name__ == "__main__":
    main()
