#!/usr/bin/env python3
"""Roulette Royale — colourful European roulette table."""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from games.theme import BLACK, CYAN, GOLD, GREEN, INK, PANEL, RED, WHITE, draw_vertical_gradient, pill, text

W, H = 960, 540
WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
         5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
RED_SET = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


def color_of(n):
    if n == 0:
        return GREEN
    return RED if n in RED_SET else BLACK


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Roulette Royale — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    big = pygame.font.SysFont("consolas", 32, bold=True)

    bank = 200
    bet_amt = 10
    choice = "red"
    spinning = False
    angle = 0.0
    vel = 0.0
    result = None
    message = "Pick a colour, then spin"
    history = []

    btns = {
        "red": pygame.Rect(620, 80, 140, 48),
        "black": pygame.Rect(780, 80, 140, 48),
        "even": pygame.Rect(620, 140, 140, 48),
        "odd": pygame.Rect(780, 140, 140, 48),
        "zero": pygame.Rect(620, 200, 140, 48),
        "spin": pygame.Rect(780, 200, 140, 48),
        "minus": pygame.Rect(620, 260, 140, 48),
        "plus": pygame.Rect(780, 260, 140, 48),
    }

    number_cells = []
    for n in range(1, 37):
        col = (n - 1) % 6
        row = (n - 1) // 6
        number_cells.append((n, pygame.Rect(620 + col * 50, 330 + row * 32, 46, 28)))

    def wins(n):
        if choice == "red":
            return n in RED_SET
        if choice == "black":
            return n != 0 and n not in RED_SET
        if choice == "even":
            return n != 0 and n % 2 == 0
        if choice == "odd":
            return n % 2 == 1
        if choice == "0":
            return n == 0
        if isinstance(choice, int):
            return n == choice
        return False

    def payout_mult():
        if isinstance(choice, int) or choice == "0":
            return 36
        return 2

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not spinning:
                p = event.pos
                if btns["red"].collidepoint(p):
                    choice = "red"
                elif btns["black"].collidepoint(p):
                    choice = "black"
                elif btns["even"].collidepoint(p):
                    choice = "even"
                elif btns["odd"].collidepoint(p):
                    choice = "odd"
                elif btns["zero"].collidepoint(p):
                    choice = "0"
                elif btns["minus"].collidepoint(p):
                    bet_amt = max(5, bet_amt - 5)
                elif btns["plus"].collidepoint(p):
                    bet_amt = min(50, bet_amt + 5)
                elif btns["spin"].collidepoint(p) and bank >= bet_amt:
                    bank -= bet_amt
                    spinning = True
                    vel = 12 + random.random() * 6
                    result = None
                    message = "Ball in motion..."
                else:
                    for n, r in number_cells:
                        if r.collidepoint(p):
                            choice = n

        if spinning:
            angle = (angle + vel) % 360
            vel *= 0.985
            if vel < 0.12:
                spinning = False
                idx = int((-angle % 360) / (360 / 37)) % 37
                result = WHEEL[idx]
                history = ([result] + history)[:8]
                if wins(result):
                    win = bet_amt * payout_mult()
                    bank += win
                    message = f"{result} hits — you win ${win}"
                else:
                    message = f"{result} — house takes the chip"

        draw_vertical_gradient(screen, (20, 8, 24), (8, 20, 16))
        text(screen, big, "ROULETTE ROYALE", GOLD, (300, 28), center=True)
        text(screen, font, f"BANK ${bank}   BET ${bet_amt}   ON {choice}", WHITE, (300, 58), center=True)

        cx, cy, rad = 300, 300, 200
        pygame.draw.circle(screen, GOLD, (cx, cy), rad + 8)
        pygame.draw.circle(screen, INK, (cx, cy), rad)
        for i, n in enumerate(WHEEL):
            a0 = math.radians(i * (360 / 37) + angle)
            a1 = math.radians((i + 1) * (360 / 37) + angle)
            pts = [(cx, cy),
                   (cx + rad * math.cos(a0), cy + rad * math.sin(a0)),
                   (cx + rad * math.cos(a1), cy + rad * math.sin(a1))]
            pygame.draw.polygon(screen, color_of(n), pts)
        pygame.draw.circle(screen, INK, (cx, cy), 48)
        pygame.draw.circle(screen, GOLD, (cx, cy), 48, 2)
        pygame.draw.circle(screen, WHITE, (cx, cy - rad + 18), 8)
        if result is not None:
            text(screen, big, str(result), GOLD, (cx, cy), center=True)

        labels = [
            ("red", "RED", RED),
            ("black", "BLACK", WHITE),
            ("even", "EVEN", CYAN),
            ("odd", "ODD", CYAN),
            ("zero", "0", GREEN),
            ("spin", "SPIN", GOLD),
            ("minus", "BET -", WHITE),
            ("plus", "BET +", WHITE),
        ]
        for key, label, col in labels:
            active = (key == "red" and choice == "red") or (key == "black" and choice == "black") or (
                key == "even" and choice == "even") or (key == "odd" and choice == "odd") or (
                key == "zero" and choice == "0")
            fill = PANEL if not active else (50, 40, 20)
            pill(screen, btns[key], fill, col)
            text(screen, font, label, col, btns[key].center, center=True)

        for n, r in number_cells:
            pygame.draw.rect(screen, color_of(n), r, border_radius=4)
            if choice == n:
                pygame.draw.rect(screen, GOLD, r, 2, border_radius=4)
            text(screen, font, str(n), WHITE, r.center, center=True)

        text(screen, font, message, GOLD, (300, 520), center=True)
        if history:
            text(screen, font, "LAST " + " ".join(str(x) for x in history), WHITE, (20, 500))
        pygame.display.flip()


if __name__ == "__main__":
    run()
