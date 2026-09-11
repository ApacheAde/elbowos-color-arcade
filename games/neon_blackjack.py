#!/usr/bin/env python3
"""Neon Blackjack — colourful casino card game."""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from games.theme import CYAN, GOLD, GREEN, INK, MAGENTA, PANEL, RED, WHITE, draw_vertical_gradient, pill, text

W, H = 960, 540
SUITS = [("\u2665", RED), ("\u2666", MAGENTA), ("\u2663", CYAN), ("\u2660", WHITE)]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def new_deck():
    deck = [(r, s, c) for r in RANKS for s, c in SUITS]
    random.shuffle(deck)
    return deck


def hand_value(hand):
    total, aces = 0, 0
    for r, _, _ in hand:
        if r == "A":
            total += 11
            aces += 1
        elif r in "JQK":
            total += 10
        else:
            total += int(r)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def draw_card(surf, font, card, x, y, hidden=False):
    rect = pygame.Rect(x, y, 86, 120)
    pygame.draw.rect(surf, WHITE if not hidden else INK, rect, border_radius=10)
    pygame.draw.rect(surf, GOLD, rect, 2, border_radius=10)
    if hidden:
        pygame.draw.rect(surf, MAGENTA, rect.inflate(-16, -16), border_radius=6)
        return rect
    rank, suit, color = card
    img = font.render(f"{rank}{suit}", True, color)
    surf.blit(img, (x + 8, y + 8))
    big = pygame.font.SysFont("segoe ui symbol", 36)
    s = big.render(suit, True, color)
    surf.blit(s, s.get_rect(center=rect.center))
    return rect


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Blackjack — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    card_font = pygame.font.SysFont("segoe ui symbol", 20)
    big = pygame.font.SysFont("consolas", 34, bold=True)

    bank = 200
    bet = 20
    deck = new_deck()
    player, dealer = [], []
    phase = "bet"
    message = "Place a bet"

    buttons = {
        "deal": pygame.Rect(40, 460, 120, 48),
        "hit": pygame.Rect(180, 460, 120, 48),
        "stand": pygame.Rect(320, 460, 120, 48),
        "minus": pygame.Rect(700, 460, 60, 48),
        "plus": pygame.Rect(860, 460, 60, 48),
    }

    def deal_card(to):
        nonlocal deck
        if len(deck) < 10:
            deck = new_deck()
        to.append(deck.pop())

    def start_hand():
        nonlocal player, dealer, phase, message, bank, bet
        if bet > bank:
            message = "Not enough chips"
            return
        bank -= bet
        player, dealer = [], []
        deal_card(player)
        deal_card(dealer)
        deal_card(player)
        deal_card(dealer)
        phase = "play"
        if hand_value(player) == 21:
            settle(True)
        else:
            message = "Hit or Stand"

    def settle(blackjack=False):
        nonlocal phase, message, bank
        phase = "settle"
        pv, dv = hand_value(player), hand_value(dealer)
        if blackjack and dv != 21:
            win = int(bet * 2.5)
            bank += win
            message = f"Blackjack! +{win}"
        elif pv > 21:
            message = "Bust"
        else:
            while hand_value(dealer) < 17:
                deal_card(dealer)
            dv = hand_value(dealer)
            if dv > 21 or pv > dv:
                bank += bet * 2
                message = f"You win +{bet * 2}"
            elif pv == dv:
                bank += bet
                message = "Push"
            else:
                message = "Dealer wins"

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
                if buttons["deal"].collidepoint(event.pos) and phase != "play":
                    start_hand()
                elif buttons["hit"].collidepoint(event.pos) and phase == "play":
                    deal_card(player)
                    if hand_value(player) >= 21:
                        settle()
                elif buttons["stand"].collidepoint(event.pos) and phase == "play":
                    settle()
                elif buttons["minus"].collidepoint(event.pos) and phase != "play":
                    bet = max(5, bet - 5)
                elif buttons["plus"].collidepoint(event.pos) and phase != "play":
                    bet = min(100, bet + 5, bank if bank else 5)

        draw_vertical_gradient(screen, (6, 40, 28), (8, 10, 28))
        pygame.draw.ellipse(screen, (20, 90, 50), (80, 70, 800, 360))
        pygame.draw.ellipse(screen, GOLD, (80, 70, 800, 360), 3)

        text(screen, big, "NEON BLACKJACK", GOLD, (W // 2, 28), center=True)
        text(screen, font, f"BANK ${bank}   BET ${bet}", WHITE, (W // 2, 62), center=True)
        text(screen, font, message, CYAN, (W // 2, 430), center=True)

        text(screen, font, "DEALER", WHITE, (140, 90))
        hide = phase == "play"
        for i, card in enumerate(dealer):
            draw_card(screen, card_font, card, 140 + i * 96, 118, hidden=(hide and i == 1))
        if phase != "play" and dealer:
            text(screen, font, f"{hand_value(dealer)}", GOLD, (140, 248))

        text(screen, font, "YOU", WHITE, (140, 280))
        for i, card in enumerate(player):
            draw_card(screen, card_font, card, 140 + i * 96, 308)
        if player:
            text(screen, font, f"{hand_value(player)}", GOLD, (140, 436))

        labels = [("deal", "DEAL", GREEN), ("hit", "HIT", CYAN), ("stand", "STAND", MAGENTA),
                  ("minus", "-", WHITE), ("plus", "+", WHITE)]
        for key, label, col in labels:
            pill(screen, buttons[key], PANEL, col)
            text(screen, font, label, col, buttons[key].center, center=True)
        pill(screen, pygame.Rect(770, 460, 80, 48), PANEL, GOLD)
        text(screen, font, f"${bet}", GOLD, (810, 484), center=True)

        pygame.display.flip()


if __name__ == "__main__":
    run()
