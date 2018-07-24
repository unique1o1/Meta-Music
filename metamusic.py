#!/usr/bin/python3
import os
import sys
import json
import warnings
import argparse
from Metamusic import MetaMusic
from Metamusic.recognize import FileRecognizer
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Meta-Music: Audio Fingerprinting")
    parser.add_argument('-f', '--fingerprint', nargs=None,
                        help='Fingerprint files or files in a directory\n'
                        'Usages: \n'
                        '--fingerprint /path/to/directory \n'
                        '--fingerprint /path/to/file')
    parser.add_argument('-r', '--recognize', nargs=None,
                        help='Recognize what is songs\n'
                        'Usage: \n'
                        '--recognize path/to/file \n')
    parser.add_argument(
        '-l',
        '--limit',
        nargs='?',
        default=None,
        help='Number of seconds from the start of the music files to limit fingerprinting to.\n'
        'Usage: \n'
        '--limit number_of_seconds \n'
    )
    args = parser.parse_args()
    if not args.fingerprint and not args.recognize:
        parser.print_help()
        sys.exit(0)
    meta = MetaMusic(12 if args.limit is None else int(args.limit))
    if args.fingerprint:

        filepath = args.fingerprint
        if os.path.isdir(filepath):
            print("Fingerprinting all  files in the {} directory".format(
                os.path.basename(filepath)))
            meta.fingerprint_directory(filepath)
        else:
            print("Fingerprinting {}..!".format(
                os.path.basename(filepath)))
            meta.fingerprint_file(filepath)

    elif args.recognize:
        # Recognize audio source
        song = None
        source = args.recognize

        if os.path.isdir(source):
            print(
                "Please specify an file if you'd like to recognize the song")
            sys.exit(1)
        song = meta.recognize(FileRecognizer, source)  # to be used later
        print(song)

    sys.exit(0)
