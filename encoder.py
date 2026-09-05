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