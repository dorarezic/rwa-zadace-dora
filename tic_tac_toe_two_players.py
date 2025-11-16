"""Console tic-tac-toe for two human players."""

from typing import List, Optional

Board = List[List[str]]

EMPTY = " "
SYMBOLS = ("X", "O")


def new_board() -> Board:
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def render(board: Board) -> None:
    for idx, row in enumerate(board):
        print(" | ".join(row))
        if idx < 2:
            print("-" * 9)


def winner(board: Board) -> Optional[str]:
    lines = []
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line[0] != EMPTY and line.count(line[0]) == 3:
            return line[0]
    if all(cell != EMPTY for row in board for cell in row):
        return "DRAW"
    return None


def player_move(board: Board, name: str) -> None:
    symbol = SYMBOLS[0] if name == players[0]["name"] else SYMBOLS[1]
    while True:
        try:
            row, col = map(int, input(f"{name} ({symbol}) — odaberi red i stupac (1-3 npr. 1 3): ").split())
            row -= 1
            col -= 1
            if row not in range(3) or col not in range(3):
                print("Vrijednosti moraju biti između 1 i 3.")
                continue
            if board[row][col] != EMPTY:
                print("To polje je već zauzeto.")
                continue
            board[row][col] = symbol
            break
        except ValueError:
            print("Neispravan unos, pokušaj ponovno.")


players = [
    {"name": "", "symbol": SYMBOLS[0]},
    {"name": "", "symbol": SYMBOLS[1]},
]


def main() -> None:
    board = new_board()
    players[0]["name"] = input("Unesi ime igrača 1 (X): ").strip() or "Igrač 1"
    players[1]["name"] = input("Unesi ime igrača 2 (O): ").strip() or "Igrač 2"

    current = 0
    print("\nPočetno stanje table:")
    render(board)

    while True:
        player_move(board, players[current]["name"])
        render(board)

        result = winner(board)
        if result:
            if result == "DRAW":
                print("Neriješeno je!")
            else:
                winner_name = next(p["name"] for p in players if p["symbol"] == result)
                print(f"Čestitke, {winner_name} pobjeđuje!")
            break

        current = 1 - current


if __name__ == "__main__":
    main()
