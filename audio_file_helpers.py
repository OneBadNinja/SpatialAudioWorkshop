import soundfile as sf
from scipy import signal
import numpy as np

def fade_in_out_audio_data(data):
    # Create a tukey window for fading in and out our sounds
    fade_in_out_window = signal.windows.tukey(data.shape[1], 0.1)

    for channel_index in np.arange(len(data)):
        data[channel_index, :] *= fade_in_out_window

    return data

def fix_duration(data, duration_samples):
    nChannels = data.shape[0]
    if(data.shape[1] > duration_samples):
        data = fade_in_out_audio_data(data[:, :duration_samples])
    else:
        data = fade_in_out_audio_data(data)
        # Pad with zeros
        data = np.pad(data,((0, 0), (0,duration_samples-data.shape[1])))
        assert(list(data.shape) == [nChannels, duration_samples])
    return data

def load_audio_file(filename, duration=None):
    audio_data, fs = sf.read(filename)

    # Convert to 2d array if 1 channel
    if(len(audio_data.shape) > 1):
        # Transpose so it is nChannels x nSamples
        audio_data = audio_data.T
    else:
        audio_data = np.array([audio_data])

    # Normalise our data between -1 and 1
    audio_data /= np.max(np.abs(audio_data))

    # If we specified a duration, pad or trim to this duration
    if(duration):
        # Trim and fade our soundfile to duration seconds
        duration_samples = int(np.floor(duration * fs))  # Compute our duration length in samples
        audio_data = fix_duration(audio_data, duration_samples)
    else:
        # Fade in and out our soundfile
        audio_data = fade_in_out_audio_data(audio_data)


    # Return the trimmed/padded and faded audio data.
    if(audio_data.shape[0] == 1):
        audio_data = audio_data[0]
    return audio_data, fs