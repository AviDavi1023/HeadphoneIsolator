import pyaudio
import wave
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 60
WAVE_OUTPUT_FILENAME = "output.wav"
VOLUME_FACTOR = 2.5

p = pyaudio.PyAudio()

# Get the list of all input devices
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# Choose the desired Bluetooth device index or device ID
desired_device_index = 1  # Change this to the desired Bluetooth device index

stream_rec = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input_device_index=desired_device_index,  # Specify the Bluetooth device index here
                    input=True,
                    frames_per_buffer=CHUNK)

stream_play = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     output=True,
                     frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream_rec.read(CHUNK)
    npdata = np.frombuffer(data, dtype=np.int16)
    npdata = (npdata * VOLUME_FACTOR).astype(np.int16)
    louder_data = npdata.tobytes()
    frames.append(louder_data)
    stream_play.write(louder_data)

print("* done recording")

stream_rec.stop_stream()
stream_rec.close()
stream_play.stop_stream()
stream_play.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
