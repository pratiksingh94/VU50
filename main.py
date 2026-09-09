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

rng = np.random.default_rng(67)
# noise_levels = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
noise_levels = [1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0]

print(f"{'noise_amp':>10} | {'SNR':>26} | {'result':<40}")
print("-" * 67)

for noise_amp in noise_levels:
    noise = rng.normal(0, noise_amp, size=padded_audio.shape).astype(np.float32)
    noisy_audio = padded_audio + noise
    snr_db = 20 * np.log10(1.0 /noise_amp) if noise_amp > 0 else float('inf')

    if noise_amp == 2.0:
        save_wav(noisy_audio, "hella_noisy2.0.wav")
    if noise_amp == 3.0:
        save_wav(noisy_audio, "hella_noisy3.0.wav")
    if noise_amp == 5.0:
        save_wav(noisy_audio, "hella_noisy5.0.wav")

    try:
        result = decode(noisy_audio, SAMPLE_RATE, BUAD_RATE)
        status = f"GUD {result!r}" if result == msg else f"BAD {result!r}"
    except ValueError as e:
        status = f"FAILED {e}"
    
    print(f"{noise_amp:>10.2f} | {snr_db:>23.1f}dB | {status}")

# save_wav(padded_audio, "padded_audio.wav")

# result = decode(padded_audio, SAMPLE_RATE, BUAD_RATE)
