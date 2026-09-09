# testing ground for now

from encoder import *
from decoder import *
import numpy as np
import wave

msg = "test meow meow"

frame = build_frame(msg)
bits = build_bit_sequence(frame)
audio = bits_to_audio(bits)

silence_before = np.zeros(int(0.41 * SAMPLE_RATE), dtype=np.float32)
silence_after = np.zeros(int(0.15 * SAMPLE_RATE), dtype=np.float32)
padded_audio = np.concatenate([silence_before, audio, silence_after])


save_wav(padded_audio, "mic_test.wav")

with wave.open("mic_recording.wav", "rb") as w:
    channels = w.getnchannels()
    sample_width = w.getsampwidth()
    sample_rate = w.getframerate()
    raw = w.readframes(w.getnframes())

audio_int16 = np.frombuffer(raw, dtype=np.int16)

if channels == 2:
    audio_int16 = audio_int16[::2]

audio = (audio_int16.astype(np.float32)) / 32768.0

# debug_audio(audio, 48000, BUAD_RATE)

result = decode(audio, SAMPLE_RATE, BUAD_RATE)
print(result)


# def apply_drift(audio, ratio):
#     n = len(audio)
#     new_length = int(n / ratio)
#     old_indicies = np.arange(n)
#     new_indicies = np.linspace(0, n - 1, new_length)
#     return np.interp(new_indicies, old_indicies, audio).astype(np.float32)


# drift_ppm_levels = [0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

# # ratio = 1.002000
# # drifted = apply_drift(padded_audio, ratio)
# # debug_audio(drifted,SAMPLE_RATE, BUAD_RATE)


# print(f"{'drift_ppm':>10} | {'ratio':>10} | {'result':>40}")
# print("-" * 67)

# for ppm in drift_ppm_levels:
#     ratio = 1.0 + (ppm/1_000_000)
#     drifted_audio = apply_drift(padded_audio, ratio)

#     # if ppm == 1000:
#     #     save_wav(drifted_audio, "drifted.wav")
#     try:
#         result = decode(drifted_audio, SAMPLE_RATE, BUAD_RATE)
#         status = f"{result!r}" if result == msg else f"BAD {result!r}"
#     except ValueError as e:
#         status = f"FAILED {e}"
    
#     print(f"{ppm:>10} | {ratio:>10.6f} | {status}")

