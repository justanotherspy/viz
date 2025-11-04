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

- Real-time audio capture from BlackHole output
- 3D isometric visualization with pale blue medium-thickness lines
- Smooth frequency spectrum analysis using FFT
- Optimized rendering for 30-60 FPS performance
- Easy configuration and customization

## Prerequisites

### macOS Audio Setup

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
   ```bash
   make install
   ```

## Usage

Run the visualizer:
```bash
make run
```

Or directly with UV:
```bash
uv run viz
```

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
├── src/viz/          # Main package
│   ├── main.py       # Entry point
│   ├── audio/        # Audio capture and analysis
│   ├── graphics/     # Rendering and visualization
│   └── utils/        # Configuration and utilities
├── pyproject.toml    # Project dependencies
├── Makefile          # Development commands
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

- **Audio Processing**: Uses PyAudio for audio capture and NumPy FFT for frequency analysis
- **Graphics**: Pygame for rendering with isometric 3D-to-2D projection
- **Performance**: Optimized with circular buffers and efficient rendering pipeline

## Troubleshooting

**No audio input detected**
- Ensure BlackHole is installed and selected in Audio MIDI Setup
- Check that audio is playing through the Multi-Output Device
- Verify the application has microphone permissions (System Preferences > Security & Privacy)

**Low frame rate**
- Reduce `TIME_HISTORY_LENGTH` in configuration
- Decrease `NUM_FREQUENCY_BANDS`
- Lower the window resolution

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [BlackHole](https://existential.audio/blackhole/) for virtual audio routing
- [UV](https://github.com/astral-sh/uv) for fast Python package management
- [Pygame](https://www.pygame.org/) for graphics rendering
