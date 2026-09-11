#!/usr/bin/env python3
"""Lumen Leap — original colourful platformer (not a Mario clone or emulator)."""

from __future__ import annotations

import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from games.theme import CYAN, GOLD, LIME, MAGENTA, NAVY, ORANGE, RED, WHITE, draw_vertical_gradient, text

W, H = 960, 540
TILE = 48
GRAVITY = 0.55
JUMP = -11.5
SPEED = 5.2

LEVEL = [
    "................................................................",
    "................................................................",
    "................o................o................o.............",
    "..............####............######.............###............",
    "........o.......................................................",
    "......####..............o...........e...............o...........",
    ".....................######......................######.........",
    "....o..........e................o........e.................F....",
    "##################....##############....########################",
]


class Actor:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False

    def move(self, solids):
        self.rect.x += int(self.vx)
        for s in solids:
            if self.rect.colliderect(s):
                if self.vx > 0:
                    self.rect.right = s.left
                elif self.vx < 0:
                    self.rect.left = s.right
                self.vx = 0
        self.rect.y += int(self.vy)
        self.on_ground = False
        for s in solids:
            if self.rect.colliderect(s):
                if self.vy > 0:
                    self.rect.bottom = s.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = s.bottom
                self.vy = 0


def parse_level():
    solids, coins, enemies, flag = [], [], [], None
    for r, row in enumerate(LEVEL):
        for c, ch in enumerate(row):
            x, y = c * TILE, r * TILE
            if ch == "#":
                solids.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == "o":
                coins.append(pygame.Rect(x + 16, y + 16, 16, 16))
            elif ch == "e":
                enemies.append({"rect": pygame.Rect(x + 8, y + 16, 32, 32), "dir": 1, "base": x})
            elif ch == "F":
                flag = pygame.Rect(x + 8, y - 48, 24, 96)
    return solids, coins, enemies, flag


def draw_player(surf, rect, facing):
    body = rect.inflate(-6, -4)
    pygame.draw.rect(surf, CYAN, body, border_radius=8)
    pygame.draw.rect(surf, WHITE, body, 2, border_radius=8)
    eye_x = body.centerx + (6 if facing > 0 else -10)
    pygame.draw.circle(surf, NAVY, (eye_x, body.y + 12), 4)
    pygame.draw.circle(surf, WHITE, (eye_x + 1, body.y + 11), 2)


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lumen Leap — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 42, bold=True)

    solids, coins, enemies, flag = parse_level()
    player = Actor(80, 200, 36, 44)
    cam_x = 0
    score = 0
    lives = 3
    won = False
    dead_timer = 0
    facing = 1
    spawn = (80, 200)

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                if player.on_ground and not won:
                    player.vy = JUMP

        keys = pygame.key.get_pressed()
        player.vx = 0
        if not won and dead_timer <= 0:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.vx = -SPEED
                facing = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.vx = SPEED
                facing = 1

        if dead_timer > 0:
            dead_timer -= dt
            if dead_timer <= 0:
                player.rect.topleft = spawn
                player.vx = player.vy = 0
        else:
            player.vy = min(player.vy + GRAVITY, 14)
            player.move(solids)

        for e in enemies:
            e["rect"].x += e["dir"] * 2
            if abs(e["rect"].x - e["base"]) > 80:
                e["dir"] *= -1
            if dead_timer <= 0 and not won and player.rect.colliderect(e["rect"]):
                if player.vy > 1 and player.rect.bottom - e["rect"].top < 18:
                    e["rect"].y = 9999
                    player.vy = JUMP * 0.6
                    score += 50
                else:
                    lives -= 1
                    dead_timer = 700
                    if lives <= 0:
                        lives = 3
                        score = 0
                        solids, coins, enemies, flag = parse_level()

        remaining = []
        for coin in coins:
            if player.rect.colliderect(coin):
                score += 10
            else:
                remaining.append(coin)
        coins = remaining

        if flag and player.rect.colliderect(flag):
            won = True

        if player.rect.top > H + 80 and dead_timer <= 0:
            lives -= 1
            dead_timer = 700
            if lives <= 0:
                lives = 3
                score = 0
                solids, coins, enemies, flag = parse_level()

        cam_x = max(0, player.rect.centerx - W // 3)

        draw_vertical_gradient(screen, (18, 12, 48), (255, 120, 80))
        for i in range(8):
            pygame.draw.circle(screen, (255, 255, 255), (80 + i * 140 - (cam_x // 8) % 140, 40 + (i % 3) * 18), 2)

        def wx(x):
            return x - cam_x

        for s in solids:
            r = pygame.Rect(wx(s.x), s.y, s.w, s.h)
            pygame.draw.rect(screen, (90, 60, 180), r, border_radius=6)
            pygame.draw.rect(screen, MAGENTA, r, 2, border_radius=6)
            pygame.draw.line(screen, (160, 120, 255), (r.x + 6, r.y + 8), (r.right - 6, r.y + 8), 2)

        for coin in coins:
            pygame.draw.circle(screen, GOLD, (wx(coin.centerx), coin.centery), 9)
            pygame.draw.circle(screen, ORANGE, (wx(coin.centerx), coin.centery), 9, 2)

        for e in enemies:
            if e["rect"].y > 800:
                continue
            r = pygame.Rect(wx(e["rect"].x), e["rect"].y, e["rect"].w, e["rect"].h)
            pygame.draw.ellipse(screen, RED, r)
            pygame.draw.ellipse(screen, WHITE, r, 2)
            pygame.draw.circle(screen, WHITE, (r.centerx - 6, r.y + 12), 4)
            pygame.draw.circle(screen, WHITE, (r.centerx + 6, r.y + 12), 4)

        if flag:
            fx = wx(flag.x)
            pygame.draw.rect(screen, WHITE, (fx + 4, flag.y, 4, flag.h))
            pygame.draw.polygon(screen, LIME, [(fx + 8, flag.y), (fx + 40, flag.y + 16), (fx + 8, flag.y + 32)])

        draw_player(screen, pygame.Rect(wx(player.rect.x), player.rect.y, player.rect.w, player.rect.h), facing)

        text(screen, font, f"SCORE {score:04d}   LIVES {lives}", WHITE, (16, 12))
        text(screen, font, "LUMEN LEAP  •  ElbowOS", CYAN, (W - 280, 12))
        if won:
            text(screen, big, "CLEAR!", GOLD, (W // 2, H // 2 - 20), center=True)
            text(screen, font, "You reached the beacon.", WHITE, (W // 2, H // 2 + 24), center=True)

        pygame.display.flip()


if __name__ == "__main__":
    run()
