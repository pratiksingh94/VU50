# testing ground for now

from encoder import *
import numpy as np

msg = "test meow meow gesknhgerns ge gbnwenbg kjbewkg jb4ewkj gbkrgb klwbglbwnglble "
f = build_frame(msg)


bits = build_bit_sequence(f)
audio = bits_to_audio(bits)

expected_dur = len(bits) / BUAD_RATE
got_dur = len(audio) / SAMPLE_RATE

print("bit count", len(bits))
print("sample per bit:", SAMPLE_RATE // BUAD_RATE)
print("expected dur:", expected_dur)
print("got dur:", got_dur)

save_wav(audio, "test.wav")
print("saved test.wav")

# preamble = bits[:PREAMBLE_BIT_COUNT]
# sync = bits[PREAMBLE_BIT_COUNT:PREAMBLE_BIT_COUNT+8]
# data = bits[PREAMBLE_BIT_COUNT+8:]

# print("frame bytes:", len(f), "expected bits:", len(f)*8)
# print("total bits:", len(bits))
# print("preamble bits:", preamble)
# print("sync bits:", sync)
# print("data bits:", data)
# print("data bits matches frame bits count:", len(data) == len(f)*8)

sample_per_bit = SAMPLE_RATE // BUAD_RATE

def dominant_freq(segment):
    spectrum = np.abs(np.fft.rfft(segment))

    freqs = np.fft.rfftfreq(len(segment), 1/SAMPLE_RATE)
    return freqs[np.argmax(spectrum)]


bit0_seg = audio[0:sample_per_bit]
bit1_seg = audio[sample_per_bit:sample_per_bit*2]
print("preamble bit 0 = ", bits[0], "dominant freq = ", dominant_freq(bit0_seg))
print("preamble bit 1 = ", bits[1], "dominant freq = ", dominant_freq(bit1_seg))