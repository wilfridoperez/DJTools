import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 1. Load an audio file
# Replace 'your_audio_file.wav' with the path to your actual audio file (e.g., .wav, .mp3, .flac)
try:
    y, sr = librosa.load('Pump_Up_The_Jam.mp3')
    print(f"Audio loaded successfully. Sampling rate: {sr} Hz, Duration: {librosa.get_duration(y=y, sr=sr):.2f} seconds")
except FileNotFoundError:
    print("Error: 'your_audio_file.wav' not found. Please provide a valid audio file path.")
    exit()
except Exception as e:
    print(f"An error occurred while loading the audio: {e}")
    exit()

# 2. Visualize the waveform
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Audio Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# 3. Extract a simple feature: Root Mean Square (RMS) energy
# RMS energy can indicate the loudness of the audio over time
rms = librosa.feature.rms(y=y)[0]
times = librosa.times_like(rms, sr=sr)

plt.figure(figsize=(12, 4))
plt.plot(times, rms)
plt.title('RMS Energy over Time')
plt.xlabel('Time (s)')
plt.ylabel('RMS Energy')
plt.grid(True)
plt.show()

# 4. (Optional) Extract a more complex feature: Mel-Frequency Cepstral Coefficients (MFCCs)
# MFCCs are widely used in speech recognition and music information retrieval
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13) # Extract 13 MFCCs

plt.figure(figsize=(12, 4))
librosa.display.specshow(mfccs, x_axis='time', sr=sr)
plt.colorbar(format='%+2.0f dB')
plt.title('MFCCs')
plt.tight_layout()
plt.show()