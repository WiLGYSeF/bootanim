from bootanim_base import (
    PART_TYPE_COMPLETE,
    PART_TYPE_FADE,
    PART_TYPE_PARTIAL,
    BootAnimationError
)

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

        if self.part_type not in (PART_TYPE_COMPLETE, PART_TYPE_PARTIAL, PART_TYPE_FADE):
            raise BootAnimationError('invalid animation part type')
        if self.loop < 0:
            raise BootAnimationError('invalid loop number')
        if self.next_delay < 0:
            raise BootAnimationError('invalid delay value')
        if len(self.name) == 0:
            raise BootAnimationError('invalid name')

        if len(self.bg_color) != 6:
            raise BootAnimationError('invalid background color')
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
        result = '%s %d %d %s' % (
            self.part_type,
            self.loop,
            self.next_delay,
            self.name
        )

        if self.bg_color != '000000':
            result += ' ' + self.bg_color
        return result
