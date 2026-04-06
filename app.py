from flask import Flask, jsonify, send_from_directory, render_template, request
import sounddevice as sd
import numpy as np
import wave
import os
import threading
from datetime import datetime
import whisper
import serial
import threading
import time

app = Flask(__name__)

SAMPLE_RATE = 44100
CHANNELS = 1
DTYPE = "int16"

is_recording = False
is_paused = False
audio_chunks = []
stream = None
lock = threading.Lock()
play_last_trigger = 0

RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

recordings_list = []
current_mode = "raw"   # "raw" or "transcribe"

# Load once at startup so you do not reload the model every transcription
# "base.en" is a reasonable prototype choice for English dictation
transcription_model = whisper.load_model("base.en")


def format_duration(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"


def format_display_name(dt):
    return dt.strftime("Recording on %B %d, %Y at %I:%M:%S %p")


def audio_callback(indata, frames, time, status):
    global audio_chunks, is_recording, is_paused

    if status:
        print("Audio status:", status)

    with lock:
        if is_recording and not is_paused:
            audio_chunks.append(indata.copy())

def start_recording():
    global is_recording, is_paused, audio_chunks, stream

    with lock:
        audio_chunks = []
        is_recording = True
        is_paused = False

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        callback=audio_callback
    )
    stream.start()
    print("Recording started.")


def transcribe_audio(filepath):
    try:
        result = transcription_model.transcribe(filepath)
        text = result.get("text", "").strip()
        return text
    except Exception as e:
        print("Transcription error:", e)
        return "[Transcription failed]"


def stop_recording():
    global is_recording, is_paused, stream, audio_chunks, recordings_list, current_mode

    with lock:
        is_recording = False
        is_paused = False

    if stream is not None:
        stream.stop()
        stream.close()
        stream = None

    if not audio_chunks:
        print("No audio recorded.")
        return None

    audio_data = np.concatenate(audio_chunks, axis=0)

    now = datetime.now()
    filename = now.strftime("recording_%Y%m%d_%H%M%S.wav")
    filepath = os.path.join(RECORDINGS_DIR, filename)

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(np.dtype(DTYPE).itemsize)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    duration_seconds = len(audio_data) / SAMPLE_RATE

    transcript = ""
    if current_mode == "transcribe":
        transcript = transcribe_audio(filepath)

    new_recording = {
        "filename": filename,
        "display_name": format_display_name(now),
        "duration": format_duration(duration_seconds),
        "transcript": transcript,
        "mode": current_mode
    }

    recordings_list.insert(0, new_recording)

    print(f"Recording saved to {filepath}")
    return new_recording

def serial_listener():
    port = "/dev/cu.wchusbserial59270092221"
    baud_rate = 115200

    while True:
        try:
            with serial.Serial(port, baud_rate, timeout=1) as ser:
                time.sleep(2)  # give ESP32 time after serial opens
                print("Listening to ESP32...")

                while True:
                    line = ser.readline().decode(errors="ignore").strip()

                    if not line:
                        continue

                    print("Received:", line)

                    if line == "R":
                        handle_record_toggle()
                    elif line == "P":
                        handle_pause_toggle()
                    elif line == "M":
                        handle_mode_toggle()
                    elif line == "D":
                        handle_delete_last()
                    elif line == "Y":
                        handle_play_last()

        except Exception as e:
            print("Serial error:", e)
            time.sleep(2)

def handle_record_toggle():
    global is_recording

    with lock:
        currently_recording = is_recording

    if not currently_recording:
        start_recording()
    else:
        stop_recording()

def handle_pause_toggle():
    global is_paused, is_recording

    with lock:
        if not is_recording:
            return
        is_paused = not is_paused

    if is_paused:
        print("Recording paused.")
    else:
        print("Recording resumed.")

def handle_mode_toggle():
    global current_mode, is_recording

    with lock:
        if is_recording:
            print("Cannot switch mode while recording")
            return

        current_mode = "transcribe" if current_mode == "raw" else "raw"

    print(f"Mode switched to {current_mode}")

def handle_delete_last():
    global recordings_list

    if not recordings_list:
        print("No recordings to delete")
        return

    last = recordings_list.pop(0)
    filepath = os.path.join(RECORDINGS_DIR, last["filename"])

    if os.path.exists(filepath):
        os.remove(filepath)

    print("Deleted last recording")

def handle_play_last():
    global play_last_trigger, recordings_list

    if not recordings_list:
        print("No recordings to play")
        return

    play_last_trigger += 1
    print("Play last recording triggered")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def get_status():
    if is_recording and is_paused:
        status = "Paused"
    elif is_recording:
        status = f"Recording ({current_mode} mode)"
    else:
        status = "Idle"

    return jsonify({
        "status": status,
        "recordings": recordings_list,
        "mode": current_mode,
        "play_last_trigger": play_last_trigger
    })

@app.route("/toggle_record", methods=["POST"])
def toggle_record():
    global is_recording

    with lock:
        currently_recording = is_recording

    if not currently_recording:
        start_recording()
        return jsonify({
            "status": f"Recording ({current_mode} mode)",
            "recordings": recordings_list,
            "mode": current_mode
        })
    else:
        saved_recording = stop_recording()
        if saved_recording:
            return jsonify({
                "status": f"Stopped ({current_mode} mode)",
                "recordings": recordings_list,
                "mode": current_mode
            })
        return jsonify({
            "status": "Stopped (no audio saved)",
            "recordings": recordings_list,
            "mode": current_mode
        })


@app.route("/toggle_pause", methods=["POST"])
def toggle_pause():
    global is_paused, is_recording

    with lock:
        if not is_recording:
            return jsonify({
                "status": "Idle",
                "recordings": recordings_list,
                "mode": current_mode
            })

        is_paused = not is_paused
        paused_now = is_paused

    if paused_now:
        print("Recording paused.")
        return jsonify({
            "status": "Paused",
            "recordings": recordings_list,
            "mode": current_mode
        })
    else:
        print("Recording resumed.")
        return jsonify({
            "status": f"Recording ({current_mode} mode)",
            "recordings": recordings_list,
            "mode": current_mode
        })


@app.route("/toggle_mode", methods=["POST"])
def toggle_mode():
    global current_mode, is_recording

    with lock:
        if is_recording:
            return jsonify({
                "status": "Cannot switch mode while recording",
                "recordings": recordings_list,
                "mode": current_mode
            })

        if current_mode == "raw":
            current_mode = "transcribe"
        else:
            current_mode = "raw"

    return jsonify({
        "status": f"Mode switched to {current_mode}",
        "recordings": recordings_list,
        "mode": current_mode
    })


@app.route("/delete_last", methods=["POST"])
def delete_last():
    global recordings_list

    if not recordings_list:
        return jsonify({
            "status": "No recordings to delete",
            "recordings": recordings_list,
            "mode": current_mode
        })

    last = recordings_list.pop(0)
    filepath = os.path.join(RECORDINGS_DIR, last["filename"])

    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted {filepath}")
    except Exception as e:
        print("Error deleting file:", e)

    return jsonify({
        "status": "Last recording deleted",
        "recordings": recordings_list,
        "mode": current_mode
    })


@app.route("/recordings", methods=["GET"])
def get_recordings():
    return jsonify({
        "recordings": recordings_list,
        "mode": current_mode
    })

@app.route("/rename_recording", methods=["POST"])
def rename_recording():
    global recordings_list

    data = request.get_json()
    filename = data.get("filename", "").strip()
    new_name = data.get("new_name", "").strip()

    if not filename or not new_name:
        return jsonify({
            "success": False,
            "message": "Missing filename or new name"
        }), 400

    for recording in recordings_list:
        if recording["filename"] == filename:
            recording["display_name"] = new_name
            return jsonify({
                "success": True,
                "recordings": recordings_list
            })

    return jsonify({
        "success": False,
        "message": "Recording not found"
    }), 404

@app.route("/download/<filename>")
def download_recording(filename):
    return send_from_directory(RECORDINGS_DIR, filename, as_attachment=True)


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(RECORDINGS_DIR, filename)


if __name__ == "__main__":
    threading.Thread(target=serial_listener, daemon=True).start()
    app.run(debug=False, port=5001)