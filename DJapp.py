import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time
import os

root = tk.Tk()
root.title("DJ Mixer with Crossfader, Waveform, and BPM Sync")
root.configure(bg="#23252a")

# Globals for Decks
deck = [
    {"data": None, "sr": None, "pos": 0, "stream": None, "playing": False, "paused": False, "volume": 1.0, "tempo": 1.0, "file": None, "label": None},
    {"data": None, "sr": None, "pos": 0, "stream": None, "playing": False, "paused": False, "volume": 1.0, "tempo": 1.0, "file": None, "label": None}
]
crossfade = 0.5

def load_track(channel):
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac *.ogg *.mp3")])
    if not file_path:
        return
    data, sr = sf.read(file_path, dtype='float32')
    if data.ndim == 1:
        data = np.expand_dims(data, axis=1)
    deck[channel]["data"] = data
    deck[channel]["sr"] = sr
    deck[channel]["pos"] = 0
    deck[channel]["file"] = file_path
    deck[channel]["tempo"] = 1.0
    deck[channel]["label"].config(text=os.path.basename(file_path))
    stop_deck(channel)

def play_pause(channel):
    if deck[channel]["playing"]:
        deck[channel]["paused"] = True
        deck[channel]["playing"] = False
    else:
        if deck[channel]["data"] is not None:
            deck[channel]["paused"] = False
            deck[channel]["playing"] = True
            if deck[channel]["stream"] is None or not deck[channel]["stream"].active:
                threading.Thread(target=play_stream, args=(channel,), daemon=True).start()

def stop_deck(channel):
    deck[channel]["playing"] = False
    deck[channel]["paused"] = False
    deck[channel]["pos"] = 0
    if deck[channel]["stream"] is not None:
        deck[channel]["stream"].stop()
        deck[channel]["stream"].close()
        deck[channel]["stream"] = None

def set_volume(channel, value):
    deck[channel]["volume"] = float(value)

def set_crossfade(value):
    global crossfade
    crossfade = float(value)
    # Optionally, adjust deck volumes here for crossfade effect

def set_tempo(channel, value):
    deck[channel]["tempo"] = 2 ** (float(value) / 100)  # -100 to 100 -> 0.5x to 2x

def play_stream(channel):
    d = deck[channel]
    blocksize = 1024
    def callback(outdata, frames, time_info, status):
        if not d["playing"] or d["data"] is None:
            outdata[:] = np.zeros((frames, d["data"].shape[1]))
            return
        start = int(d["pos"])
        step = d["tempo"]
        idxs = (start + np.arange(frames) * step).astype(int)
        idxs = np.clip(idxs, 0, len(d["data"]) - 1)
        out = d["data"][idxs] * d["volume"]
        # Apply crossfade
        if channel == 0:
            out *= (1.0 - crossfade)
        else:
            out *= crossfade
        outdata[:,:] = out
        d["pos"] += frames * step
        if d["pos"] >= len(d["data"]):
            d["playing"] = False
    d["stream"] = sd.OutputStream(
        samplerate=d["sr"],
        channels=d["data"].shape[1],
        blocksize=blocksize,
        callback=callback
    )
    d["stream"].start()
    while d["playing"]:
        if d["paused"]:
            time.sleep(0.05)
        else:
            time.sleep(0.05)
    d["stream"].stop()
    d["stream"].close()
    d["stream"] = None

# --- Top Bar ---
top_frame = tk.Frame(root, bg="#23252a")
top_frame.pack(fill="x", pady=10)
tk.Button(top_frame, text="+", bg="#333", fg="white", font=("Arial", 16), width=2, relief="flat", command=lambda: load_track(0)).pack(side="left", padx=10)
label_a = tk.Label(top_frame, text="DJ FREE", bg="#23252a", fg="#888", font=("Arial", 18, "bold"))
label_a.pack(side="left", expand=True)
deck[0]["label"] = label_a
label_b = tk.Label(top_frame, text="DJ FREE", bg="#23252a", fg="#888", font=("Arial", 18, "bold"))
label_b.pack(side="right", expand=True)
deck[1]["label"] = label_b
tk.Button(top_frame, text="+", bg="#333", fg="white", font=("Arial", 16), width=2, relief="flat", command=lambda: load_track(1)).pack(side="right", padx=10)

# --- Decks Frame ---
decks_frame = tk.Frame(root, bg="#23252a")
decks_frame.pack(fill="both", expand=True, padx=20, pady=10)

# --- Left Deck ---
left_deck = tk.Frame(decks_frame, bg="#23252a")
left_deck.pack(side="left", expand=True, fill="both", padx=10)
tempo_a = tk.Scale(left_deck, from_=-100, to=100, orient="vertical", length=200, bg="#23252a", fg="white", troughcolor="#444", highlightthickness=0, label="TEMPO", command=lambda v: set_tempo(0, v))
tempo_a.set(0)
tempo_a.pack(side="left", padx=10)
tk.Button(left_deck, text="CUE", width=6, bg="#444", fg="white", command=lambda: stop_deck(0)).pack(pady=5)
tk.Button(left_deck, text="▶", width=6, bg="#444", fg="white", command=lambda: play_pause(0)).pack(pady=5)

# --- Right Deck ---
right_deck = tk.Frame(decks_frame, bg="#23252a")
right_deck.pack(side="right", expand=True, fill="both", padx=10)
tempo_b = tk.Scale(right_deck, from_=-100, to=100, orient="vertical", length=200, bg="#23252a", fg="white", troughcolor="#444", highlightthickness=0, label="TEMPO", command=lambda v: set_tempo(1, v))
tempo_b.set(0)
tempo_b.pack(side="right", padx=10)
tk.Button(right_deck, text="CUE", width=6, bg="#444", fg="white", command=lambda: stop_deck(1)).pack(pady=5)
tk.Button(right_deck, text="▶", width=6, bg="#444", fg="white", command=lambda: play_pause(1)).pack(pady=5)

# --- Crossfader ---
crossfader_frame = tk.Frame(root, bg="#23252a")
crossfader_frame.pack(pady=10)
tk.Scale(crossfader_frame, from_=0, to=1, orient="horizontal", length=300, resolution=0.01, bg="#23252a", fg="white", troughcolor="#444", highlightthickness=0, command=set_crossfade).pack()

root.mainloop()