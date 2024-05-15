#!/usr/bin/env python3

import os
import shutil
from datetime import datetime
import argparse

def get_creation_date(file_path):
    """
    Get the creation date of the file. Use st_ctime as a fallback for the creation date.
    """
    stat = os.stat(file_path)
    return datetime.fromtimestamp(stat.st_ctime)


def process_files(src_dir, dest_dir):
    """
    Recursively process files in the given directory.
    """
    for root, _, files in os.walk(src_dir):
        for file in files:
            file_path = os.path.join(root, file)
            creation_date = get_creation_date(file_path)
            formatted_date = creation_date.strftime("%Y-%m-%d")
            target_dir = os.path.join(dest_dir, formatted_date)
            os.makedirs(target_dir, exist_ok=True)
            target_file_path = os.path.join(target_dir, file)
            if not os.path.exists(target_file_path):
                shutil.copy(file_path, target_file_path)
                print(f"Copied {file} to {target_file_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_dir", help="Source directory")
    parser.add_argument("dest_dir", help="Destination directory")

    args = parser.parse_args()

    src_dir = args.src_dir
    dest_dir = args.dest_dir

    if not os.path.isdir(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        exit(1)

    os.makedirs(dest_dir, exist_ok=True)
    process_files(src_dir, dest_dir)
    print("Files have been processed and copied successfully.")

if __name__ == "__main__":
    main()
