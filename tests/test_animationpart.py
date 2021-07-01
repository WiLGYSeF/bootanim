import unittest

from animationpart import AnimationPart


FROM_TUPLE = {
    ('c', 1, 0, 'part0'): {
        'part_type': 'c',
        'loop': 1,
        'next_delay': 0,
        'name': 'part0',
        'bg_color': '000000'
    },
    ('p', 0, 5, 'part1', 'ffa600'): {
        'part_type': 'p',
        'loop': 0,
        'next_delay': 5,
        'name': 'part1',
        'bg_color': 'ffa600'
    },
}

STR = {
    AnimationPart(**{
        'part_type': 'c',
        'loop': 1,
        'next_delay': 0,
        'name': 'part0',
        'bg_color': '000000'
    }): 'c 1 0 part0',
    AnimationPart(**{
        'part_type': 'p',
        'loop': 0,
        'next_delay': 5,
        'name': 'part1',
        'bg_color': 'ffa600'
    }): 'p 0 5 part1 ffa600'
}


class AnimationPartTest(unittest.TestCase):
    def test_from_tuple(self):
        for key, val in FROM_TUPLE.items():
            part = AnimationPart.from_tuple(key)
            for vattr, expected in val.items():
                self.assertEqual(getattr(part, vattr), expected)

    def test_str(self):
        for key, val in STR.items():
            self.assertEqual(str(key), val)
