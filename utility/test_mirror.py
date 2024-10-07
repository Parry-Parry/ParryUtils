import os
import argparse

def mirror_structure(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        # Create corresponding directory in the target
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path)
        os.makedirs(target_path, exist_ok=True)

        # Create empty files with "test_" prefix
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                target_file = os.path.join(target_path, f"test_{file}")
                open(target_file, 'a').close()  # Create an empty file

        # Create __init__.py files in each directory
        init_file = os.path.join(target_path, "__init__.py")
        open(init_file, 'a').close()

def main():
    parser = argparse.ArgumentParser(description="Mirror directory structure with test_ prefixed files")
    parser.add_argument("source", help="Source directory to mirror")
    parser.add_argument("target", help="Target directory for mirrored structure")
    args = parser.parse_args()

    mirror_structure(args.source, args.target)
    print(f"Directory structure mirrored from {args.source} to {args.target}")

if __name__ == "__main__":
    main()