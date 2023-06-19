import pyaudio
import time
import numpy as np

class AudioPlayer:
    def __init__(self, blockSize=1024):
        self.is_streaming = False
        self.blockSize = blockSize
        self.audioData = None
        self.fs = None
        self.stream = None

    def play(self, audioData, fs):
        self.portaudio = pyaudio.PyAudio()
        if(self.stream is not None):
            print("Cannot start - please stop the player first")
            return

        if(len(audioData.shape) > 1):
            # Channels must be nChannels x nSamples
            assert(len(audioData.shape) == 2)
            assert(audioData.shape[0] < audioData.shape[1])
        else:
            audioData = np.array([audioData])

        nChannels = audioData.shape[0]

        # Flatten the n-channel data into a single interleaved array
        self.audioData = audioData.flatten('F').astype(np.float32)

        # Store the sampling rate
        self.fs = fs

        # Calculate the number of frames in a block
        self.frame_count = self.blockSize * nChannels 
        # Calculate the total number of blocks to play
        self.num_blocks = self.audioData.shape[0] // (self.frame_count) + 1
        # Reset the block index
        self.block_i = 0

        # Start the stream
        self.is_streaming = True
        self.stream = self.portaudio.open(format=pyaudio.paFloat32,
                                     channels=nChannels,
                                     rate=self.fs,
                                     output=True,
                                     input=False,
                                     frames_per_buffer = self.blockSize,
                                     stream_callback = self.play_block)
        self.stream.start_stream()

    def is_playing(self):
        if self.stream is not None:
            return self.stream.is_active()
        return False
    
    def play_block(self, in_data, frame_count, time_info, status):
        # If we have finished playing (or received a request to stop), return silence
        if(not self.is_streaming or self.block_i >= self.num_blocks):
            return None, pyaudio.paComplete

        # Try to get the latest data block otherwise
        data = self.audioData[self.frame_count*self.block_i:self.frame_count*(self.block_i+1)]

        # Increment the block index
        self.block_i += 1
        # Return the next block of audio data
        return (data, pyaudio.paContinue)
        

    def stop(self):
        # Turn off our streaming flag
        self.is_streaming = False
        while(self.stream.is_active()):
            time.sleep(0.1)
        print("Stopped playing")
        self.stream.stop_stream()
        self.stream.close()
        self.portaudio.terminate()

        self.portaudio = None
        self.stream = None
        self.audioData = None
