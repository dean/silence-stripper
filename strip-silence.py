#!/usr/bin/env python

from pydub import AudioSegment
from pydub.utils import db_to_float

import argparse
import os
from queue import Queue
import threading


lock = threading.Lock()


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
    with lock:
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
        with lock:
            print(f + ' was unaltered.')
        return

    # save the result
    song.export(f + '.new', format="mp3")
    os.remove(f)
    os.rename(f + '.new', f)
    with lock:
        print('Finished: ' + f)


# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        f = q.get()
        remove_silence(f)
        q.task_done()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Strips silence from songs ' +
                                     'the specified target directory.')
    parser.add_argument('-r', help='Recursively go through directories.',
                        action='store_true')
    parser.add_argument('--target-dir', help='Directory to strip silence from')
    parser.add_argument('--threads', help='Number of threads to use',
                        default=5)
    args = parser.parse_args()
    if not args.target_dir:
        parser.print_help()
        raise Exception('Please provide a target directory.')

    q = Queue()
    for i in range(int(args.threads)):
        t = threading.Thread(target=worker)
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t.start()

    for f in get_files(args.target_dir, recursive=args.r):
        q.put(f)

    q.join()
