#!/usr/bin/env python3
"""ElbowOS Color Arcade launcher."""

from __future__ import annotations

import pygame

from games.theme import CYAN, GOLD, INK, LIME, MAGENTA, NAVY, ORANGE, PANEL, WHITE, draw_vertical_gradient, pill, text
from games import lumen_leap, neon_blackjack, lucky_reels, roulette_royale, prism_klondike

W, H = 960, 540
GAMES = [
    ("Lumen Leap", "Original neon platformer", lumen_leap.run, MAGENTA),
    ("Neon Blackjack", "Casino twenty-one", neon_blackjack.run, LIME),
    ("Lucky Reels", "Three-reel slots", lucky_reels.run, ORANGE),
    ("Roulette Royale", "European wheel", roulette_royale.run, CYAN),
    ("Prism Klondike", "Colour solitaire", prism_klondike.run, GOLD),
]


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("ElbowOS Color Arcade")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("consolas", 44, bold=True)
    font = pygame.font.SysFont("consolas", 22)
    small = pygame.font.SysFont("consolas", 16)

    cards = []
    for i, (name, blurb, fn, col) in enumerate(GAMES):
        x = 40 + (i % 3) * 300
        y = 140 + (i // 3) * 160
        cards.append((pygame.Rect(x, y, 280, 140), name, blurb, fn, col))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, name, blurb, fn, col in cards:
                    if rect.collidepoint(event.pos):
                        pygame.quit()
                        fn()
                        return main()

        draw_vertical_gradient(screen, NAVY, (28, 10, 48))
        text(screen, title, "ELBOWOS COLOR ARCADE", GOLD, (W // 2, 48), center=True)
        text(screen, font, "Full-colour Python 3 games  •  x.com/ElbowOS", CYAN, (W // 2, 92), center=True)

        mouse = pygame.mouse.get_pos()
        for rect, name, blurb, fn, col in cards:
            fill = (36, 28, 70) if rect.collidepoint(mouse) else PANEL
            pill(screen, rect, fill, col, radius=18)
            text(screen, font, name, col, (rect.centerx, rect.centery - 16), center=True)
            text(screen, small, blurb, WHITE, (rect.centerx, rect.centery + 18), center=True)

        text(screen, small, "Click a cabinet  •  Esc quits a game", WHITE, (W // 2, 520), center=True)
        pygame.display.flip()


if __name__ == "__main__":
    main()
