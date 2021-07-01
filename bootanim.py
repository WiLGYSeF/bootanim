#!/usr/bin/env python3

import argparse
import os
import sys
import tempfile
import zipfile

from bootanimation_class import BootAnimation


def main(args):
    parser = argparse.ArgumentParser(
        description='convert android boot animations to gif previews',
        usage='%(prog)s [options] INPUT_FILE_OR_DIR OUTPUT'
    )
    parser.add_argument('-v', '--verbose',
        action='count', default=0,
        help='verbose mode'
    )
    parser.add_argument('files',
        action='store', metavar='PATH', nargs=2
    )

    group = parser.add_argument_group('gif options')
    group.add_argument('--loop-limit',
        action='store', metavar='COUNT', type=int, default=3,
        help='set the loop count for a part meant to loop forever until boot (default 3)'
    )
    group.add_argument('--load-time',
        action='store', metavar='TIME', type=float, default=0,
        help='set a load time to simulate a phone finishing boot (seconds)'
    )
    group.add_argument('--loop-forever',
        action='store_true', default=False,
        help='the output gif will loop forever instead of just once'
    )

    argspace = parser.parse_args(args)

    in_path = argspace.files[0]
    tmpdname = None

    if not os.path.isdir(in_path):
        tmpdname = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(in_path, 'r') as zipf:
            zipf.extractall(tmpdname.name)
        in_path = tmpdname.name

    anim = BootAnimation(in_path)
    anim.save_gif(
        argspace.files[1],
        loop_limit=argspace.loop_limit,
        load_time=argspace.load_time,
        loop_forever=argspace.loop_forever,
        verbose=argspace.verbose
    )

    if tmpdname is not None:
        tmpdname.cleanup()

if __name__ == '__main__':
    main(sys.argv[1:])
