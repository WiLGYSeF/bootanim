import os
import unittest

from bootanim_base import BootAnimationError
from bootanimation_class import BootAnimation


ANIMATIONS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'animations')

LOAD = {
    os.path.join(ANIMATIONS_DIR, 'amatsuka-uto-wink'): {
        'dimensions': (1080, 2280),
        'framerate': 30,
        'parts': [
            'c 3 0 part0',
            'p 0 0 part0'
        ]
    }
}


class BootAnimationTest(unittest.TestCase):
    def test_load(self):
        for path, result in LOAD.items():
            anim = BootAnimation(path)
            for vattr, expected in result.items():
                if vattr == 'parts':
                    for i in range(len(anim.parts)):
                        self.assertEqual(str(anim.parts[i]), expected[i])
                else:
                    self.assertEqual(getattr(anim, vattr), expected)
