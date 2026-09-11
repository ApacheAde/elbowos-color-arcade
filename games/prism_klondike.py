#!/usr/bin/env python3
"""Prism Klondike — colourful solitaire."""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from games.theme import CYAN, GOLD, INK, MAGENTA, NAVY, PANEL, RED, WHITE, draw_vertical_gradient, pill, text

W, H = 960, 540
SUITS = [("\u2665", RED), ("\u2666", MAGENTA), ("\u2663", CYAN), ("\u2660", WHITE)]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
RANK_I = {r: i for i, r in enumerate(RANKS)}
CW, CH = 78, 104


class Card:
    def __init__(self, rank, suit, color):
        self.rank = rank
        self.suit = suit
        self.color = color
        self.face = False

    def red(self):
        return self.color in (RED, MAGENTA)


def make_deck():
    deck = [Card(r, s, c) for r in RANKS for s, c in SUITS]
    random.shuffle(deck)
    return deck


def draw_card(surf, font, card, x, y, selected=False):
    rect = pygame.Rect(x, y, CW, CH)
    if card is None:
        pygame.draw.rect(surf, PANEL, rect, border_radius=8)
        pygame.draw.rect(surf, CYAN, rect, 1, border_radius=8)
        return rect
    if not card.face:
        pygame.draw.rect(surf, INK, rect, border_radius=8)
        pygame.draw.rect(surf, MAGENTA, rect.inflate(-12, -12), border_radius=6)
        pygame.draw.rect(surf, GOLD, rect, 2, border_radius=8)
        return rect
    pygame.draw.rect(surf, WHITE, rect, border_radius=8)
    pygame.draw.rect(surf, GOLD if selected else INK, rect, 2, border_radius=8)
    label = font.render(f"{card.rank}{card.suit}", True, card.color)
    surf.blit(label, (x + 6, y + 6))
    return rect


def can_stack(moving, onto):
    if onto is None:
        return moving.rank == "K"
    return moving.red() != onto.red() and RANK_I[onto.rank] - RANK_I[moving.rank] == 1


def can_foundation(moving, pile):
    if not pile:
        return moving.rank == "A"
    top = pile[-1]
    return moving.suit == top.suit and RANK_I[moving.rank] - RANK_I[top.rank] == 1


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Prism Klondike — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoe ui symbol", 18)
    ui = pygame.font.SysFont("consolas", 20)

    def deal():
        deck = make_deck()
        tableau = [[] for _ in range(7)]
        for col in range(7):
            for n in range(col + 1):
                card = deck.pop()
                card.face = n == col
                tableau[col].append(card)
        return deck, [], tableau, [[] for _ in range(4)]

    stock, waste, tableau, foundations = deal()
    selected = None
    new_btn = pygame.Rect(20, 490, 120, 36)
    stock_rect = pygame.Rect(20, 70, CW, CH)
    waste_rect = pygame.Rect(110, 70, CW, CH)
    found_rects = [pygame.Rect(420 + i * 90, 70, CW, CH) for i in range(4)]

    def tab_pos(col, idx):
        return 20 + col * 135, 200 + idx * 22

    def hit_test(pos):
        if stock_rect.collidepoint(pos):
            return ("stock",)
        if waste and waste_rect.collidepoint(pos):
            return ("w",)
        for i, r in enumerate(found_rects):
            if r.collidepoint(pos):
                return ("f", i)
        for col, pile in enumerate(tableau):
            if not pile:
                r = pygame.Rect(*tab_pos(col, 0), CW, CH)
                if r.collidepoint(pos):
                    return ("t", col, 0)
                continue
            for idx in range(len(pile) - 1, -1, -1):
                r = pygame.Rect(*tab_pos(col, idx), CW, CH)
                if r.collidepoint(pos):
                    return ("t", col, idx)
        return None

    def stack_from(sel):
        if sel[0] == "w":
            return [waste[-1]] if waste else []
        if sel[0] == "t":
            _, col, idx = sel
            if tableau[col][idx].face:
                return tableau[col][idx:]
        return []

    def remove_from(sel, n):
        if sel[0] == "w":
            waste.pop()
        elif sel[0] == "t":
            _, col, idx = sel
            del tableau[col][idx:]
            if tableau[col] and not tableau[col][-1].face:
                tableau[col][-1].face = True

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
                if new_btn.collidepoint(event.pos):
                    stock, waste, tableau, foundations = deal()
                    selected = None
                    continue
                hit = hit_test(event.pos)
                if hit is None:
                    selected = None
                    continue
                if hit[0] == "stock":
                    if stock:
                        c = stock.pop()
                        c.face = True
                        waste.append(c)
                    elif waste:
                        stock = waste[::-1]
                        for c in stock:
                            c.face = False
                        waste = []
                    selected = None
                    continue
                if selected is None:
                    if hit[0] in ("w", "t"):
                        selected = hit
                    continue
                moving = stack_from(selected)
                if not moving:
                    selected = None
                    continue
                placed = False
                if hit[0] == "f" and len(moving) == 1 and can_foundation(moving[0], foundations[hit[1]]):
                    foundations[hit[1]].append(moving[0])
                    remove_from(selected, 1)
                    placed = True
                elif hit[0] == "t":
                    dest = tableau[hit[1]]
                    onto = dest[-1] if dest else None
                    if can_stack(moving[0], onto):
                        dest.extend(moving)
                        remove_from(selected, len(moving))
                        placed = True
                selected = None if placed else hit

        draw_vertical_gradient(screen, (12, 24, 48), NAVY)
        text(screen, ui, "PRISM KLONDIKE  •  ElbowOS", GOLD, (20, 16))
        won = all(len(f) == 13 for f in foundations)
        text(screen, ui, "CLEARED!" if won else "Build A->K by suit  •  alternate colours on the table", WHITE, (20, 42))

        if stock:
            stock_dummy = Card("", "", WHITE)
            stock_dummy.face = False
            draw_card(screen, font, stock_dummy, stock_rect.x, stock_rect.y)
        else:
            draw_card(screen, font, None, stock_rect.x, stock_rect.y)
        if waste:
            draw_card(screen, font, waste[-1], waste_rect.x, waste_rect.y, selected=(selected == ("w",)))
        else:
            draw_card(screen, font, None, waste_rect.x, waste_rect.y)

        for i, pile in enumerate(foundations):
            draw_card(screen, font, pile[-1] if pile else None, found_rects[i].x, found_rects[i].y)

        for col, pile in enumerate(tableau):
            if not pile:
                draw_card(screen, font, None, *tab_pos(col, 0))
            for idx, card in enumerate(pile):
                sel = selected == ("t", col, idx) or (
                    selected and selected[0] == "t" and selected[1] == col and idx >= selected[2]
                )
                draw_card(screen, font, card, *tab_pos(col, idx), selected=bool(sel and card.face))

        pill(screen, new_btn, PANEL, GOLD)
        text(screen, ui, "NEW DEAL", GOLD, new_btn.center, center=True)
        pygame.display.flip()


if __name__ == "__main__":
    run()
