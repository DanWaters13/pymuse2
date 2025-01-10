import os

def count_lines_in_file(file_path):
    """Counts the lines in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def main():
    # Define the target files and directories
    files_and_dirs = [
        "main.py",
        "src/core",
        "src/tests"
    ]

    total_lines = 0

    print("Counting lines of code in main.py and all .py files in src/core and src/tests...\n")
    for path in files_and_dirs:
        if os.path.isfile(path):
            # If it's a single file, count its lines
            lines = count_lines_in_file(path)
            total_lines += lines
            print(f"{lines} lines in {path}")
        elif os.path.isdir(path):
            # If it's a directory, count lines in all .py files
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        lines = count_lines_in_file(file_path)
                        total_lines += lines
                        print(f"{lines} lines in {file_path}")

    print("\n--------------------------------------")
    print(f"Total lines of code: {total_lines}")
    print("--------------------------------------")

if __name__ == "__main__":
    main()
