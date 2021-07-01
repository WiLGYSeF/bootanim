#!/usr/bin/env python3

import os
import re


class BootAnimation:
    def __init__(self, path):
        self.dimensions = (None, None)
        self.framerate = None

        self.parts = []

        if path is not None:
            self.load(path)

    def load(self, path):
        if os.path.isdir(path):
            return self.load_dir(path)
        if not os.path.isfile(path):
            raise ValueError()

    def load_dir(self, path):
        with open(os.path.join(path, 'desc.txt'), 'r') as descfile:
            lines = descfile.readlines()
            match = re.fullmatch(r'(\d+) (\d+) (\d+)\r?\n', lines[0])
            if match is None:
                raise ValueError()

            width, height, fps = match.groups()
            self.dimensions = (width, height)
            self.framerate = fps

            # https://blog.justinbull.ca/making-a-custom-android-boot-animation/
            part_regex = re.compile(r'([cp]) (\d+) (\d+) ([^ ]+)(?: ([0-9A-Fa-f]{6}))?')

            for i in range(1, len(lines)):
                line = lines[i].rstrip()
                match = part_regex.fullmatch(line)
                if match is None:
                    raise ValueError()

                ptype, loop, next_delay, name, bg_color = match.groups()
                part = AnimationPart(**{
                    'part_type': ptype,
                    'loop': int(loop),
                    'next_delay': int(next_delay),
                    'name': name,
                    'bg_color': bg_color,
                    'path': os.path.join(path, name)
                })
                print(part)

class AnimationPart:
    def __init__(self, **kwargs):
        self.part_type = kwargs['part_type']
        self.loop = kwargs['loop']
        self.next_delay = kwargs['next_delay']
        self.name = kwargs['name']
        self.bg_color = kwargs.get('bg_color', '000000')

        self.path = kwargs.get('path')

        if self.part_type not in (PART_TYPE_COMPLETE, PART_TYPE_PARTIAL):
            raise ValueError()
        if self.loop < 0:
            raise ValueError()
        if self.next_delay < 0:
            raise ValueError()

        hexchars = set('0123456789ABCDEFabcdef')
        for char in self.bg_color:
            if char not in hexchars:
                raise ValueError()

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

#input_path = '../Amatsuka Uto Wink/bootanimation.zip'
input_path = '../Amatsuka Uto Wink/'
anim = BootAnimation(input_path)
