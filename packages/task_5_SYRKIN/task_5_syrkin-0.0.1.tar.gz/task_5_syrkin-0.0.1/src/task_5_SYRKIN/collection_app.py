import argparse
from collections import Counter
from functools import lru_cache

ERROR_MSG_FILE_NOT_FOUND = "Error: The file '{}' does not exist"
ERROR_MSG_PERMISSION_DENIED = "Error: Permission denied for '{}'"


@lru_cache(maxsize=None)
def count_unique_characters(input_string: str) -> int:
    """Count the number of unique characters in the given string."""
    # Validate the input
    if not isinstance(input_string, str):
        raise TypeError(f"Expected a string, but got {type(input_string).__name__}")

    char_counter = Counter(input_string)
    unique_count = sum(1 for _, count in char_counter.items() if count == 1)
    return unique_count


def read_file(file_path: str) -> str:
    """Read the content of the file."""
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(ERROR_MSG_FILE_NOT_FOUND.format(file_path))
        return None
    except PermissionError:
        print(ERROR_MSG_PERMISSION_DENIED.format(file_path))
        return None


def process_arguments(args) -> None:
    """Process input arguments and execute the appropriate action."""
    if args.file:
        content = read_file(args.file)
        if content:
            unique_count = count_unique_characters(content)
            print(f"File '{args.file}' has {unique_count} unique characters.")
    elif args.string:
        unique_count = count_unique_characters(args.string)
        print(f"The string '{args.string}' has {unique_count} unique characters.")
    else:
        print("Error: Please provide either --string or --file as input.")


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Count unique characters in a string or a file.")
    parser.add_argument('--string', type=str, help="Input string to process")
    parser.add_argument('--file', type=str, help="Path to the file to process")
    args = parser.parse_args()
    process_arguments(args)


if __name__ == "__main__":
    main()
