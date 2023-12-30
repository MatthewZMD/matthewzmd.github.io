#!/bin/python
import os
import fnmatch
import shutil
import sys

def get_jpg_files(dir_path):
    # Recursively search for JPG files in the given directory
    jpg_files = []
    for root, _, files in os.walk(dir_path):
        for filename in files:
            if fnmatch.fnmatch(filename.lower(), '*.jpg') or fnmatch.fnmatch(filename.lower(), '*.jpg'):
                jpg_files.append(os.path.join(root, filename))
    return jpg_files

def main(jpg_dir, raw_dir):
    # Get a list of JPG files in JPG directory
    jpg_files = get_jpg_files(jpg_dir)

    if not jpg_files:
        print("No JPG files found in JPG directory.")
        return

    # Iterate through each JPG file in JPG directory
    for file_a in jpg_files:
        # Extract the file name without extension
        jpg_filename_without_extension = os.path.splitext(os.path.basename(file_a))[0]

        # Check if a matching file exists in RAW directory
        matching_files_b = []
        for root, _, files in os.walk(raw_dir):
            for filename in files:
                if os.path.splitext(os.path.basename(filename))[0] in jpg_filename_without_extension and \
                   (filename.endswith("RAF") or filename.endswith("DNG") or filename.endswith("ARW")):
                    matching_files_b.append(os.path.join(root, filename))

        if matching_files_b:
            print(f"Matching files found in RAW directory for '{jpg_filename_without_extension}':")
            for idx, matching_file in enumerate(matching_files_b):
                print(f"{idx + 1}: {matching_file}")

            user_input = input("Do you want to copy any of these files? (Y/n): ").lower()

            if user_input.lower() == 'y' or user_input == '':
                if len(matching_files_b) == 1:
                    file_path_to_copy = matching_files_b[0]
                    file_to_copy = os.path.basename(file_path_to_copy)
                else:
                    file_idx_to_copy = int(input("Enter the index of the file to copy (1 to N): ") or 1) - 1
                    if 0 <= file_idx_to_copy < len(matching_files_b):
                        file_path_to_copy = matching_files_b[file_idx_to_copy]
                        file_to_copy = os.path.basename(file_path_to_copy)
                    else:
                        print("Invalid index.")
                # Create a subdirectory 'raw' in JPEG dir if it doesn't exist
                jpg_raw_dir = os.path.join(jpg_dir, 'raw')
                if not os.path.exists(jpg_raw_dir):
                    os.makedirs(jpg_raw_dir)
                destination_path = os.path.join(jpg_raw_dir, file_to_copy)
                shutil.copy2(file_path_to_copy, destination_path)
                print(f"File '{file_to_copy}' copied to JPG directory.")
        else:
            print(f"No matching files found in RAW directory for '{jpg_filename_without_extension}'.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: raw_copy.py JPEG_FOLDER RAW_FOLDER")
    main(sys.argv[1], sys.argv[2])
