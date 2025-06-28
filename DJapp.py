import pygame
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import librosa
from tempfile import NamedTemporaryFile
import threading
import time
from matplotlib.animation import FuncAnimation

pygame.mixer.init()

root = tk.Tk()
root.title("DJ Mixer with Crossfader, Waveform, and BPM Sync")

channel_a = pygame.mixer.Channel(0)
channel_b = pygame.mixer.Channel(1)
sound_a = None
sound_b = None

bpm_a = None
bpm_b = None
path_a = None
path_b = None

play_start_a = None
play_start_b = None

def show_waveform(audio_segment, title):
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)  # Convert stereo to mono
    time_axis = np.linspace(0, len(samples) / audio_segment.frame_rate, num=len(samples))
    
    plt.figure(figsize=(5, 2))
    plt.plot(time_axis, samples, linewidth=0.5)
    plt.title(f"Waveform - {title}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

#def detect_bpm(file_path):
#    y, sr = librosa.load(file_path, sr=None, mono=True)
#    tempo, _ = librosa.beat.beat_track(y, sr=sr)
#    return tempo

def detect_bpm(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=True)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

def load_track(channel):
    global sound_a, sound_b, bpm_a, bpm_b, path_a, path_b, play_start_a, play_start_b
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        bpm = detect_bpm(file_path)
       # print(f"Detected BPM for Deck {'A' if channel == 0 else 'B'}: {bpm:.2f}")

        if channel == 0:
            path_a = file_path
            bpm_a = bpm
            sound_a = pygame.mixer.Sound(file_path)
            channel_a.play(sound_a, loops=-1)
            play_start_a = time.time()
        else:
            path_b = file_path
            bpm_b = bpm
            sound_b = pygame.mixer.Sound(file_path)
            channel_b.play(sound_b, loops=-1)
            play_start_b = time.time()

def stop_tracks():
    pygame.mixer.stop()

def set_volume(channel, value):
    volume = float(value)
    if channel == 0:
        channel_a.set_volume(volume)
    else:
        channel_b.set_volume(volume)

def set_crossfade(value):
    fade = float(value)
    channel_a.set_volume(1.0 - fade)
    channel_b.set_volume(fade)

def sync_bpm():
    global bpm_a, bpm_b, path_b, sound_b
    if bpm_a and bpm_b and path_b:
        ratio = bpm_a / bpm_b
#        print(f"Syncing Track B to Track A BPM (×{ratio:.2f})")
        audio = AudioSegment.from_file(path_b)
        faster = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * ratio)
        }).set_frame_rate(audio.frame_rate)

        with NamedTemporaryFile(delete=False, suffix=".wav") as f:
            faster.export(f.name, format="wav")
            sound_b = pygame.mixer.Sound(f.name)
            channel_b.play(sound_b, loops=-1)
    else:
        print("Make sure both tracks are loaded and analyzed for BPM.")


def live_waveform(audio_segment, title):
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)
    time_axis = np.linspace(0, len(samples) / audio_segment.frame_rate, num=len(samples))

    fig, ax = plt.subplots(figsize=(5, 2))
    line, = ax.plot([], [], lw=0.5)
    ax.set_xlim(0, 5)  # Show 5 seconds window
    ax.set_ylim(np.min(samples), np.max(samples))
    ax.set_title(f"Live Waveform - {title}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    def update(frame):
        # Show a moving window of 5 seconds
        start = int(frame * audio_segment.frame_rate)
        end = start + int(5 * audio_segment.frame_rate)
        if end > len(samples):
            end = len(samples)
        line.set_data(time_axis[start:end], samples[start:end])
        return line,

    ani = FuncAnimation(fig, update, frames=range(0, len(samples) // audio_segment.frame_rate), interval=100, blit=True)
    plt.show()

def start_waveform_visual123(channel):
    if channel == 0 and path_a:
        audio = AudioSegment.from_file(path_a)
        live_waveform(audio, "Deck A")
    elif channel == 1 and path_b:
        audio = AudioSegment.from_file(path_b)
        live_waveform(audio, "Deck B")

def live_waveform_sync(audio_segment, title, channel):
    global play_start_a, play_start_b
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)
    time_axis = np.linspace(0, len(samples) / audio_segment.frame_rate, num=len(samples))

    fig, ax = plt.subplots(figsize=(5, 2))
    line, = ax.plot([], [], lw=0.5)
    ax.set_xlim(0, 5)  # Show 5 seconds window
    ax.set_ylim(np.min(samples), np.max(samples))
    ax.set_title(f"Live Waveform - {title}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    def update(_):
        # Calculate playback position in seconds
        if channel == 0:
            if play_start_a is None:
                pos_sec = 0
            else:
                pos_sec = time.time() - play_start_a
        else:
            if play_start_b is None:
                pos_sec = 0
            else:
                pos_sec = time.time() - play_start_b

        # Show a moving window of 5 seconds centered on playback
        start_time = max(0, pos_sec - 2.5)
        end_time = start_time + 5
        start_idx = int(start_time * audio_segment.frame_rate)
        end_idx = int(end_time * audio_segment.frame_rate)
        if end_idx > len(samples):
            end_idx = len(samples)
        line.set_data(time_axis[start_idx:end_idx], samples[start_idx:end_idx])
        ax.set_xlim(start_time, end_time)
        return line,

    ani = FuncAnimation(fig, update, interval=50, blit=True)
    plt.show()

def start_waveform_visual(channel):
    if channel == 0 and path_a:
        audio = AudioSegment.from_file(path_a)
        live_waveform_sync(audio, "Deck A", 0)
    elif channel == 1 and path_b:
        audio = AudioSegment.from_file(path_b)
        live_waveform_sync(audio, "Deck B", 1)

# UI Elements
tk.Button(root, text="Load Track A", command=lambda: load_track(0)).pack()
tk.Button(root, text="Load Track B", command=lambda: load_track(1)).pack()

tk.Label(root, text="Volume A").pack()
vol_a = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal",
                 command=lambda v: set_volume(0, v))
vol_a.set(1)
vol_a.pack()

tk.Label(root, text="Volume B").pack()
vol_b = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal",
                 command=lambda v: set_volume(1, v))
vol_b.set(1)
vol_b.pack()

tk.Label(root, text="Crossfader").pack()
cross = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal",
                 command=set_crossfade)
cross.set(0.5)
cross.pack()

tk.Button(root, text="Sync B to A", command=sync_bpm).pack()
tk.Button(root, text="Stop All", command=stop_tracks).pack()

tk.Button(root, text="Visualize Deck A", command=lambda: start_waveform_visual(0)).pack()
tk.Button(root, text="Visualize Deck B", command=lambda: start_waveform_visual(1)).pack()

root.mainloop()
