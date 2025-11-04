"""
Isometric projection module for converting 3D coordinates to 2D screen space.
"""
import numpy as np
from ..utils import config


class IsometricProjection:
    """Handles 3D to 2D isometric projection."""

    def __init__(self, width, height):
        """
        Initialize the isometric projection.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2

        # Pre-calculate rotation matrices
        angle_rad = np.radians(config.ISO_ANGLE)
        self.cos_angle = np.cos(angle_rad)
        self.sin_angle = np.sin(angle_rad)

    def project(self, x, y, z):
        """
        Project a 3D point to 2D screen coordinates.

        For isometric view:
        - X-axis goes right-up
        - Y-axis goes up
        - Z-axis goes left-up

        Args:
            x: X coordinate (frequency band)
            y: Y coordinate (amplitude)
            z: Z coordinate (time slice)

        Returns:
            Tuple of (screen_x, screen_y)
        """
        # Scale the coordinates
        scaled_x = x * config.SCALE_X
        scaled_y = y * config.SCALE_Y
        scaled_z = z * config.SCALE_Z

        # Isometric projection formula
        screen_x = (scaled_x - scaled_z) * self.cos_angle
        screen_y = scaled_y - (scaled_x + scaled_z) * self.sin_angle

        # Translate to screen center
        screen_x += self.center_x
        screen_y = self.center_y - screen_y  # Flip Y (screen coords go down)

        return int(screen_x), int(screen_y)

    def project_points(self, points):
        """
        Project multiple 3D points to 2D screen coordinates.

        Args:
            points: NumPy array of shape (N, 3) with columns [x, y, z]

        Returns:
            NumPy array of shape (N, 2) with screen coordinates
        """
        if len(points) == 0:
            return np.array([])

        # Scale
        scaled = points * np.array(
            [config.SCALE_X, config.SCALE_Y, config.SCALE_Z]
        )

        # Project
        screen_x = (scaled[:, 0] - scaled[:, 2]) * self.cos_angle
        screen_y = scaled[:, 1] - (scaled[:, 0] + scaled[:, 2]) * self.sin_angle

        # Translate
        screen_x += self.center_x
        screen_y = self.center_y - screen_y

        return np.column_stack([screen_x, screen_y]).astype(int)
