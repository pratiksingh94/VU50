import numpy as np
import wave




def build_frame(text: str):
    payload = text.encode("ascii")
    
    if len(payload) > 255:
        raise ValueError(f"payload too long: {len(payload)} bytes (max 255)")
    
    length_byte = bytes([len(payload)])
    checksum = 0

    for b in payload:
        checksum ^= b
    
    checksum_byte = bytes([checksum])
    return length_byte + payload + checksum_byte




PREAMBLE_BIT_COUNT = 20
SYNC_BYTE = 0b01111110

def byte_to_bits(byte: int):
    return [(byte >> shift) & 1 for shift in range(7, -1, -1)]

def bytes_to_bits(data: bytes):
    bits = []
    for byte in data:
        bits.extend(byte_to_bits(byte))
    return bits


def build_preamble(bit_count: int = PREAMBLE_BIT_COUNT):
    return [i % 2 for i in range(bit_count)]


def build_bit_sequence(frame: bytes):
    preamble = build_preamble(PREAMBLE_BIT_COUNT)
    sync_bits = byte_to_bits(SYNC_BYTE)
    frame_bits = bytes_to_bits(frame)

    return preamble + sync_bits + frame_bits



SAMPLE_RATE = 44100
BUAD_RATE = 50
FREQ_ZERO = 1200
FREQ_ONE = 2200


def bits_to_audio(bits: list[int], sample_rate: int = SAMPLE_RATE, baud: int = BUAD_RATE):
    samples_per_bit = int(sample_rate / baud)
    t_bit = np.arange(samples_per_bit) / sample_rate

    tone_zero = np.sin(2 * np.pi * FREQ_ZERO * t_bit)
    tone_one = np.sin(2 * np.pi * FREQ_ONE * t_bit)

    chunks = [tone_one if bit else tone_zero for bit in bits]
    audio = np.concatenate(chunks).astype(np.float32)
    return audio



def save_wav(audio: "np.ndarray", path: str, sample_rate: int = SAMPLE_RATE):
    clipped = np.clip(audio, -1.0, 1.0)
    pcm = (clipped * 32767).astype(np.int16)

    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(pcm.tobytes())