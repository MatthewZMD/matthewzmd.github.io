#!/bin/python

import os
import shutil
import argparse

def find_jpg_destination(dest_dir, raw_filename):
    """
    Recursively search for a .JPG file that matches the raw file name in the destination directory.
    """
    jpg_filename = os.path.splitext(raw_filename)[0] + '.jpg'
    for root, _, files in os.walk(dest_dir):
        for file in files:
            if file.lower() == jpg_filename.lower():
                return root
    return None

def process_files(src_dir, dest_dir):
    """
    Recursively process .ARW, .DNG, and .RAF files in the source directory.
    """
    raw_extensions = {'.arw', '.dng', '.raf'}
    for root, _, files in os.walk(src_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in raw_extensions:
                file_path = os.path.join(root, file)
                jpg_dest = find_jpg_destination(dest_dir, file)

                if jpg_dest and jpg_dest != root:
                    target_file_path = os.path.join(jpg_dest, file)
                    shutil.move(file_path, target_file_path)
                    print(f"Moved {file} to {target_file_path}")
                elif jpg_dest == root:
                    print(f"{file} is already in the same directory as its matching .JPG file.")
                else:
                    print(f"No matching .JPG file found for {file} in the destination directory.")

def main():
    parser = argparse.ArgumentParser(description="Move .ARW, .DNG, and .RAF files to the same directory as their matching .JPG files in the destination directory.")
    parser.add_argument("src_dir", help="Source directory containing raw files")
    parser.add_argument("dest_dir", help="Destination directory to search for matching .JPG files")

    args = parser.parse_args()

    src_dir = args.src_dir
    dest_dir = args.dest_dir

    if not os.path.isdir(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        exit(1)

    if not os.path.isdir(dest_dir):
        print(f"Destination directory '{dest_dir}' does not exist.")
        exit(1)

    process_files(src_dir, dest_dir)
    print("Processing completed.")

if __name__ == "__main__":
    main()
