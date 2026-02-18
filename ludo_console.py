import random
from typing import List

# ------------------------------
# Simple Ludo (Console) Rules:
# - 2 to 4 players
# - One token per player
# - Need a 6 to enter the track from "home" (-1 -> 0)
# - Path length: 57 (0..56 on main loop + 1 final home position)
# - Roll 6 => get another turn
# - No captures, no safe squares (kept simple)
# ------------------------------

TRACK_LEN = 57  # reaching 57 means "home" (0..56 are steps, pos == 57 -> finished)

class Player:
    def __init__(self, name: str, color: str, start_offset: int):
        self.name = name
        self.color = color
        self.start_offset = start_offset  # Where your 0 maps on the shared loop (cosmetic for real Ludo)
        self.pos = -1  # -1 means still in base/home
        self.finished = False

    def __repr__(self):
        state = "FINISHED" if self.finished else ("BASE" if self.pos < 0 else str(self.pos))
        return f"{self.name}({self.color}): {state}"

def roll_dice() -> int:
    return random.randint(1, 6)

def can_enter(roll: int, pos: int) -> bool:
    # Must roll 6 to leave base
    return pos < 0 and roll == 6

def move_possible(pos: int, roll: int) -> bool:
    # If already on the board, can move if it doesn't overshoot final home
    if pos < 0:
        return False
    return (pos + roll) <= TRACK_LEN

def apply_move(player: Player, roll: int):
    if player.finished:
        return

    # Enter the track from base
    if can_enter(roll, player.pos):
        player.pos = 0
        return

    # Move forward if already on track and not overshooting
    if move_possible(player.pos, roll):
        player.pos += roll
        if player.pos == TRACK_LEN:
            player.finished = True

def everyone_finished(players: List[Player]) -> bool:
    return all(p.finished for p in players)

def print_board(players: List[Player], turn_owner: Player, roll: int | None):
    print("\n" + "=" * 50)
    print("Simple Ludo (Console) — One Token Each")
    print("-" * 50)
    for p in players:
        marker = "🟢" if p is turn_owner else "  "
        pos_label = "BASE" if p.pos < 0 else (f"{p.pos:02d}" if not p.finished else "HOME")
        print(f"{marker} {p.name:<10} [{p.color:<5}] → {pos_label}")
    if roll is not None:
        print(f"\nLast roll: {roll}")
    print("=" * 50)

def next_index(current: int, n: int) -> int:
    return (current + 1) % n

def setup_players() -> List[Player]:
    # Choose 2–4 players interactively (with defaults)
    default_players = [
        ("Red", "RED", 0),
        ("Blue", "BLUE", 14),
        ("Green", "GREEN", 28),
        ("Yellow", "YELLOW", 42),
    ]

    try:
        raw = input("Number of players [2-4, default 2]: ").strip()
        n = int(raw) if raw else 2
        if n < 2 or n > 4:
            print("Invalid count; using 2 players.")
            n = 2
    except ValueError:
        print("Invalid input; using 2 players.")
        n = 2

    players = [Player(*default_players[i]) for i in range(n)]
    return players

def main():
    print("Welcome to Simple Ludo (Console)!")
    print("Rules: Need 6 to leave base. Roll 6 → extra turn. Reach 57 to win.")
    print("Press ENTER to roll on your turn. Type 'q' to quit.\n")

    players = setup_players()
    turn = 0
    winner_declared = False

    while True:
        current = players[turn]

        if current.finished:
            # Skip finished players
            turn = next_index(turn, len(players))
            continue

        print_board(players, current, roll=None)
        action = input(f"{current.name}'s turn — press ENTER to roll (q to quit): ").strip().lower()
        if action == "q":
            print("Game exited. Bye!")
            break

        roll = roll_dice()
        print_board(players, current, roll=roll)

        # Decide move
        if current.pos < 0:
            if can_enter(roll, current.pos):
                print(f"{current.name} rolled a 6 and enters the track!")
                apply_move(current, roll)
            else:
                print(f"{current.name} is in base and needs a 6 to enter. No move.")
        else:
            if move_possible(current.pos, roll):
                old = current.pos
                apply_move(current, roll)
                if current.finished:
                    print(f"🎉 {current.name} reached HOME! They WIN!")
                    winner_declared = True
                else:
                    print(f"{current.name} moved from {old} → {current.pos}")
            else:
                print(f"Move would overshoot HOME. No move.")

        # Extra turn on 6 if not finished
        if not winner_declared and roll == 6 and not current.finished:
            print(f"{current.name} rolled a 6 — extra turn!")
            continue

        if winner_declared or everyone_finished(players):
            print("\nFinal standings:")
            for p in players:
                status = "WINNER" if p.finished else (f"POS {p.pos}" if p.pos >= 0 else "BASE")
                print(f"- {p.name}: {status}")
            print("Thanks for playing! 🙌")
            break

        # Next player's turn
        turn = next_index(turn, len(players))

if __name__ == "__main__":
    main()
