#!/usr/bin/env python3
"""Lucky Reels — colourful three-reel slot machine."""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from games.theme import CYAN, GOLD, INK, LIME, MAGENTA, NAVY, ORANGE, PANEL, RED, WHITE, draw_vertical_gradient, pill, text

W, H = 960, 540
SYMBOLS = [
    ("7", RED, 12),
    ("★", GOLD, 8),
    ("◆", MAGENTA, 6),
    ("●", CYAN, 4),
    ("♣", LIME, 3),
    ("♪", ORANGE, 2),
]


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lucky Reels — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    huge = pygame.font.SysFont("segoe ui symbol", 72, bold=True)
    big = pygame.font.SysFont("consolas", 36, bold=True)

    bank = 150
    bet = 5
    reels = [0, 1, 2]
    spinning = [0, 0, 0]
    message = "Pull the lever"
    spin_btn = pygame.Rect(400, 450, 160, 52)
    minus = pygame.Rect(200, 450, 60, 52)
    plus = pygame.Rect(280, 450, 60, 52)

    def payout(combo):
        names = [SYMBOLS[i][0] for i in combo]
        if names[0] == names[1] == names[2]:
            return SYMBOLS[combo[0]][2] * bet
        if names[0] == names[1] or names[1] == names[2] or names[0] == names[2]:
            return bet
        return 0

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if spin_btn.collidepoint(event.pos) and not any(spinning) and bank >= bet:
                    bank -= bet
                    spinning = [18 + i * 8 for i in range(3)]
                    message = "Good luck..."
                elif minus.collidepoint(event.pos) and not any(spinning):
                    bet = max(1, bet - 1)
                elif plus.collidepoint(event.pos) and not any(spinning):
                    bet = min(20, bet + 1, bank if bank else 1)

        for i in range(3):
            if spinning[i] > 0:
                if spinning[i] % 2 == 0:
                    reels[i] = random.randrange(len(SYMBOLS))
                spinning[i] -= 1
                if spinning[i] == 0 and i == 2:
                    win = payout(reels)
                    bank += win
                    message = f"WIN ${win}!" if win else "No line — try again"

        draw_vertical_gradient(screen, (40, 8, 40), NAVY)
        text(screen, big, "LUCKY REELS", GOLD, (W // 2, 36), center=True)
        text(screen, font, "ElbowOS casino floor", CYAN, (W // 2, 72), center=True)

        machine = pygame.Rect(170, 110, 620, 300)
        pygame.draw.rect(screen, (50, 20, 70), machine, border_radius=24)
        pygame.draw.rect(screen, GOLD, machine, 4, border_radius=24)

        for i, idx in enumerate(reels):
            box = pygame.Rect(210 + i * 190, 160, 160, 200)
            pygame.draw.rect(screen, INK, box, border_radius=16)
            pygame.draw.rect(screen, CYAN if spinning[i] else GOLD, box, 3, border_radius=16)
            glyph, color, _ = SYMBOLS[idx]
            img = huge.render(glyph, True, color)
            screen.blit(img, img.get_rect(center=box.center))

        text(screen, font, f"BANK ${bank}", WHITE, (200, 424))
        text(screen, font, message, GOLD, (W // 2, 424), center=True)

        pill(screen, minus, PANEL, WHITE)
        pill(screen, plus, PANEL, WHITE)
        pill(screen, spin_btn, PANEL, MAGENTA if not any(spinning) else CYAN)
        text(screen, font, "-", WHITE, minus.center, center=True)
        text(screen, font, "+", WHITE, plus.center, center=True)
        text(screen, font, f"SPIN ${bet}", GOLD, spin_btn.center, center=True)

        pay = "PAY: 777 x12   ★★★ x8   pair x1"
        text(screen, font, pay, WHITE, (W // 2, 520), center=True)
        pygame.display.flip()


if __name__ == "__main__":
    run()
