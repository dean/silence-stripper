#!/usr/bin/env python

from pydub import AudioSegment
from pydub.utils import db_to_float

import argparse
import asyncio
import os


# Let's load up the audio we need...
def get_files(target_dir, recursive=True):
    paths = []
    for f in os.listdir(target_dir):
        f = os.path.join(target_dir, f)
        if recursive and os.path.isdir(f):
            paths.extend(get_files(f))
            continue
        if not f.endswith('.mp3'):
            continue
        paths.append(f)
    return paths


@asyncio.coroutine
def remove_silence(f):
    print('Working on: ' + f)

    song = AudioSegment.from_mp3(f)
    before = len(song)

    for x in range(2):
        # filter out the silence from the beginning/end
        for i, ms in enumerate(song):
            if ms.rms > 0:
                song = song[i:]
                break
        song = song[::-1]

    # Check to see if song length changed. (Did we remove silence?)
    after = len(song)
    if before == after:
        print(f + ' was unaltered.')
        return

    # save the result
    song.export(f + '.new', format="mp3")
    os.remove(f)
    os.rename(f + '.new', f)
    print('Finished: ' + f)


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

    tasks = asyncio.wait([remove_silence(f) for f in
                          get_files(args.target_dir, recursive=args.r)])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
