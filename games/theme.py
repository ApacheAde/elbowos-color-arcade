"""Shared neon palette for ElbowOS Color Arcade."""

NAVY = (8, 10, 28)
INK = (14, 16, 42)
PANEL = (22, 24, 58)
CYAN = (0, 230, 255)
MAGENTA = (255, 70, 180)
GOLD = (255, 210, 60)
LIME = (90, 255, 120)
ORANGE = (255, 140, 40)
WHITE = (245, 247, 255)
MUTED = (160, 170, 210)
RED = (255, 70, 90)
BLACK = (12, 12, 18)
GREEN = (30, 170, 90)
BLUE = (60, 110, 255)
PURPLE = (150, 90, 255)


def draw_vertical_gradient(surface, top, bottom):
    import pygame

    h = surface.get_height()
    w = surface.get_width()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        )
        pygame.draw.line(surface, c, (0, y), (w, y))


def pill(surface, rect, fill, border=CYAN, radius=14):
    import pygame

    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 2, border_radius=radius)


def text(surface, font, s, color, pos, center=False):
    img = font.render(s, True, color)
    rect = img.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(img, rect)
    return rect
