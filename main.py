# testing ground for now

from encoder import *


msg = "test meow meow"
f = build_frame(msg)

print("frame hex:", f.hex())

# print("sync bits:", byte_to_bits(SYNC_BYTE))

bits = build_bit_sequence(f)

preamble = bits[:PREAMBLE_BIT_COUNT]
sync = bits[PREAMBLE_BIT_COUNT:PREAMBLE_BIT_COUNT+8]
data = bits[PREAMBLE_BIT_COUNT+8:]

print("frame bytes:", len(f), "expected bits:", len(f)*8)
print("total bits:", len(bits))
print("preamble bits:", preamble)
print("sync bits:", sync)
print("data bits:", data)
print("data bits matches frame bits count:", len(data) == len(f)*8)