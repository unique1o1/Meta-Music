
import os
import sys
import json
import warnings
import argparse


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
                        '--recognize file path/to/file \n')
    args = parser.parse_args()
    if not args.fingerprint and not args.recognize:
        parser.print_help()
        sys.exit(0)
