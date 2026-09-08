import numpy as np

def goertzel_magnitude(samples: "np.ndarray", target_freq: float, sample_rate: int):
    n = len(samples)
    k = int(0.5 + (n * target_freq) / sample_rate)
    # where is my alpha 😔
    omega = (2 * np.pi * k) / n
    coeff = 2 * np.cos(omega)

    s_prev = 0.0
    s_prev2 = 0.0
    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    
    power = s_prev2 ** 2 + s_prev ** 2 - coeff + s_prev + s_prev2
    return float(np.sqrt(max(power, 0.0)))


FREQ_ZERO = 1200
FREQ_ONE = 2200

def audio_to_bits(audio: "np.ndarray", sample_rate: int, baud: int):
    samples_per_bit = int(sample_rate / baud)
    bits = []

    for start in range(0, len(audio) - samples_per_bit + 1, samples_per_bit):
        chunk = audio[start:start+samples_per_bit]
        mag_zero = goertzel_magnitude(chunk, FREQ_ZERO, sample_rate)
        mag_one = goertzel_magnitude(chunk, FREQ_ONE, sample_rate)

        bits.append(1 if mag_one > mag_zero else 0)
    
    return bits




PREAMBLE_BIT_COUNT = 20
SYNC_BITS = [0,1,1,1,1,1,1,0]

def find_sync_bit_index(bits: list[int]):
    n = len(SYNC_BITS)
    for i in range(len(bits) - n + 1):
        if bits[i : i + n] == SYNC_BITS:
            return i
    
    return None



def score_preamble(window: list[int], expected: list[int]):
    return sum(1 for a,b in zip(window, expected) if a==b)


def find_preamble_and_decode(audio: "np.ndarray", sample_rate: int, baud: int, preamble_bit_count: int = PREAMBLE_BIT_COUNT, sub_bit_search: int = 8, min_score_ratio: float = 0.9):
    samples_per_bit = int(sample_rate / baud)

    step = max(1, samples_per_bit // sub_bit_search)
    expected = [i % 2 for i in range(preamble_bit_count)]

    best_score = -1
    best_bits = None
    best_window_start = None

    for offset in range(0, samples_per_bit, step):
        bits = audio_to_bits(audio[offset:], sample_rate, baud)
        for start in range(0, len(bits)- preamble_bit_count+ 1):
            window = bits[start:start+preamble_bit_count]
            score = score_preamble(window, expected)

            if score > best_score:
                # print(score)
                best_score = score
                best_bits = bits
                best_window_start = start

    if best_bits is None or best_score < preamble_bit_count * min_score_ratio:
        return None
    
    sync_start = best_window_start + preamble_bit_count
    sync_candidate = best_bits[sync_start:sync_start+len(SYNC_BITS)]
    
    if sync_candidate != SYNC_BITS:
        nearby = best_bits[max(0, sync_start -4 ):sync_start + 12]
        idx = find_sync_bit_index(nearby)
        if idx is None:
            return None

        sync_start = max(0, sync_start - 4) + idx

    data_start = sync_start + len(SYNC_BITS)
    return best_bits[data_start:]