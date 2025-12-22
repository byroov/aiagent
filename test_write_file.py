from functions.write_file import write_file




def main(description, *args):
    print(f"\nTEST: {description}")
    try:
        result = write_file(*args)
        print("RESULT:", result)
    except Exception as e:
        print("ERROR:", type(e).__name__, "-", e)

if __name__ == "__main__":
    main(
        "Write file in base directory",
        "calculator",
        "lorem.txt",
        "wait, this isn't lorem ipsum"
    )

    main(
        "Write file in nested directory",
        "calculator",
        "pkg/morelorem.txt",
        "lorem ipsum dolor sit amet"
    )

    main(
        "Attempt to write absolute path (should fail)",
        "calculator",
        "/tmp/temp.txt",
        "this should not be allowed"
    )

