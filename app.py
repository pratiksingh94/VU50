from flask import Flask, request, send_file
import os
import tempfile
import io
import wave
import numpy as np


from encoder import build_frame, build_bit_sequence, bits_to_audio
from decoder import decode_wav_file

app = Flask(__name__)

@app.route("/test")
def test():
    return {"status": "ok"}



@app.route("/encode", methods=["POST"])
def encode():
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not text:
        return { "error": "missing text field" }, 400

    try:
        frame = build_frame(text)
        bits = build_bit_sequence(frame)
        audio = bits_to_audio(bits)

    except ValueError as e:
        return {"error": str(e)}, 400
    
    buf = io.BytesIO()

    clipped = np.clip(audio, -1.0, 1.0)
    pcm = (clipped * 32767).astype(np.int16)

    with wave.open(buf, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(pcm.tobytes())

    buf.seek(0)

    return send_file(buf, mimetype="audio/wav", as_attachment=True, download_name="VU50_message.wav")


@app.route("/decode", methods=["POST"])
def decode():
    if "audio" not in request.files:
        return { "error": "missing audio field" }, 400
    
    uploaded = request.files["audio"]

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        uploaded.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        text = decode_wav_file(tmp_path, baud=50)
        return { "text": text }
    except ValueError as e:
        return {"error": str(e)}, 422
    except Exception as e:
        return {"error": f"could not read audio file: {e}"}, 422
    finally:
        os.remove(tmp_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767)