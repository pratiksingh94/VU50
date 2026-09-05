# VU50
my own little digital mode

> VU = country code of indian callsigns, 50 = decided baud rate

## specs
*(can change later! + will be more detailed in future)*
```
preamble: simple alternating tone
structure: [preamble][sync byte][1-byte length N][N payload bytes][1-byte checksum]
sample rate: 44100 Hz
```
