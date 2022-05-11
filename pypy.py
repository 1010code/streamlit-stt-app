import pyaudio
import wave
import numpy as np
import sounddevice as sd
import streamlit as st

st.header("Real Time Speech-to-Text")
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # read data-chunks in strings
    data = stream.read(CHUNK)
    #frames.append(data)
    # change the format to numpy int16
    frames.append(np.fromstring(data,dtype=np.int16))
#newS = np.fromstring(frames,dtype=np.int16)
print("* done recording")
sound = np.array(frames)
sound = sound.flatten()
sd.play(sound,44100*1)
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

audio_file = open('output.wav', 'rb')
audio_bytes = audio_file.read()
print(audio_bytes)
print(len(audio_bytes))
print(type(audio_bytes))
st.audio(audio_bytes, format='audio/wav')