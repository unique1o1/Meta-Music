
import os
import sys
import json
import warnings
import argparse


def initialize():


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Meta-Music: Audio Fingerprinting")
    parser.add_argument('-f', '--fingerprint', nargs='*',
                        help='Fingerprint files in a directory\n'
                        'Usages: \n'
                        '--fingerprint /path/to/directory extension\n'
                        '--fingerprint /path/to/directory')
    parser.add_argument('-r', '--recognize', nargs=2,
                        help='Recognize what is songs\n'
                        'Usage: \n'
                        '--recognize path/to/file \n')
    args = parser.parse_args()
    if not args.fingerprint and not args.recognize:
        parser.print_help()
        sys.exit(0)
    if args.fingerprint:
        # Fingerprint all files in a directory
        if len(args.fingerprint) == 2:
            directory = args.fingerprint[0]
            extension = args.fingerprint[1]
            print("Fingerprinting all .%s files in the %s directory"
                  % (extension, directory))
            meta.fingerprint_directory(directory, ['.'+extension])

        elif len(args.fingerprint) == 1:
            filepath = args.fingerprint[0]
            if os.path.isdir(filepath):
                print(
                    "Please specify an extension if you'd like to fingerprint a directory!")
                sys.exit(1)
            meta.fingerprint_file(filepath)

    elif args.recognize:
        # Recognize audio source
        song = None
        source = args.recognize[0]

        if os.path.isdir(source):
            print(
                "Please specify an file if you'd like to recognize the song")
            sys.exit(1)
        song = meta.recognize(FileRecognizer, opt_arg)
        print(song)

    sys.exit(0)
