import argparse
import io
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Remove raw files that haven't been edited.")
    parser.add_argument("-e", "--extension", dest="extensions", default=[".NEF", ".nef"], nargs="+", help="Raw file extension. Defaults to Nikon `.NEF` files.")
    parser.add_argument("path", help="Path of the directory to recursively traverse.")
    arguments = parser.parse_args(sys.argv[1:])

    # Figure out full paths
    arguments.path = os.path.abspath(arguments.path)
    arguments.extensions = { period(e) for e in arguments.extensions }

    to_remove = []

    # Iterate over all files in the directory structure
    for root, _, files in os.walk(arguments.path):
        if len(files) == 0:
            continue
        print("\nIn {}:".format(root))
        for file in files:
            name, extension = os.path.splitext(file)
            # For all RAW files, find any other file in the same directory whose name starts with the same characters
            # Usually an XMP sidecar, a PSD, DNG, TIF, etc.
            if extension in arguments.extensions:
                full = os.path.join(root, file)
                remove = True
                for f in files:
                    if f != file and f.startswith(name):
                        remove = False
                        print("> Skipping {} ({})".format(full, f))
                        break
                if remove:
                    print("> Removing {}".format(full))
                    to_remove.append(full)

    # Confirm with the user this is what they really want to do
    print("\n{} files to be removed".format(len(to_remove)))
    confirm = input("Do you wish to proceed? Type `proceed` to continue: ")
    if confirm != "proceed":
        print("Aborting")
        exit()

    # Actually remove the filess
    print("\nRemoving files")
    for file in to_remove:
        print("> Removing {}".format(file))
        os.remove(file)

# Add a period at the beginning of a file extension if there is none
def period(extension):
    if len(extension) != 0 and extension[0] != ".":
        extension = "." + extension
    return extension

if __name__ == '__main__':
    main()
