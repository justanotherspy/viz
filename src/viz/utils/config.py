"""
Configuration settings for the Viz audio visualizer.
"""

# Audio Settings
SAMPLE_RATE = 44100  # Hz
CHUNK_SIZE = 2048  # samples per buffer
CHANNELS = 2  # stereo

# Visualization Settings
NUM_FREQUENCY_BANDS = 64  # number of frequency bins to display
TIME_HISTORY_LENGTH = 80  # number of time slices to keep
FPS_TARGET = 60  # target frames per second

# Display Settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Viz - 3D Audio Visualizer"

# Visual Style
LINE_COLOR = (173, 216, 230)  # pale blue (ADD8E6)
LINE_THICKNESS = 2  # pixels
BACKGROUND_COLOR = (10, 10, 20)  # dark blue-black

# Isometric Projection Settings
ISO_ANGLE = 30  # degrees for isometric view
SCALE_X = 12  # pixels per frequency band
SCALE_Y = 3  # pixels per amplitude unit
SCALE_Z = 8  # pixels per time slice

# Audio Processing
MIN_FREQUENCY = 20  # Hz
MAX_FREQUENCY = 20000  # Hz
SMOOTHING_FACTOR = 0.7  # 0-1, higher = more smoothing

# Performance
USE_HARDWARE_ACCELERATION = True
VSYNC = True
