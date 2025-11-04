"""
Audio capture module for capturing audio from BlackHole device.
"""
import pyaudio
import numpy as np
from ..utils import config


class AudioCapture:
    """Handles audio input capture from BlackHole device."""

    def __init__(self):
        """Initialize the audio capture system."""
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.device_index = self._find_blackhole_device()

    def _find_blackhole_device(self):
        """Find the BlackHole audio device."""
        # TODO: Implement device detection
        # For now, return None (will need to be implemented)
        for i in range(self.pa.get_device_count()):
            device_info = self.pa.get_device_info_by_index(i)
            if "BlackHole" in device_info.get("name", ""):
                return i
        return None

    def start(self):
        """Start the audio capture stream."""
        if self.device_index is None:
            raise RuntimeError("BlackHole device not found")

        self.stream = self.pa.open(
            format=pyaudio.paFloat32,
            channels=config.CHANNELS,
            rate=config.SAMPLE_RATE,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=config.CHUNK_SIZE,
        )

    def read_chunk(self):
        """Read a chunk of audio data."""
        if self.stream is None:
            return None

        try:
            data = self.stream.read(config.CHUNK_SIZE, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)
            return audio_data
        except Exception as e:
            print(f"Error reading audio: {e}")
            return None

    def stop(self):
        """Stop the audio capture stream."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def close(self):
        """Clean up audio resources."""
        self.stop()
        self.pa.terminate()
