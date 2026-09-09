# testing ground for now

from encoder import *
from decoder import *
import numpy as np

msg = "test meow meow"

frame = build_frame(msg)
bits = build_bit_sequence(frame)
audio = bits_to_audio(bits)

silence_before = np.zeros(int(0.41 * SAMPLE_RATE), dtype=np.float32)
silence_after = np.zeros(int(0.15 * SAMPLE_RATE), dtype=np.float32)
padded_audio = np.concatenate([silence_before, audio, silence_after])

save_wav(padded_audio, "padded_audio.wav")

result = decode(padded_audio, SAMPLE_RATE, BUAD_RATE)

# debug_audio(padded_audio, SAMPLE_RATE, BUAD_RATE)

print("sent:", repr(msg))
print("recovered:", repr(result))
print(result == msg)