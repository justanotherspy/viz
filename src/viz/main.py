"""
Main entry point for the Viz 3D audio visualizer.
"""
import sys
import numpy as np
import pygame

from .audio.capture import AudioCapture
from .audio.analyzer import AudioAnalyzer
from .graphics.renderer import Renderer
from .utils.icon import create_app_icon
from .utils import config


class Visualizer:
    """Main visualizer application class."""

    def __init__(self):
        """Initialize the visualizer application."""
        self.running = False
        self.clock = pygame.time.Clock()

        # Initialize pygame
        pygame.init()

        # Set window icon before creating the window
        icon = create_app_icon()
        pygame.display.set_icon(icon)

        # Initialize renderer (creates the window)
        print("Initializing renderer...")
        self.renderer = Renderer()

        # Initialize audio components
        print("Initializing audio capture...")
        try:
            self.audio_capture = AudioCapture()
            self.audio_analyzer = AudioAnalyzer()
            self.use_audio = True

            # Try to start audio capture
            try:
                self.audio_capture.start()
                print("✓ Audio capture started successfully")
            except RuntimeError as e:
                print(f"⚠ Warning: {e}")
                print("⚠ Running in demo mode with generated audio")
                self.use_audio = False
        except Exception as e:
            print(f"⚠ Warning: Failed to initialize audio: {e}")
            print("⚠ Running in demo mode with generated audio")
            self.use_audio = False
            self.audio_capture = None
            self.audio_analyzer = AudioAnalyzer()

        # Demo mode variables
        self.demo_time = 0
        self.demo_phase = 0

    def _generate_demo_audio(self):
        """Generate demo audio data for testing when no audio device is available."""
        # Create a mix of sine waves at different frequencies
        t = np.linspace(
            self.demo_time,
            self.demo_time + config.CHUNK_SIZE / config.SAMPLE_RATE,
            config.CHUNK_SIZE,
        )

        # Base frequencies for demo
        freq1 = 200 + 100 * np.sin(self.demo_phase)
        freq2 = 800 + 400 * np.sin(self.demo_phase * 0.7)
        freq3 = 3000 + 1000 * np.sin(self.demo_phase * 0.5)

        # Generate mixed signal
        audio = (
            0.3 * np.sin(2 * np.pi * freq1 * t)
            + 0.2 * np.sin(2 * np.pi * freq2 * t)
            + 0.15 * np.sin(2 * np.pi * freq3 * t)
        )

        # Add some randomness
        audio += 0.05 * np.random.randn(config.CHUNK_SIZE)

        self.demo_time += config.CHUNK_SIZE / config.SAMPLE_RATE
        self.demo_phase += 0.05

        return audio.astype(np.float32)

    def run(self):
        """Run the main application loop."""
        self.running = True
        print("\n" + "=" * 50)
        print("Viz is running!")
        print("=" * 50)
        if not self.use_audio:
            print("Mode: DEMO (no audio device connected)")
        else:
            print("Mode: LIVE AUDIO")
        print("\nControls:")
        print("  - Close window or press Ctrl+C to exit")
        print("=" * 50 + "\n")

        try:
            while self.running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

                # Get audio data
                if self.use_audio and self.audio_capture:
                    audio_data = self.audio_capture.read_chunk()
                else:
                    # Use demo audio
                    audio_data = self._generate_demo_audio()

                # Analyze audio
                if audio_data is not None:
                    spectrum = self.audio_analyzer.analyze(audio_data)
                    self.renderer.add_spectrum(spectrum)

                # Render frame
                self.renderer.render()

                # Maintain target FPS
                self.clock.tick(config.FPS_TARGET)

        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal...")
        except Exception as e:
            print(f"\n\nError in main loop: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self.shutdown()

    def shutdown(self):
        """Clean up and shut down the application."""
        print("Shutting down...")

        # Stop audio
        if self.audio_capture:
            try:
                self.audio_capture.close()
                print("✓ Audio capture closed")
            except Exception as e:
                print(f"⚠ Error closing audio: {e}")

        # Clean up pygame
        try:
            pygame.quit()
            print("✓ Graphics closed")
        except Exception as e:
            print(f"⚠ Error closing graphics: {e}")

        print("Goodbye!")


def main():
    """Main entry point for the visualizer application."""
    print("\n" + "=" * 50)
    print("Viz - 3D Audio Visualizer")
    print("=" * 50)
    print("Initializing...\n")

    try:
        app = Visualizer()
        app.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
