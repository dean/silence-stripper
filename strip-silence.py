#!/usr/bin/env python

from pydub import AudioSegment
from pydub.utils import db_to_float

import argparse
import os

# Let's load up the audio we need...
def main(target_dir, recursive=True):
    for f in os.listdir(target_dir):
        f = os.path.join(target_dir, f)
        if recursive and os.path.isdir(f):
            main(f)
            continue
        if not f.endswith('.mp3'):
            continue

        print('Working on: ' + f)
        song = AudioSegment.from_mp3(f)

        for x in range(2):
            # filter out the silence from the beginning/end
            for i, ms in enumerate(song):
                if ms.rms > 0:
                    song = song[i:]
                    break
            song = song[::-1]

        # save the result
        song.export(f, format="mp3")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Strips silence from songs ' +
                                     'the specified target directory.')
    parser.add_argument('-r', help='Recursively go through directories.',
                        action='store_true')
    parser.add_argument('--target-dir', help='Directory to strip silence from')
    args = parser.parse_args()
    if not args.target_dir:
        parser.print_help()
        raise Exception('Please provide a target directory.')
    main(args.target_dir, recursive=args.r)
