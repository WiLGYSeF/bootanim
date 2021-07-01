import hashlib
import os
import random
import unittest

from bootanim_base import BootAnimationError
from bootanimation_class import BootAnimation


ANIMATIONS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'animations')
GIFS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gifs')

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

NAME = 'name'
ARGS = 'args'
RESULT = 'result'

SAVE_GIF = [
    {
        NAME: 'amatsuka-uto-wink',
        ARGS: [],
        RESULT: '96c91f3f986672eeb4a137454a73624680d05d3e3fa9fa0bd43b6a3e319a404a'
    },
    {
        NAME: 'amatsuka-uto-wink',
        ARGS: [1],
        RESULT: '06bcf49c27f5160d5c59fb1c66299f5eb849007d8a70b72c11dedcfb172da3b5'
    },
    {
        NAME: 'amatsuka-uto-wink',
        ARGS: [3, 4],
        RESULT: '9488ecbb5221301970fc803dd5a630243a5344ce4bf004b9bdd6bff19eaab7b9'
    }
]


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

    @unittest.skipIf(os.environ.get('SKIP_GIF', False), 'gif testing is slow')
    def test_save_gif(self):
        for entry in SAVE_GIF:
            anim = BootAnimation(os.path.join(ANIMATIONS_DIR, entry[NAME]))

            tmpfname = 'tmp%d.gif' % random.randint(0, 99)

            try:
                anim.save_gif(tmpfname, *entry[ARGS])
                self.assertEqual(sha256(tmpfname), entry[RESULT])
            finally:
                try:
                    os.remove(tmpfname)
                except:
                    pass

# https://stackoverflow.com/a/3431838
def sha256(fname):
    ohash = hashlib.sha256()
    with open(fname, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            ohash.update(chunk)
    return ohash.hexdigest()
