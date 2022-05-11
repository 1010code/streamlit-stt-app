import pyaudio
import deepspeech
import numpy as np
from queue import SimpleQueue
from pathlib import Path

BUFFERS_PER_SECOND = 10
SAMPLE_WIDTH = 2
BEAM_WIDTH = 512


buffer_queue = SimpleQueue()


def audio_callback(in_data, frame_count, time_info, status_flags):
    buffer_queue.put(np.frombuffer(in_data, dtype='int16'))
    return (None, pyaudio.paContinue)


def find_device(pyaudio, device_name):
    ''' find specific device or return default input device'''
    default = pyaudio.get_default_input_device_info()
    for i in range(pyaudio.get_device_count()):
        name = pyaudio.get_device_info_by_index(i)['name']
        if name == device_name:
            return (i, name)
    return (default['index'], default['name'])


def main():

    audio = pyaudio.PyAudio()
    index, name = find_device(audio, 'pulse')

    print(f'select device {name}')

    buffer_size = 18000
    audio_stream = audio.open(rate=buffer_size,
                              channels=1,
                              format=audio.get_format_from_width(
                                  SAMPLE_WIDTH, unsigned=False),
                              input_device_index=index,
                              input=True,
                              frames_per_buffer=buffer_size,
                              stream_callback=audio_callback)
    frames = []
    while audio_stream.is_active():
        print(buffer_queue.get().shape)


if __name__ == '__main__':
    main()
    #find_device()