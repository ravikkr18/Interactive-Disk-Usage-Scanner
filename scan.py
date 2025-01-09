import os

def get_size(path):
    """Calculate the total size of a directory or file."""
    total_size = 0
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
    elif os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    # Skip files that can't be accessed
                    pass
    return total_size

def human_readable_size(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def scan_directory(path):
    """Scan the given directory for disk usage."""
    results = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                item_size = get_size(item_path)
                results.append((item_path, item_size))
            except (PermissionError, FileNotFoundError):
                # Skip paths that can't be accessed
                continue
    except (PermissionError, FileNotFoundError):
        print(f"Permission denied or path not found: {path}")
        return []
    return sorted(results, key=lambda x: x[1], reverse=True)

def main():
    # Ask user for the root path
    root_path = input("Enter the root path to scan (default is '/'): ").strip()
    if not root_path:
        root_path = "/"

    while True:
        print(f"\nScanning directory: {root_path}")
        results = scan_directory(root_path)

        if not results:
            print("No accessible files or directories found.")
            break

        # Display top 10 files or directories
        print(f"\n{'#':<3} {'Path':<60} {'Size':>15}")
        print("-" * 80)
        for i, (path, size) in enumerate(results[:10], start=1):
            print(f"{i:<3} {path:<60} {human_readable_size(size):>15}")

        # Ask user to choose an option
        print("\nOptions:")
        print("Enter the number (1-10) to scan further.")
        print("Enter 'c' to specify a custom path.")
        print("Enter 'q' to quit.")
        choice = input("Your choice: ").strip()

        if choice.lower() == 'q':
            print("Exiting the program.")
            break

        if choice.lower() == 'c':
            custom_path = input("Enter the custom path to scan: ").strip()
            if os.path.exists(custom_path):
                root_path = custom_path
            else:
                print(f"Invalid path: {custom_path}")
            continue

        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(results[:10]):
                selected_path = results[choice_index][0]
                if os.path.isdir(selected_path):
                    root_path = selected_path
                else:
                    print(f"'{selected_path}' is a file. Scanning files further is not possible.")
            else:
                print("Invalid choice. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()
