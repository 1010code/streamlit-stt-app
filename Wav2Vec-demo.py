import av
import streamlit as st
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer

from IPython.display import Audio
from scipy.io import wavfile
import numpy as np
import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

st.cache()
def load_model():
     # load pretrained model
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    return processor, model
processor, model = load_model()

def inference():
    st.write("loading.")
    file_name = 'input.wav'
    data = wavfile.read(file_name)
    framerate = data[0]
    sounddata = data[1]
    time = np.arange(0,len(sounddata))/framerate
    st.write('Sample rate:',framerate,'Hz')
    st.write('Total time:',len(sounddata)/framerate,'s')
    
    input_audio, _ = librosa.load(file_name,  sr=16000)
    input_values = processor(input_audio, return_tensors="pt", sampling_rate=16000).input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    st.write('Result:', transcription)

def app():
    st.write("Click start button to record audio.")
    def in_recorder_factory() -> MediaRecorder:
        return MediaRecorder(
            "input.wav", format="wav"
        )

    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={
            "video": False,
            "audio": True,
        },
        sendback_audio=False,
        in_recorder_factory=in_recorder_factory,
    )
    try:
        st.audio('input.wav', format="audio/wav")
        if st.button('Compute'):
            # call Wav2Vec model and inference.
            inference()
    except:
        st.write("No record media.")
        

if __name__ == "__main__":
    app()