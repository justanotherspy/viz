# Viz - 3D Audio Visualizer

## Initialization Process

This project was initialized using UV package manager with a complete Python project structure for a 3D audio visualizer that captures audio from BlackHole on macOS.

### Initial Setup (Commit 79d6134)

The initialization process created:

**Project Infrastructure:**
- UV-based Python project with pyproject.toml configuration
- Core dependencies: pygame, numpy, scipy (pyaudio optional)
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

### Full Implementation (Commit ec4c28a)

**Window Bootstrapping & UI:**
- Custom application icon generator (`utils/icon.py`)
- Proper pygame window initialization with icon and title bar
- Event handling for window close, ESC key, and Ctrl+C
- Live UI overlay with FPS counter and buffer status
- Clean resource management and shutdown

**Audio Pipeline Integration:**
- Connected AudioCapture → AudioAnalyzer → Renderer pipeline
- Demo mode with generated sine wave audio for testing
- PyAudio made optional dependency (under `[audio]` extras)
- Graceful fallback when audio device unavailable
- Proper error handling with informative messages

**Visualizer Application Class:**
- Main lifecycle manager in `main.py`
- Handles initialization: pygame → icon → window → audio → event loop
- Clock-based FPS management for smooth rendering
- Proper cleanup of all subsystems on exit
- Exception handling with stack traces for debugging

## Project Overview

Viz is a Python-based 3D audio visualizer designed for macOS that captures audio output from a BlackHole multi-output channel setup and displays a real-time frequency spectrum visualization.

The visualizer displays frequency spectrum in 3D space with:
- **X-axis**: frequency bands
- **Y-axis**: amplitude/volume
- **Z-axis**: time progression (waterfall effect)

## Architecture

### Application Lifecycle

The `Visualizer` class in `main.py` manages the complete application lifecycle:

1. **Initialization**
   - Initialize pygame subsystem
   - Create and set application icon
   - Initialize Renderer (creates window)
   - Initialize audio components (capture + analyzer)
   - Start audio stream or fallback to demo mode

2. **Main Event Loop**
   - Process pygame events (window close, ESC key)
   - Capture or generate audio chunk
   - Analyze audio with FFT
   - Add spectrum to renderer history
   - Render frame to screen
   - Maintain target FPS with clock

3. **Shutdown**
   - Stop audio stream
   - Close audio resources
   - Quit pygame
   - Exit cleanly

### Visualization Design

The visualizer displays audio data in a 3D space with the following axes:
- **X-axis**: Frequency bands (from low to high, 64 bins)
- **Y-axis**: Amplitude/Volume level (scaled for visibility)
- **Z-axis**: Time progression (80 time slices)

The visualization uses an isometric perspective view (similar to video games) where:
- The current time slice is rendered at the front
- As time progresses, older data moves down and to the left
- Creates a "waterfall" effect showing frequency evolution over time
- Older time slices fade using alpha blending for depth perception

### Visual Style
- **Line color**: Pale blue (#ADD8E6 / RGB 173, 216, 230)
- **Line thickness**: 2 pixels for spectrum, 1 pixel for time connections
- **Background**: Dark blue-black (#0A0A14 / RGB 10, 10, 20)
- **Rendering**: Pygame with hardware acceleration and VSync
- **Window**: 1280×720 with custom icon

## Technical Stack

### Core Dependencies
- **pygame**: UI rendering and graphics
- **numpy**: Fast array operations and FFT calculations
- **scipy**: Signal processing utilities
- **pyaudio** (optional): Audio input capture from BlackHole

### Audio Setup (macOS)

**For Live Audio Mode** (optional):
1. Install PortAudio: `brew install portaudio`
2. Install BlackHole: `brew install blackhole-2ch`
3. Create a Multi-Output Device in Audio MIDI Setup
4. Add both your speakers and BlackHole to the multi-output
5. Install PyAudio: `uv pip install --extra audio .`

**Demo Mode** (automatic fallback):
- Runs without PyAudio or audio hardware
- Generates test audio with mixed sine waves
- Frequencies vary over time for realistic visualization
- Perfect for development and testing

## Project Structure

```
viz/
├── src/
│   └── viz/
│       ├── __init__.py
│       ├── main.py              # Entry point & Visualizer class
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── capture.py       # Audio input (PyAudio wrapper, optional)
│       │   └── analyzer.py      # FFT and frequency analysis
│       ├── graphics/
│       │   ├── __init__.py
│       │   ├── renderer.py      # Pygame rendering & UI
│       │   └── isometric.py     # 3D to 2D projection
│       └── utils/
│           ├── __init__.py
│           ├── config.py        # Configuration settings
│           └── icon.py          # Application icon generator
├── pyproject.toml               # Dependencies & project metadata
├── Makefile                     # Development commands
├── .gitignore                   # Git ignore patterns
├── README.md                    # User documentation
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

### Audio Processing Pipeline

**AudioCapture** (`audio/capture.py`):
- PyAudio wrapper for audio device access (optional dependency)
- Device detection: searches for "BlackHole" in device names
- Captures audio in float32 format at 44.1kHz
- Chunk size: 2048 samples (~46ms latency)
- Stereo input (channels mixed to mono in analyzer)

**AudioAnalyzer** (`audio/analyzer.py`):
1. Apply Hann windowing function to reduce spectral leakage
2. Perform FFT using NumPy's `rfft` (real FFT for efficiency)
3. Map FFT bins to 64 logarithmic frequency bands (20Hz - 20kHz)
4. Normalize amplitudes to 0-1 range
5. Apply exponential smoothing (0.7 factor) to reduce jitter
6. Return spectrum array for visualization

**Demo Mode** (`main.py`):
- Generates mixed sine waves when audio unavailable
- 3 frequencies that vary over time for realism
- Adds small amount of noise for texture
- Maintains proper sample rate and chunk size

### 3D Rendering Pipeline

**Renderer** (`graphics/renderer.py`):
1. Maintains circular buffer (`deque`) of spectrum arrays (80 max)
2. Draws from back to front for proper depth ordering
3. For each time slice:
   - Projects frequency bands to 2D screen coordinates
   - Draws spectrum line connecting all frequency points
   - Draws vertical lines connecting to previous time slice
4. Applies alpha fade: newer slices brighter, older slices dimmer
5. Renders UI overlay (FPS, buffer status)
6. Double-buffered flip with VSync

**IsometricProjection** (`graphics/isometric.py`):
- Converts (x, y, z) 3D coordinates to (screen_x, screen_y)
- Uses 30° isometric angle
- Scaling: X=12px, Y=3px, Z=8px per unit
- Centers visualization in window
- Pre-calculates sin/cos for performance

### Performance Optimizations

**Memory Management:**
- Circular buffer (`deque`) with fixed max length (80 slices)
- Automatic eviction of old data, constant memory usage
- NumPy arrays for efficient numerical operations
- Single spectrum copy per frame

**Rendering:**
- Hardware acceleration enabled (`HWSURFACE`)
- VSync to prevent tearing and limit CPU usage
- Back-to-front drawing avoids overdraw
- Pre-calculated projection matrices
- Clock-based FPS limiting (target 60 FPS)

**Audio Processing:**
- FFT computed on 2048 samples (~2ms on modern CPU)
- Logarithmic binning reduces 1024 FFT bins to 64 bands
- Smoothing filter reduces spectrum recalculation

## Configuration Options

All settings in `src/viz/utils/config.py`:

**Audio Settings:**
- `SAMPLE_RATE`: Audio sample rate (default: 44100 Hz)
- `CHUNK_SIZE`: Audio buffer size (default: 2048 samples)
- `CHANNELS`: Audio channels (default: 2 for stereo)
- `MIN_FREQUENCY`: Lower frequency bound (default: 20 Hz)
- `MAX_FREQUENCY`: Upper frequency bound (default: 20000 Hz)
- `SMOOTHING_FACTOR`: Temporal smoothing 0-1 (default: 0.7)

**Visualization Settings:**
- `NUM_FREQUENCY_BANDS`: Number of frequency bins (default: 64)
- `TIME_HISTORY_LENGTH`: Time slices to display (default: 80)
- `FPS_TARGET`: Target frame rate (default: 60)

**Display Settings:**
- `WINDOW_WIDTH`: Window width in pixels (default: 1280)
- `WINDOW_HEIGHT`: Window height in pixels (default: 720)
- `WINDOW_TITLE`: Window title text

**Visual Style:**
- `LINE_COLOR`: RGB tuple (default: (173, 216, 230) pale blue)
- `LINE_THICKNESS`: Line width in pixels (default: 2)
- `BACKGROUND_COLOR`: RGB tuple (default: (10, 10, 20) dark blue)

**Isometric Projection:**
- `ISO_ANGLE`: Viewing angle in degrees (default: 30)
- `SCALE_X`: Pixels per frequency band (default: 12)
- `SCALE_Y`: Pixels per amplitude unit (default: 3)
- `SCALE_Z`: Pixels per time slice (default: 8)

**Performance:**
- `USE_HARDWARE_ACCELERATION`: Enable hardware rendering (default: True)
- `VSYNC`: Enable vertical sync (default: True)

## Testing & Development Notes

**Important**: This application requires a display and cannot be tested in headless environments. The visualizer creates a pygame window that must be visible to verify functionality.

**Testing Strategy:**
1. **Demo Mode Testing**: Run without PyAudio to verify rendering pipeline
2. **Live Audio Testing**: Requires macOS with BlackHole configured
3. **Performance Testing**: Monitor FPS counter in UI overlay
4. **Visual Verification**: User must manually verify window appearance

**Development Workflow:**
- Make code changes
- User tests locally by running `make run`
- User verifies window appears and visualization works
- Commit changes only after successful user testing

## Implementation Status

**Completed Features:**
- ✅ Complete audio capture system with device detection
- ✅ FFT-based frequency analyzer with logarithmic binning
- ✅ Isometric 3D-to-2D projection system
- ✅ Pygame renderer with waterfall visualization
- ✅ Custom application icon
- ✅ Window initialization and event handling
- ✅ Demo mode with generated audio
- ✅ UI overlay with FPS and buffer status
- ✅ Graceful error handling and fallback modes
- ✅ Resource cleanup and shutdown management
- ✅ Configuration system

**Known Limitations:**
- Requires display (cannot run headless)
- Live audio mode macOS-only (BlackHole dependency)
- PyAudio installation requires PortAudio system library
- No audio file playback mode (live capture only)

## Future Enhancements

Potential features to add:
- Multiple visualization modes (bars, particles, mesh)
- Color schemes based on frequency or amplitude
- Recording/export to video
- Audio file playback mode
- Configuration UI/settings panel
- Fullscreen mode and window resizing
- Multiple color themes
- Beat detection and reactive effects
