# ElbowOS Color Arcade

Full-colour **Python 3** games for [ElbowOS](https://x.com/ElbowOS).

These are **original** arcade and table games — not ROM emulators and not Nintendo titles. A real Mario Bros. emulator would need a legally owned dump of copyrighted software; that is not included.

## Games

| Game | File | Genre |
| --- | --- | --- |
| Lumen Leap | `games/lumen_leap.py` | Side-scrolling platformer |
| Neon Blackjack | `games/neon_blackjack.py` | Casino card game |
| Lucky Reels | `games/lucky_reels.py` | Slot machine |
| Roulette Royale | `games/roulette_royale.py` | European roulette |
| Prism Klondike | `games/prism_klondike.py` | Solitaire card game |

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 launcher.py
```

Or run any title directly:

```bash
python3 games/lumen_leap.py
```

## Controls

Shared across most titles: **mouse** to click buttons, **Esc** to quit.

- **Lumen Leap** — A/D or arrows to move, Space/W/Up to jump
- **Blackjack / Slots / Roulette / Klondike** — on-screen buttons and card clicks

## Credit

Published for **[x.com/ElbowOS](https://x.com/ElbowOS)** · GitHub: [ApacheAde](https://github.com/ApacheAde)
