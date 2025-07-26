import base64
import sys
import os
import subprocess
import whisper
import json

def main():
    b64_input = sys.stdin.read().strip()

    with open("audio.opus", "wb") as f:
        f.write(base64.b64decode(b64_input))

    subprocess.run(
        ["ffmpeg", "-y", "-i", "audio.opus", "-ar", "16000", "-ac", "1", "converted.wav"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    model = whisper.load_model("base")
    result = model.transcribe("converted.wav", language="ru")

    print(json.dumps({"stt": result["text"].strip()}, ensure_ascii=False))

    os.remove("audio.opus")
    os.remove("converted.wav")

if __name__ == "__main__":
    main()
