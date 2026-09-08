# testing ground for now

from encoder import *
from decoder import *
import numpy as np

msg = "test meow meow gesknhgerns ge gbnwenbg kjbewkg jb4ewkj gbkrgb klwbglbwnglble "

f = build_frame(msg)
bits = build_bit_sequence(f)
audio = bits_to_audio(bits)
save_wav(audio, "test.wav")

sample_per_bit = SAMPLE_RATE // BUAD_RATE

silence_before = np.zeros(int(0.37 * SAMPLE_RATE), dtype=np.float32)
# silence_after = np.zeros(int(0.2 * SAMPLE_RATE), dtype=np.float32)
padded = np.concatenate([silence_before, audio])

step = max(1, sample_per_bit //  8)
expected = [i%2 for i in range(PREAMBLE_BIT_COUNT)]

best_score = -1
for offset in range(0, sample_per_bit, step):
    bits = audio_to_bits(padded[offset:], SAMPLE_RATE, BUAD_RATE)
    for start in range(0, len(bits) - PREAMBLE_BIT_COUNT + 1):
        score = score_preamble(bits[start:start+PREAMBLE_BIT_COUNT], expected)
        # print(score)
        if score > best_score:
            # print("better score:", score)
            best_score = score

print(f"best preamble match score:", best_score)
print(f"threshold:", PREAMBLE_BIT_COUNT * 0.9)

# recovered_frame = find_preamble_and_decode(padded, SAMPLE_RATE, BUAD_RATE)
# expected_frame = bits[PREAMBLE_BIT_COUNT+8:]

# if recovered_frame is None:
#     print("failed to recover frame bits")
# else:
#     print("expected frame bits", len(expected_frame))
#     print("recovered frame bits", len(recovered_frame))
#     match = np.array_equal(recovered_frame[:len(expected_frame)], expected_frame)
#     print(match)

# print("original bit count:", len(bits))
# print("recovered bit count:", len(recoverd_bits))

# if bits != recoverd_bits:
#     mismtach = [i for i, (a,b) in enumerate(zip(bits, recoverd_bits)) if a != b]
#     print("mismatch pos:", mismtach)


# def dominant_freq(segment):
#     spectrum = np.abs(np.fft.rfft(segment))

#     freqs = np.fft.rfftfreq(len(segment), 1/SAMPLE_RATE)
#     return freqs[np.argmax(spectrum)]


# bit0_seg = audio[0:sample_per_bit]
# bit1_seg = audio[sample_per_bit:sample_per_bit*2]

# print("SEGMENT 0")
# mag1200 = goertzel_magnitude(bit0_seg, FREQ_ZERO, SAMPLE_RATE)
# mag2200 = goertzel_magnitude(bit0_seg, FREQ_ONE, SAMPLE_RATE)
# print(f"magnitude at 1200 Hz: {mag1200}")
# print(f"magnitude at 2200 Hz: {mag2200}")

# print("SEGMENT 1")
# mag1200 = goertzel_magnitude(bit1_seg, FREQ_ZERO, SAMPLE_RATE)
# mag2200 = goertzel_magnitude(bit1_seg, FREQ_ONE, SAMPLE_RATE)
# print(f"magnitude at 1200 Hz: {mag1200}")
# print(f"magnitude at 2200 Hz: {mag2200}")