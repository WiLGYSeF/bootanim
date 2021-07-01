import os
import re
import sys

from PIL import Image

from bootanim_base import (
    PART_TYPE_COMPLETE,
    BootAnimationError
)

from animationpart import AnimationPart


DESC_FNAME = 'desc.txt'

class BootAnimation:
    def __init__(self, path):
        self.dimensions = (None, None)
        self.framerate = None

        self.parts = []

        if path is not None:
            self.load(path)

    def load(self, path):
        if not os.path.isdir(path):
            raise ValueError('path must be directory')

        self.load_dir(path)

        has_infinite_loop = False
        for part in self.parts:
            if part.loop == 0:
                if has_infinite_loop:
                    print(
                        'warn: boot animation has multiple infinite loops, but only the first will loop',
                        file=sys.stderr
                    )
                    break
                has_infinite_loop = True

    # https://github.com/aosp-mirror/platform_frameworks_base/blob/master/cmds/bootanimation/FORMAT.md
    def load_dir(self, path):
        with open(os.path.join(path, DESC_FNAME), 'r') as descfile:
            lines = descfile.readlines()
            match = re.fullmatch(r'(\d+) (\d+) (\d+)\r?\n', lines[0])
            if match is None:
                raise BootAnimationError('invalid first line of %s' % DESC_FNAME)

            width, height, fps = match.groups()
            self.dimensions = (int(width), int(height))
            self.framerate = int(fps)

            part_regex = re.compile(
                r'(?P<type>[cfp])'
                r' (?P<loop>\d+)'
                r' (?P<delay>\d+)'
                r' (?P<name>[^ ]+)'
                r'(?: (?P<fade>\d+))?'
                r'(?: #?(?P<bg>[0-9A-Fa-f]{6}))?'
                r'(?: (?P<clk1>(c|-?\d+))(?: (?P<clk2>(c|-?\d+)))?)?'
            )

            # TODO: handle fade, clock1, clock2

            for i in range(1, len(lines)):
                line = lines[i].rstrip()
                match = part_regex.fullmatch(line)
                if match is None:
                    raise BootAnimationError('invalid %s line: %s' % (DESC_FNAME, line))

                groups = match.groupdict()
                part = AnimationPart(**{
                    'part_type': groups['type'],
                    'loop': int(groups['loop']),
                    'next_delay': int(groups['delay']),
                    'name': groups['name'],
                    'bg_color': groups['bg'],
                    'path': os.path.join(path, groups['name'])
                })
                self.parts.append(part)

    def save_gif(self, fname, **kwargs):
        loop_limit = kwargs.get('loop_limit', 3)
        load_time = kwargs.get('load_time', 0)
        loop_forever = kwargs.get('loop_forever', False)
        verbose = kwargs.get('verbose', 0)

        # TODO: specify screen size

        if verbose > 0:
            print('creating %s ...' % fname)

        if loop_limit < 1:
            raise ValueError('loop_limit must be at least 1')

        partframes = {}
        frames = []
        time_taken = 0
        spf = 1 / self.framerate

        def is_done():
            return load_time > 0 and time_taken >= load_time

        for part in self.parts:
            if verbose > 0:
                print('  loading %s ...' % part.name)

            # TODO: handle bg_color
            if part.name not in partframes:
                partframes[part.name] = []
                for imgfname in sorted(os.listdir(part.path)):
                    imgpath = os.path.join(part.path, imgfname)
                    partframes[part.name].append(Image.open(imgpath))

            loopcount = part.loop
            if loopcount == 0:
                loopcount = loop_limit

            for _ in range(loopcount):
                for frame in partframes[part.name]:
                    frames.append(frame)
                    time_taken += spf

                    if part.part_type != PART_TYPE_COMPLETE and is_done():
                        # TODO: handle PART_TYPE_FADE
                        break
                # TODO: is this supposed to be here?
                if is_done():
                    break
            if is_done():
                break

            for _ in range(part.next_delay):
                frames.append(partframes[part.name][-1])
                time_taken += spf
            if is_done():
                break

        if verbose > 0:
            print('  writing gif...')

        frames[0].save(
            fname,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=1000 / self.framerate,
            loop=0 if loop_forever else 1
        )
