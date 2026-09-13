FIXED_FRAME_BYTES = 40
REPEAT_COUNT = 3



def crc8(data: bytes, poly: int = 0x07, init: int = 0x00):
    crc = init
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    
    return crc