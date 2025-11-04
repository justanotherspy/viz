# Viz - 3D Audio Visualizer

A real-time 3D audio spectrum visualizer for macOS that creates stunning frequency visualizations from your system audio output.

![Visualization Style](https://img.shields.io/badge/style-isometric-blue)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.11+-blue)

## Overview

Viz captures audio from a BlackHole multi-output device on macOS and renders a beautiful 3D frequency spectrum visualization using pygame. The visualization displays frequency data across three dimensions:

- **X-axis**: Frequency bands (low to high)
- **Y-axis**: Amplitude/volume levels
- **Z-axis**: Time progression

As music plays, the current frequency spectrum appears at the front, and older data gracefully flows down and to the left, creating a mesmerizing "waterfall" effect in an isometric perspective.

## Features

- **Real-time audio capture** from BlackHole output
- **3D isometric visualization** with pale blue medium-thickness lines and waterfall effect
- **Smooth frequency spectrum analysis** using FFT with logarithmic frequency binning
- **Demo mode** with generated audio when no audio device is available
- **Custom application icon** with frequency spectrum design
- **Live UI overlay** showing FPS and buffer status
- **Optimized rendering** for 60 FPS performance with hardware acceleration
- **Graceful error handling** with automatic fallback modes

## Prerequisites

### System Dependencies (macOS only)

**For live audio capture**, install PortAudio:
```bash
brew install portaudio
```

**Note**: The visualizer will run in demo mode without PortAudio/PyAudio, generating test audio for visualization testing.

### macOS Audio Setup (for live audio)

1. **Install BlackHole**
   ```bash
   brew install blackhole-2ch
   ```
   Or download from: https://existential.audio/blackhole/

2. **Create Multi-Output Device**
   - Open "Audio MIDI Setup" (in Applications/Utilities)
   - Click the "+" button and select "Create Multi-Output Device"
   - Check both your speakers/headphones and BlackHole
   - (Optional) Right-click and set as default output

### Python Requirements

- Python 3.11 or higher
- UV package manager

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd viz
   ```

2. **Install UV** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**

   For demo mode (no audio required):
   ```bash
   make install
   ```

   For live audio mode (requires PortAudio installed first):
   ```bash
   uv pip install --extra audio .
   ```

## Usage

### Running the Visualizer

Run the visualizer:
```bash
make run
```

Or directly with UV:
```bash
uv run viz
```

### Controls

- **Close window** or **ESC key**: Exit the application
- **Ctrl+C** in terminal: Gracefully shutdown

### Modes

**Live Audio Mode** (when PyAudio is installed and BlackHole is configured):
- Captures real-time audio from your system output
- Displays actual frequency spectrum of playing audio

**Demo Mode** (automatic fallback):
- Runs when PyAudio is not installed or no audio device is found
- Generates test audio (mixed sine waves) for visualization
- Perfect for testing and development without audio hardware

## Development

### Available Commands

```bash
make help        # Show all available commands
make install     # Install dependencies
make run         # Run the visualizer
make clean       # Clean up cache files
make format      # Format code with ruff
make lint        # Lint code with ruff
make test        # Run tests
```

### Project Structure

```
viz/
├── src/viz/
│   ├── main.py              # Entry point and Visualizer class
│   ├── audio/
│   │   ├── capture.py       # Audio capture (PyAudio wrapper)
│   │   └── analyzer.py      # FFT frequency analysis
│   ├── graphics/
│   │   ├── renderer.py      # Pygame rendering engine
│   │   └── isometric.py     # 3D to 2D projection
│   └── utils/
│       ├── config.py        # Configuration settings
│       └── icon.py          # Application icon generator
├── pyproject.toml           # Project dependencies
├── Makefile                 # Development commands
├── .gitignore              # Git ignore patterns
└── README.md
```

## Configuration

Key settings can be adjusted in `src/viz/utils/config.py`:

- `SAMPLE_RATE`: Audio sample rate (default: 44100 Hz)
- `CHUNK_SIZE`: Audio buffer size (default: 2048 samples)
- `NUM_FREQUENCY_BANDS`: Number of frequency divisions
- `TIME_HISTORY_LENGTH`: Number of time slices to display
- `LINE_COLOR`: Visualization color (default: pale blue)
- `LINE_THICKNESS`: Width of rendered lines

## Technical Details

### Audio Pipeline
- **Capture**: PyAudio captures audio chunks from BlackHole device (optional)
- **Analysis**: NumPy FFT with Hann windowing function
- **Frequency Mapping**: Logarithmic binning from 20Hz to 20kHz
- **Smoothing**: Exponential moving average to reduce jitter
- **Demo Mode**: Generates mixed sine waves with varying frequencies

### Graphics Pipeline
- **Window**: 1280x720 pygame window with custom icon
- **Projection**: Isometric 3D-to-2D transformation
- **Rendering**: Hardware-accelerated double-buffered drawing
- **Visualization**: 64 frequency bands × 80 time slices waterfall
- **Colors**: Pale blue (#ADD8E6) lines with alpha fade for depth
- **Performance**: Circular buffer with VSync for smooth 60 FPS

### Architecture
- **Visualizer Class**: Main application lifecycle manager
- **Event Loop**: Handles window events, audio processing, and rendering
- **Resource Management**: Proper initialization and cleanup of all subsystems
- **Error Handling**: Graceful degradation with informative error messages

## Troubleshooting

**Installation fails with "portaudio.h file not found"**
- This is expected if you want to run in demo mode only
- For live audio, install PortAudio first: `brew install portaudio`
- If you've just installed PortAudio, set environment variables:
  ```bash
  export CFLAGS="-I/opt/homebrew/include"
  export LDFLAGS="-L/opt/homebrew/lib"
  uv pip install --extra audio .
  ```

**Application runs in demo mode instead of live audio**
- Check that PyAudio is installed: `uv pip install --extra audio .`
- Ensure BlackHole is installed and configured in Audio MIDI Setup
- Verify audio is playing through the Multi-Output Device
- Check application has microphone permissions (System Preferences > Security & Privacy)

**No window appears**
- The application requires a display - cannot run headless
- Check that pygame is properly installed
- Look for error messages in the terminal output

**Low frame rate**
- Reduce `TIME_HISTORY_LENGTH` in `src/viz/utils/config.py`
- Decrease `NUM_FREQUENCY_BANDS`
- Try disabling VSync: set `VSYNC = False` in config

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [BlackHole](https://existential.audio/blackhole/) for virtual audio routing
- [UV](https://github.com/astral-sh/uv) for fast Python package management
- [Pygame](https://www.pygame.org/) for graphics rendering
