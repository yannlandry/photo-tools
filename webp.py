import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Mass-convert PNG files to WebP")
    parser.add_argument("-q", "--quality", dest="quality", default="75", help="Quality to use on the WebP compressor")
    parser.add_argument("-o", "--output", dest="output", default=".", help="Output of converted file(s)")
    parser.add_argument("files", nargs="+", help="Path to scan for images to compress")
    arguments = parser.parse_args(sys.argv[1:])

    for file in arguments.files:
        name = ".".join(file.split(".")[:-1])
        webp = os.path.join(arguments.output, name + ".webp")
        print("Converting `{}` into `{}`".format(file, webp))
        process = subprocess.run(["cwebp", "-q", arguments.quality, "-preset", "photo", "-noalpha", file, "-o", webp], capture_output=True)
        if process.returncode == 0:
            print(">>> Succeeded")
        else:
            print(">>> Failed")
            print(">>> {}".format(process.stderr.decode("utf-8")), end="")

if __name__ == '__main__':
    main()
