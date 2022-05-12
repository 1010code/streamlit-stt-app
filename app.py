# import logging
# import logging.handlers
# import queue
# import threading
# import time
# import urllib.request
# from collections import deque
# from pathlib import Path
# from typing import List

# import numpy as np
# import pydub
# import streamlit as st

# from streamlit_webrtc import (
#     AudioProcessorBase,
#     ClientSettings,
#     WebRtcMode,
#     webrtc_streamer,
# )

# logger = logging.getLogger(__name__)


# def main():
#     st.header("Real Time Speech-to-Text")

#     sound_only_page = "Sound only (sendonly)"
#     app_mode = st.selectbox("Choose the app mode", [sound_only_page])

#     if app_mode == sound_only_page:
#         app_sst()

# def app_sst():
#     webrtc_ctx = webrtc_streamer(
#         key="speech-to-text",
#         mode=WebRtcMode.SENDONLY,
#         audio_receiver_size=1024,
#         client_settings=ClientSettings(
#             rtc_configuration={
#                 "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
#             },
#             media_stream_constraints={"video": False, "audio": True},
#         ),
#     )
#     # status_indicator = st.empty()

#     # if not webrtc_ctx.state.playing:
#     #     return

#     # status_indicator.write("Loading...")
#     # text_output = st.empty()

#     # while True:
#     #     if webrtc_ctx.audio_receiver:

#     #         sound_chunk = pydub.AudioSegment.empty()
#     #         try:
#     #             audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
#     #         except queue.Empty:
#     #             time.sleep(0.1)
#     #             status_indicator.write("No frame arrived.")
#     #             continue

#     #         status_indicator.write("Running. Say something!")

#     #         for audio_frame in audio_frames:
#     #             sound = pydub.AudioSegment(
#     #                 data=audio_frame.to_ndarray().tobytes(),
#     #                 sample_width=audio_frame.format.bytes,
#     #                 frame_rate=audio_frame.sample_rate,
#     #                 channels=len(audio_frame.layout.channels),
#     #             )
#     #             sound_chunk += sound
#     #         if len(sound_chunk) > 0:
#     #             sound_chunk = sound_chunk.set_channels(1).set_frame_rate(
#     #                 18000
#     #             )
#     #             buffer = np.array(sound_chunk.get_array_of_samples())
#     #             text_output.markdown(f"**Text:** {buffer}")
#     #     else:
#     #         status_indicator.write("AudioReciver is not set. Abort.")
#     #         break


# if __name__ == "__main__":
#     import os

#     DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

#     logging.basicConfig(
#         format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
#         "%(message)s",
#         force=True,
#     )

#     logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

#     st_webrtc_logger = logging.getLogger("streamlit_webrtc")
#     st_webrtc_logger.setLevel(logging.DEBUG)

#     fsevents_logger = logging.getLogger("fsevents")
#     fsevents_logger.setLevel(logging.WARNING)

#     main()

import av
import cv2
import time
import streamlit as st
from aiortc.contrib.media import MediaRecorder

from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer


def app():
    class OpenCVEdgeProcessor(VideoProcessorBase):
        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            # perform edge detection
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            return av.VideoFrame.from_ndarray(img, format="bgr24")

    def in_recorder_factory() -> MediaRecorder:
        return MediaRecorder(
            "input.mp3", format="mp3"
        )  # HLS does not work. See https://github.com/aiortc/aiortc/issues/331

    def out_recorder_factory() -> MediaRecorder:
        return

    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={
            "video": False,
            "audio": True,
        },
        # video_processor_factory=OpenCVEdgeProcessor,
        in_recorder_factory=in_recorder_factory,
        out_recorder_factory=out_recorder_factory,
    )
    try:
        time.sleep(1)
        st.audio('input.mp3', format="audio/mp3", start_time=0)
    except:
        st.write("No record media.")

if __name__ == "__main__":
    app()