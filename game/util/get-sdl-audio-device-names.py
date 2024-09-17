#! /usr/bin/env -vS python

import pygame
import pygame._sdl2.audio as sdl2_audio
# import os
import time


# pygame.init()
# pygame.mixer.init()
# devices = tuple(sdl2_audio.get_audio_device_names())
# print(devices)


# RESULT:
# pygame-ce 2.5.0 (SDL 2.30.3, Python 3.12.4)
# Traceback (most recent call last):
#   File "/home/bilbo/repos/pygamefun/game/util/get-sdl-audio-device-names.py", line 8, in <module>
#     pygame.mixer.init()
# pygame.error: dsp: No such audio device

# This is not helpful. This test needs to init but if I could init I wouldn't be here. Chicken/egg problem.
# STILL LOOKING FOR A WAY TO CONFIRM THE DEVICE NAMES, THEN NEXT I CAN SEE ABOUT DRIVER INSTALLS/LIBS ETC.




# ***********************************************************
# ***********************************************************

# https://github.com/bastibe/SoundCard
# import soundcard as sc
# import numpy
#
# # get a list of all speakers:
# speakers = sc.all_speakers()
# # get the current default speaker on your system:
# default_speaker = sc.default_speaker()
#
#
# # get a list of all microphones:
# mics = sc.all_microphones()
# # get the current default microphone on your system:
# default_mic = sc.default_microphone()
#
#
# # record and play back one second of audio:
# data = default_mic.record(samplerate=48000, numframes=48000)
# # normalized playback
# default_speaker.play(data/numpy.max(numpy.abs(data)), samplerate=48000)


# *** TRYING TO USE THIS 'soundcard' LIBRARY YIELDED THE FOLLOWING ERRORS. AGAIN, TRYING TO FIND PULSE AUDIO LIBS.
# PulseAudio is Linux only, so the common failure here is all these libs are acting like they are on Linux and not
# finding or correctly callying the correct Windows libraries.
# Traceback (most recent call last):
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/soundcard/pulseaudio.py", line 17, in <module>
#     _pa = _ffi.dlopen('pulse')
#           ^^^^^^^^^^^^^^^^^^^^
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/cffi/api.py", line 150, in dlopen
#     lib, function_cache = _make_ffi_library(self, name, flags)
#                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/cffi/api.py", line 834, in _make_ffi_library
#     backendlib = _load_backend_lib(backend, libname, flags)
#                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/cffi/api.py", line 829, in _load_backend_lib
#     raise OSError(msg)
# OSError: ctypes.util.find_library() did not manage to locate a library called 'pulse'
#
# During handling of the above exception, another exception occurred:
#
# Traceback (most recent call last):
#   File "/home/bilbo/repos/pygamefun/game/util/get-sdl-audio-device-names.py", line 28, in <module>
#     import soundcard as sc
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/soundcard/__init__.py", line 4, in <module>
#     from soundcard.pulseaudio import *
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/soundcard/pulseaudio.py", line 20, in <module>
#     _pa = _ffi.dlopen('libpulse.so')
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/cffi/api.py", line 150, in dlopen
#     lib, function_cache = _make_ffi_library(self, name, flags)
#                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/cffi/api.py", line 834, in _make_ffi_library
#     backendlib = _load_backend_lib(backend, libname, flags)
#                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/cffi/api.py", line 829, in _load_backend_lib
#     raise OSError(msg)
# OSError: cannot load library 'libpulse.so': libpulse.so: cannot open shared object file: No such file or directory.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'libpulse.so'



# ***********************************************************
# ***********************************************************




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Trying module: sounddevice
# import sounddevice
#
# devs = sounddevice.query_devices()
# print(devs)  # Shows current output and input as well with "<" abd ">" tokens
#
# for dev in devs:
#     print(dev['name'])

# NOPE:
# OSError: PortAudio library not found
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -





# BELOW IS OLD STUFF - ABOVE IS NEW, SIMPLIFIED
#===========================================================================================================

# It appears this program cannot tell me the audio devices because of the same problem I am trying to solve:
# Cannot initialize pygame mixer, apparently because I have not specified the correct audio device, at the point of
#   attempted initialization.

# SIDENOTE: If you pass empty string for the driver, it defaults to trying to load pulseaudio libraries.
# It appears that pulseaudio is really ONLY a Linux thing. No support for any modern Windows.
# https://www.freedesktop.org/wiki/Software/PulseAudio/
# So we can ignore pulseaudio for our Windows goals. This just shows that default modes in SDL lean towards Linux.
# CURRENTLY: We simply cannot find a driver name that results in any progress. I've tried everything possible:
# '', dsp, ds, directsound, winmm, realtex, nvidia, NVIDIA, Realtek, Realtek(R) Audio, SAMSUNG, and many more.

# SOME ERRORS: Audio target 'XXXX' not available
# OTHERS: XXXX: No such audio device

# UNIQUE RESULT: 'ALSA', And some hints indicate this is what I might need to use on Windows.

# os.environ['SDL_AUDIODRIVER'] = 'dsp'

# print(sdl2_audio.SDL_GetCurrentAudioDriver())  # Wrong. Don't know where this function lives.

# devices = tuple(sdl2_audio.get_audio_device_names(True))  # TOO SOON. 'Audio system not initialized.' Chicken/Egg problem.
# print(devices)

# def get_devices(capture_devices: bool = False) -> tuple[str, ...]:
#     mixer_not_initialized = not pygame.mixer.get_init()  # This particular logic came from a posting. Not mine. It's a little weird, but that doesn't matter.
#     if mixer_not_initialized:
#         pygame.mixer.init()
#     devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
#     if mixer_not_initialized:
#         pygame.mixer.quit()
#     return devices

# print(get_devices(capture_devices=False))



# Similar problem affects this utility as affects my game - Cannot find audio driver?!?
# Below is run from console. Actually cannot run this from within PyCharm.

# (ve.pygamefun) bilbo@forest:~/repos/pygamefun/game/util$ ./get-sdl-audio-device-names.py
# split -S:  ‘ python\r’
#  into:    ‘python’
# executing: python
#    arg[0]= ‘python’
#    arg[1]= ‘./get-sdl-audio-device-names.py’
# pygame-ce 2.5.0 (SDL 2.30.3, Python 3.12.4)
# Traceback (most recent call last):
#   File "/home/bilbo/repos/pygamefun/game/util/./get-sdl-audio-device-names.py", line 15, in <module>
#     print(get_devices())
#           ^^^^^^^^^^^^^
#   File "/home/bilbo/repos/pygamefun/game/util/./get-sdl-audio-device-names.py", line 9, in get_devices
#     pygame.mixer.init()
# pygame.error: dsp: No such audio device


# List of SDL2 Audio Drivers:

# https://wiki.libsdl.org/SDL2/FAQUsingSDL



# pygame.error: Audio target 'winmm' not available


# 'ALSA' gives a unique result:
# pygame.error: Failed loading libasound.so.2: libasound.so.2: cannot open shared object file: No such file or directory
