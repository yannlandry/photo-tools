import argparse
import io
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Backup new and updated files from one place to another.")
    parser.add_argument("-s", "--source", dest="source", required=True, help="Source path to a file structure to recursively traverse.")
    parser.add_argument("-d", "--destination", dest="destination", required=True, help="Destination path where new/updated files should be copied.")
    arguments = parser.parse_args(sys.argv[1:])

    # Figure out full paths
    arguments.source = os.path.abspath(arguments.source)
    arguments.destination = os.path.abspath(arguments.destination)

    # Force specific path endings for source and destination
    if arguments.source[-1] != "/":
        arguments.source = arguments.source + "/"
    while arguments.destination[-1] == "/":
        arguments.destination = arguments.destination[:-1]

    # Build commands
    command = ["rsync", "--verbose", "--recursive", "--update", "--perms", "--owner", "--group", "--times", "--dry-run"]
    dry_run = command + [arguments.source, arguments.destination]
    wet_run = command[:-1] + [arguments.source, arguments.destination]

    # Safety
    if "--dry-run" not in dry_run:
        print("`--dry-run` not found in the dry run command, aborting.")
        exit()

    # Dry run
    print("Doing dry run:")
    print("\t" + " ".join(dry_run) + "\n")
    dry_run_result = run(dry_run)
    print("\nDry run returned with code {}".format(dry_run_result))

    # Safe confirmation
    confirm = input("Do you want to proceed with an actual run? Type `proceed` to continue: ")
    if confirm != "proceed":
        print("Aborting")
        exit()

    # Full run
    print("Doing full run:")
    print("\t" + " ".join(wet_run) + "\n")
    wet_run_result = run(wet_run)
    print("\nFull run returned with code {}".format(wet_run_result))

def run(arguments):
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
        print("> " + line, end="")
    return process.poll()

if __name__ == '__main__':
    main()
