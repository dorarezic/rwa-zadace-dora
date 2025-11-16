"""Console tic-tac-toe with a minimax-driven computer opponent."""

from math import inf
from typing import List, Optional, Tuple

Board = List[List[str]]

EMPTY = " "
PLAYER = "X"
AI = "O"


def new_board() -> Board:
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def render(board: Board) -> None:
    for idx, row in enumerate(board):
        print(" | ".join(row))
        if idx < 2:
            print("-" * 9)


def winner(board: Board) -> Optional[str]:
    lines = []
    lines.extend(board)  # rows
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # columns
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line[0] != EMPTY and line.count(line[0]) == 3:
            return line[0]
    if all(cell != EMPTY for row in board for cell in row):
        return "DRAW"
    return None


def minimax(board: Board, maximizing: bool) -> int:
    state = winner(board)
    if state == PLAYER:
        return 1
    if state == AI:
        return -1
    if state == "DRAW":
        return 0

    if maximizing:
        best = -inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER
                    best = max(best, minimax(board, False))
                    board[r][c] = EMPTY
        return best

    best = inf
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                best = min(best, minimax(board, True))
                board[r][c] = EMPTY
    return best


def ai_move(board: Board) -> Tuple[int, int]:
    best_score = inf
    best = (-1, -1)
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(board, True)
                board[r][c] = EMPTY
                if score < best_score:
                    best_score = score
                    best = (r, c)
    return best


def player_move(board: Board) -> Tuple[int, int]:
    while True:
        try:
            row, col = map(int, input("Enter row and column (1-3, e.g. 2 3): ").split())
            row -= 1
            col -= 1
            if row not in range(3) or col not in range(3):
                print("Values must be between 1 and 3.")
                continue
            if board[row][col] != EMPTY:
                print("That square is already taken.")
                continue
            return row, col
        except ValueError:
            print("Invalid input, try again.")


def main() -> None:
    board = new_board()
    current = PLAYER
    print("Tic-Tac-Toe: you play as X, computer plays as O.")
    render(board)

    while True:
        if current == PLAYER:
            r, c = player_move(board)
            board[r][c] = PLAYER
        else:
            print("Computer is thinking...")
            r, c = ai_move(board)
            board[r][c] = AI

        render(board)
        result = winner(board)
        if result:
            if result == PLAYER:
                print("Congratulations, you win!")
            elif result == AI:
                print("Computer wins.")
            else:
                print("It's a draw.")
            break

        current = AI if current == PLAYER else PLAYER


if __name__ == "__main__":
    main()
