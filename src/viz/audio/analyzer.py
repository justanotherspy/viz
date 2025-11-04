"""
Audio analysis module for FFT and frequency spectrum analysis.
"""
import numpy as np
from scipy import signal
from ..utils import config


class AudioAnalyzer:
    """Performs FFT and frequency analysis on audio data."""

    def __init__(self):
        """Initialize the audio analyzer."""
        self.window = signal.windows.hann(config.CHUNK_SIZE)
        self.prev_spectrum = None

    def analyze(self, audio_data):
        """
        Analyze audio data and return frequency spectrum.

        Args:
            audio_data: NumPy array of audio samples

        Returns:
            NumPy array of frequency amplitudes
        """
        if audio_data is None or len(audio_data) == 0:
            return np.zeros(config.NUM_FREQUENCY_BANDS)

        # Convert stereo to mono if needed
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Apply window function
        windowed = audio_data[: config.CHUNK_SIZE] * self.window

        # Perform FFT
        fft_data = np.fft.rfft(windowed)
        fft_magnitude = np.abs(fft_data)

        # Convert to frequency bins
        spectrum = self._map_to_frequency_bands(fft_magnitude)

        # Apply smoothing
        if self.prev_spectrum is not None:
            spectrum = (
                config.SMOOTHING_FACTOR * self.prev_spectrum
                + (1 - config.SMOOTHING_FACTOR) * spectrum
            )

        self.prev_spectrum = spectrum
        return spectrum

    def _map_to_frequency_bands(self, fft_magnitude):
        """
        Map FFT output to logarithmic frequency bands.

        Args:
            fft_magnitude: FFT magnitude array

        Returns:
            NumPy array of frequency band amplitudes
        """
        # Create logarithmic frequency scale
        freqs = np.fft.rfftfreq(config.CHUNK_SIZE, 1.0 / config.SAMPLE_RATE)

        # Filter to desired frequency range
        freq_mask = (freqs >= config.MIN_FREQUENCY) & (freqs <= config.MAX_FREQUENCY)
        filtered_freqs = freqs[freq_mask]
        filtered_magnitudes = fft_magnitude[freq_mask]

        if len(filtered_freqs) == 0:
            return np.zeros(config.NUM_FREQUENCY_BANDS)

        # Create logarithmic bins
        log_bins = np.logspace(
            np.log10(config.MIN_FREQUENCY),
            np.log10(config.MAX_FREQUENCY),
            config.NUM_FREQUENCY_BANDS + 1,
        )

        # Map magnitudes to bins
        spectrum = np.zeros(config.NUM_FREQUENCY_BANDS)
        for i in range(config.NUM_FREQUENCY_BANDS):
            bin_mask = (filtered_freqs >= log_bins[i]) & (
                filtered_freqs < log_bins[i + 1]
            )
            if np.any(bin_mask):
                spectrum[i] = np.mean(filtered_magnitudes[bin_mask])

        # Normalize
        max_val = np.max(spectrum)
        if max_val > 0:
            spectrum = spectrum / max_val

        return spectrum
