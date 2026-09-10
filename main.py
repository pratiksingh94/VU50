# testing ground for now

from encoder import *
from decoder import *
import numpy as np
import wave

result = decode_wav_file("mic_recording.wav", BUAD_RATE)
print(result)