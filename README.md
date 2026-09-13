# VU50

A custom amateur digital radio mode built from scratch in python :3       
"VU" is India's amateur radio callsign prefix and "50" is the baud rate.

VU50 encodes text as audio-frequency FSK tones (the same thing modes like RTTY and PSK31 use), so a VU50 signal is, by construction radio-transmittable: play the generated `.wav` into a radio's mic input to transmit it irl, or feed a received audio recording into the decoder to recover the text.

## How it works

### Modulation

- **2-tone FSK** (Frequency Shift Keying): `1200 Hz` = bit `0`, `2200 Hz` = bit `1`
- **50 baud**: each bit is one tone lasting 1/50th of a second
- **44100 Hz**: sample rate, mono, 16-bit PCM `.wav` output

### Frame structure

```
[preamble: 20 alternating bits] [sync byte: 0111 1110]
[frame, padded to 40 bytes & repeated 3x] [trailing padding: 12 bits]
```

Each **frame** (before padding/repetition) is:

```
[1-byte length][N payload bytes][1-byte CRC-8]
```

- **Preamble** - a long alternating `0101...` pattern the decoder uses
  to lock onto bit timing before doing anythingg
- **Sync byte** (`0111 1110`) - marks where frame data begins
- **Length byte** - how many payload bytes follow
- **Payload** - the message in ASCII, max 38 bytes
- **CRC-8** - catches corruption in the payload
- **Fixed-size padding + 3x repetition** - the whole frame is
  zero-padded to a constant 40 bytes and transmitted three times. The
  decoder takes a per-bit majority vote across the three copies before
  parsing. This recovers the correct message even when *no single
  copy* was fully clean, as long as errors are scattered rather than
  hitting the same bit position in most copies (if that happens then idk)
- **Trailing padding** - a few extra alternating bits after the last
  copy, so nothing critical is the literal last thing transmitted
  before silence

### Decoding pipeline

```
raw audio
  -> preprocessing (DC offset removal, amplitude normalization)
  -> preamble detection
  -> sync byte detection
  -> majority vote across the 3 repeated frame copies
  -> bytes -> CRC-8 verification -> text
```

Tone detection uses the **Goertzel algorithm**: simpler than a full FFT when you only care about energy at two known frequencies :3

## Running it (locally)

```bash
pip install -r requirements.txt
python3 app.py
```

Then open `http://localhost:6767`. (sorry T_T)


## Known limitation: real mic recording

Sooo the intended validation method for "is this really radio-transmittable" was an simple loopback: play the generated signal through a speaker, record it back with a separate microphone (phone speaker → laptop mic), and decode the recording.     
This is meant to stand in for an actual radio's mic-in/speaker-out path, since i dont have an actual radio to test it.

still mic recordings surfaced shit ton of problems, most of which i found and fixed:

1. DC offset and inconsistent volume in recordings: fixed with preprocessing (DC removal + amplitude normalization,ez)
2. The XOR checksum blind spot: fixed by switching to CRC-8
3. Errors concentrated at the tail of transmissions (i GUESS room reverb): solved with trailing padding
4. Scattered errors throughout the message: fixed with the majority-vote error correction

AND STILL the damn mic-loopback test remains not working past that last fix, even though the encode/decode pipeline is solid (100% pass rate on direct file tests)

**This is planned future work for now, i have no idea how to fix this rn :(**
