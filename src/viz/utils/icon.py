"""
Application icon generation for the Viz visualizer.
"""
import pygame


def create_app_icon(size=64):
    """
    Create a simple application icon for the window.

    Args:
        size: Icon size in pixels (default 64x64)

    Returns:
        pygame.Surface with the icon
    """
    icon = pygame.Surface((size, size))
    icon.fill((10, 10, 20))  # Dark background

    # Draw a stylized waveform/spectrum visualization icon
    # Create three "bars" of different heights to represent frequency spectrum
    bar_width = size // 5
    gap = size // 10

    # Low frequency (tallest bar) - pale blue
    pygame.draw.rect(
        icon,
        (173, 216, 230),
        (gap, size // 3, bar_width, size * 2 // 3 - gap),
    )

    # Mid frequency (medium bar)
    pygame.draw.rect(
        icon,
        (173, 216, 230),
        (gap * 2 + bar_width, size // 2, bar_width, size // 2 - gap),
    )

    # High frequency (shortest bar)
    pygame.draw.rect(
        icon,
        (173, 216, 230),
        (gap * 3 + bar_width * 2, size * 2 // 3, bar_width, size // 3 - gap),
    )

    # Add a subtle glow effect around the bars
    for i in range(3):
        x_offset = gap + (gap + bar_width) * i
        y_start = size // 3 + i * size // 6
        height = size * 2 // 3 - gap - i * size // 6

        # Draw semi-transparent glow
        glow_surface = pygame.Surface((bar_width + 4, height + 4), pygame.SRCALPHA)
        pygame.draw.rect(
            glow_surface,
            (173, 216, 230, 60),
            (0, 0, bar_width + 4, height + 4),
            border_radius=2,
        )
        icon.blit(glow_surface, (x_offset - 2, y_start - 2))

    return icon
