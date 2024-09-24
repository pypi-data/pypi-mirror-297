import argparse
from pathlib import Path

from src.pliers import combine_files

def main():
    parser = argparse.ArgumentParser(description="Combine multiple .cbz files into one.")
    parser.add_argument("cbz_dir", type=Path, help="Path to the folder containing .cbz files")
    parser.add_argument("volume_title", help="Title for the output .cbz file")
    parser.add_argument("series_title", help="Title of the manga series, only shows in the .xml file, but could be useful on some tablets")
    parser.add_argument("-m", help="Use this flag if you want to run the script for multiple directories at once. It runs the script for EVERY directory given in cbz_dir argument", action="store_true", required=False)
    args = parser.parse_args()
    print(args)
    combine_files(args.cbz_dir, args.volume_title, args.series_title, args.m)

if __name__ == "__main__":
    main()