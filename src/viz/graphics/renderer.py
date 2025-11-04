"""
Graphics renderer module for drawing the 3D audio visualization.
"""
import pygame
import numpy as np
from collections import deque
from .isometric import IsometricProjection
from ..utils import config


class Renderer:
    """Handles all graphics rendering for the visualizer."""

    def __init__(self):
        """Initialize the renderer."""
        # Set up display
        flags = pygame.DOUBLEBUF
        if config.USE_HARDWARE_ACCELERATION:
            flags |= pygame.HWSURFACE

        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags, vsync=config.VSYNC
        )
        pygame.display.set_caption(config.WINDOW_TITLE)

        # Initialize projection
        self.projection = IsometricProjection(
            config.WINDOW_WIDTH, config.WINDOW_HEIGHT
        )

        # Time history buffer - stores spectrum data over time
        self.history = deque(maxlen=config.TIME_HISTORY_LENGTH)

        # Font for debug info
        self.font = pygame.font.Font(None, 24)

    def add_spectrum(self, spectrum):
        """
        Add a new spectrum to the history buffer.

        Args:
            spectrum: NumPy array of frequency band amplitudes
        """
        self.history.append(spectrum.copy())

    def render(self):
        """Render the current frame."""
        # Clear screen
        self.screen.fill(config.BACKGROUND_COLOR)

        # Draw visualization if we have data
        if len(self.history) > 0:
            self._draw_spectrum_lines()

        # Draw UI elements
        self._draw_ui()

        # Update display
        pygame.display.flip()

    def _draw_spectrum_lines(self):
        """Draw the 3D spectrum visualization."""
        # Draw from back to front for proper depth
        for time_idx in range(len(self.history)):
            spectrum = self.history[time_idx]
            z = time_idx  # Z coordinate is time index

            # Create points for this time slice
            points = []
            for freq_idx in range(len(spectrum)):
                x = freq_idx  # X coordinate is frequency band
                y = spectrum[freq_idx] * 100  # Scale amplitude for visibility

                # Project to screen coordinates
                screen_pos = self.projection.project(x, y, z)
                points.append(screen_pos)

            # Draw lines connecting the frequency bands
            if len(points) > 1:
                # Fade older time slices
                alpha = int(255 * (time_idx + 1) / len(self.history))
                color = (
                    config.LINE_COLOR[0] * alpha // 255,
                    config.LINE_COLOR[1] * alpha // 255,
                    config.LINE_COLOR[2] * alpha // 255,
                )

                # Draw the spectrum line
                pygame.draw.lines(
                    self.screen, color, False, points, config.LINE_THICKNESS
                )

                # Draw connection to previous time slice for waterfall effect
                if time_idx > 0:
                    prev_spectrum = self.history[time_idx - 1]
                    for freq_idx in range(len(spectrum)):
                        x = freq_idx
                        y1 = spectrum[freq_idx] * 100
                        y2 = prev_spectrum[freq_idx] * 100

                        pos1 = self.projection.project(x, y1, time_idx)
                        pos2 = self.projection.project(x, y2, time_idx - 1)

                        pygame.draw.line(
                            self.screen, color, pos1, pos2, config.LINE_THICKNESS // 2
                        )

    def _draw_ui(self):
        """Draw UI elements like FPS counter."""
        # FPS counter
        fps = int(pygame.time.Clock().get_fps())
        fps_text = self.font.render(f"FPS: {fps}", True, (100, 100, 100))
        self.screen.blit(fps_text, (10, 10))

        # Buffer status
        buffer_text = self.font.render(
            f"Buffer: {len(self.history)}/{config.TIME_HISTORY_LENGTH}",
            True,
            (100, 100, 100),
        )
        self.screen.blit(buffer_text, (10, 35))

    def close(self):
        """Clean up resources."""
        pygame.quit()
