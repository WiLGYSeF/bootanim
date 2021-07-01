#!/usr/bin/env python3

import os
import re

from PIL import Image

DESC_FNAME = 'desc.txt'

class BootAnimation:
    def __init__(self, path):
        self.dimensions = (None, None)
        self.framerate = None

        self.parts = []

        if path is not None:
            self.load(path)

    def load(self, path):
        if os.path.isdir(path):
            self.load_dir(path)
        elif os.path.isfile(path):
            pass
        else:
            raise ValueError()

        # TODO: check multiple infinite loops

    # https://github.com/aosp-mirror/platform_frameworks_base/blob/master/cmds/bootanimation/FORMAT.md
    def load_dir(self, path):
        with open(os.path.join(path, DESC_FNAME), 'r') as descfile:
            lines = descfile.readlines()
            match = re.fullmatch(r'(\d+) (\d+) (\d+)\r?\n', lines[0])
            if match is None:
                raise BootAnimationError('invalid first line of %s' % DESC_FNAME)

            width, height, fps = match.groups()
            self.dimensions = (width, height)
            self.framerate = int(fps)

            part_regex = re.compile(r'([cp]) (\d+) (\d+) ([^ ]+)(?: ([0-9A-Fa-f]{6}))?')

            for i in range(1, len(lines)):
                line = lines[i].rstrip()
                match = part_regex.fullmatch(line)
                if match is None:
                    raise BootAnimationError('invalid %s line: %s' % (DESC_FNAME, line))

                ptype, loop, next_delay, name, bg_color = match.groups()
                part = AnimationPart(**{
                    'part_type': ptype,
                    'loop': int(loop),
                    'next_delay': int(next_delay),
                    'name': name,
                    'bg_color': bg_color,
                    'path': os.path.join(path, name)
                })
                self.parts.append(part)

    def save_gif(self, fname, loop_limit=3, load_time=0):
        if loop_limit < 1:
            raise ValueError()

        partframes = {}
        frames = []
        time_taken = 0
        spf = 1 / self.framerate

        for part in self.parts:
            if part.name not in partframes:
                partframes[part.name] = []
                for imgfname in os.listdir(part.path):
                    imgpath = os.path.join(part.path, imgfname)
                    partframes[part.name].append(Image.open(imgpath))

            loopcount = part.loop
            if loopcount == 0:
                loopcount = loop_limit

            for _ in range(loopcount):
                for frame in partframes[part.name]:
                    frames.append(frame)
                    time_taken += spf

                    if all((
                        part.part_type != PART_TYPE_COMPLETE,
                        load_time > 0 and time_taken >= load_time
                    )):
                        break

            if load_time > 0 and time_taken >= load_time:
                break

            for _ in range(part.next_delay):
                if load_time > 0 and time_taken >= load_time:
                    break
                frames.append(partframes[part.name][-1])
                time_taken += spf

            if load_time > 0 and time_taken >= load_time:
                break

        frames[0].save(
            fname,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=1000 / self.framerate,
            loop=1
        )

PART_TYPE_COMPLETE = 'c'
PART_TYPE_PARTIAL = 'p'

class AnimationPart:
    def __init__(self, **kwargs):
        self.part_type = kwargs['part_type']
        self.loop = kwargs['loop']
        self.next_delay = kwargs['next_delay']
        self.name = kwargs['name']
        self.bg_color = kwargs.get('bg_color')
        if self.bg_color is None:
            self.bg_color = '000000'

        self.path = kwargs.get('path')

        if self.part_type not in (PART_TYPE_COMPLETE, PART_TYPE_PARTIAL):
            raise BootAnimationError('invalid animation part type')
        if self.loop < 0:
            raise BootAnimationError('invalid loop number')
        if self.next_delay < 0:
            raise BootAnimationError('invalid delay value')

        hexchars = set('0123456789ABCDEFabcdef')
        for char in self.bg_color:
            if char not in hexchars:
                raise BootAnimationError('invalid background color')

    @staticmethod
    def from_tuple(tup):
        if len(tup) == 4:
            return AnimationPart(**{
                'part_type': tup[0],
                'loop': tup[1],
                'next_delay': tup[2],
                'name': tup[3]
            })
        return AnimationPart(**{
            'part_type': tup[0],
            'loop': tup[1],
            'next_delay': tup[2],
            'name': tup[3],
            'bg_color': tup[4]
        })

    def __str__(self):
        return '%s %d %d %s' % (
            self.part_type,
            self.loop,
            self.next_delay,
            self.name
        )

class BootAnimationError(Exception):
    pass

#input_path = '../Amatsuka Uto Wink/bootanimation.zip'
input_path = '../Amatsuka Uto Wink/'
anim = BootAnimation(input_path)
anim.save_gif('test.gif')
