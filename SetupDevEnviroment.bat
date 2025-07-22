@echo off
REM Install Python dependencies for DJapp.py

python -m pip install --upgrade pip
python -m pip install tkinter sounddevice soundfile numpy matplotlib librosa
echo.
echo All dependencies installed!
pause