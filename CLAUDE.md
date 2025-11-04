# Viz - 3D Audio Visualizer

## Initialization Process

This project was initialized using UV package manager with a complete Python project structure for a 3D audio visualizer that captures audio from BlackHole on macOS.

### Initial Setup (Commit 79d6134)

The initialization process created:

**Project Infrastructure:**
- UV-based Python project with pyproject.toml configuration
- Core dependencies: pygame, numpy, pyaudio, scipy
- Modular architecture with audio and graphics modules
- Makefile for common development commands
- Comprehensive documentation (README.md and CLAUDE.md)
- Python 3.11+ environment with .python-version file

**Features Implemented:**
- Audio capture module for BlackHole device detection
- FFT-based frequency analyzer with logarithmic binning
- Isometric 3D-to-2D projection system
- Pygame renderer with time-history waterfall visualization
- Configuration system with pale blue styling

**File Structure Created:**
- 16 files total with 792+ lines of code
- Complete module structure with __init__.py files
- py.typed marker for type checking support
- Dedicated modules for audio, graphics, and utilities

## Project Overview

Viz is a Python-based 3D audio visualizer designed for macOS that captures audio output from a BlackHole multi-output channel setup and displays a real-time frequency spectrum visualization.

The visualizer displays frequency spectrum in 3D space with:
- **X-axis**: frequency bands
- **Y-axis**: amplitude/volume
- **Z-axis**: time progression (waterfall effect)

## Architecture

### Visualization Design

The visualizer displays audio data in a 3D space with the following axes:
- **X-axis**: Frequency bands (from low to high)
- **Y-axis**: Amplitude/Volume level
- **Z-axis**: Time progression

The visualization uses an isometric perspective view (similar to video games) where:
- The current time slice is rendered at the front
- As time progresses, older data moves down and to the left
- Creates a "waterfall" effect showing frequency evolution over time

### Visual Style
- Line color: Pale blue (#ADD8E6 or similar)
- Line thickness: Medium (2-3 pixels)
- Rendering: Pygame with OpenGL acceleration (if available)

## Technical Stack

### Core Dependencies
- **pygame**: UI rendering and graphics
- **numpy**: Fast array operations and FFT calculations
- **pyaudio**: Audio input capture from BlackHole
- **scipy**: Signal processing utilities

### Audio Setup (macOS)
This project requires BlackHole to be installed and configured as a multi-output device:
1. Install BlackHole (https://existential.audio/blackhole/)
2. Create a Multi-Output Device in Audio MIDI Setup
3. Add both your speakers and BlackHole to the multi-output
4. Configure the application to capture from BlackHole

## Project Structure

```
viz/
├── src/
│   └── viz/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── capture.py       # Audio input handling
│       │   └── analyzer.py      # FFT and frequency analysis
│       ├── graphics/
│       │   ├── __init__.py
│       │   ├── renderer.py      # Pygame rendering
│       │   └── isometric.py     # 3D to 2D projection
│       └── utils/
│           ├── __init__.py
│           └── config.py        # Configuration settings
├── pyproject.toml
├── Makefile
├── README.md
└── CLAUDE.md                    # This file - Technical documentation
```

## Development Commands

Use the Makefile for common development tasks:
- `make install` - Install dependencies
- `make run` - Run the visualizer
- `make clean` - Clean up cache files
- `make format` - Format code
- `make lint` - Lint code

## Key Implementation Details

### Audio Processing
1. Capture audio stream from BlackHole device
2. Apply windowing function to audio chunks
3. Perform FFT to get frequency spectrum
4. Map frequencies to logarithmic scale for better visualization
5. Smooth amplitude values to reduce jitter

### 3D Rendering
1. Maintain a circular buffer of frequency spectrums (time history)
2. Convert 3D coordinates to 2D isometric projection
3. Render lines for each frequency band across time slices
4. Use depth sorting for proper occlusion

### Performance Considerations
- Buffer size: Balance between latency and frequency resolution
- Update rate: Target 30-60 FPS for smooth animation
- History depth: Store 50-100 time slices for adequate time visualization

## Configuration Options

Key parameters to tune:
- `SAMPLE_RATE`: Audio sample rate (44100 or 48000 Hz)
- `CHUNK_SIZE`: Audio buffer size (1024, 2048, or 4096 samples)
- `NUM_FREQUENCY_BANDS`: Number of frequency divisions (32-128)
- `TIME_HISTORY_LENGTH`: Number of time slices to display
- `LINE_COLOR`: RGB tuple for visualization color
- `LINE_THICKNESS`: Width of rendered lines

## Future Enhancements

Potential features to add:
- Multiple visualization modes
- Color schemes based on frequency or amplitude
- Export to video
- Audio file playback mode
- Configuration UI
- Performance metrics overlay
