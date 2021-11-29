#Andy's windows sound implementation

#Andy's code, only works in Python 2

#!/usr/bin/python2

'''
Creates a simple waveform and plays it out the speakers.

Windows only.

Python2 only.
'''

import io, wave, winsound, math, struct

sampwidth = 2
framerate = 48000
tonefreq = 166

if sampwidth == 1:
	structfmt = '<b'
if sampwidth == 2:
	structfmt = '<h'
if sampwidth == 4:
	structfmt = '<i'

samples = b''

duration = 2
samplemix = 0.1

for t in range(0, duration * framerate):
    # here's where the magic happens
    sample = 0.0
    # sin wave
    sample += math.sin(2. * math.pi * tonefreq * t / framerate)
    # harmonic sin
    #sample += 0.2 * math.sin(1.1 + 1.5 * 2.0 * math.pi * tonefreq * t / framerate)
    # harmonic sin
    #sample += 0.2 * math.sin(math.pi + 3.04 * 2.0 * math.pi * tonefreq * t / framerate)
    # sawtooth wave
    #sample += 1.0 - 2 * ((1.5 * tonefreq * t / framerate)%2.0)
    # square wave
    #sample += 2*int((tonefreq * t / framerate)%2) - 1
    #print(sample)
    sample *= samplemix
    sample = max(sample, -0.99)
    sample = min(sample, 0.99)
    sample *= (1<<(sampwidth * 8) - 1) - 1
    sample = struct.pack(structfmt, int(sample))
    samples += sample

b1 = io.BytesIO()

w1 = wave.open(b1, 'wb')

w1.setnchannels(1)
w1.setsampwidth(sampwidth)
w1.setframerate(framerate)

w1.writeframes(samples)

w1.close()

b1.seek(0)

d1 = b1.read()

s1 = d1.decode('string_escape')

winsound.PlaySound(s1, winsound.SND_MEMORY)
