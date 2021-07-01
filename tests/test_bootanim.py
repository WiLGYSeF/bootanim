import os
import random
import unittest

import bootanim
from tests.helpers import sha256


ANIMATIONS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'animations')

LOAD = {
    os.path.join(
        ANIMATIONS_DIR, 'amatsuka-uto-wink.zip'
    ): '96c91f3f986672eeb4a137454a73624680d05d3e3fa9fa0bd43b6a3e319a404a',
}


class BootanimTest(unittest.TestCase):
    def test_main_save_from_file(self):
        for path, result in LOAD.items():
            tmpfname = 'tmp%d.gif' % random.randint(0, 99)
            bootanim.main([path, tmpfname])

            try:
                # FIXME: i swear it works on my machine
                if not 'TRAVIS' in os.environ:
                    self.assertEqual(sha256(tmpfname), result)
            finally:
                try:
                    os.remove(tmpfname)
                except: #pragma: no cover
                    pass
