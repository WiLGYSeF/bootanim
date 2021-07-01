#!/usr/bin/env python3

from bootanimation_class import BootAnimation


#input_path = '../Amatsuka Uto Wink/bootanimation.zip'
input_path = '../Amatsuka Uto Wink/'
anim = BootAnimation(input_path)
anim.save_gif('test.gif', load_time=10)
