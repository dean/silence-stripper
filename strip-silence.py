#!/usr/bin/env python

import argparse
from multiprocessing import Pool
import os

from pydub import AudioSegment
from pydub.utils import db_to_float


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


def remove_silence(f):
    song = AudioSegment.from_mp3(f)
    if song[0].rms != 0 and song[-1].rms != 0:
        return

    print('Working on: ' + f)
    for x in range(2):
        # filter out the silence from the beginning/end
        for i, ms in enumerate(song):
            if ms.rms > 0:
                song = song[i:]
                break
        song = song[::-1]

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

    with Pool(processes=10) as pool:
        files = get_files(args.target_dir, recursive=args.r)
        result = pool.map_async(remove_silence, files).get()
        print('Finished completely.')

