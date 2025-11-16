from __future__ import annotations

from typing import List, Optional, Tuple

BOARD_SIZE = 3
AI = "X"
HUMAN = "O"
EMPTY = " "

Board = List[List[str]]


def create_board() -> Board:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def render_board(board: Board) -> None:
    separator = "\n" + "-+-+-" * (BOARD_SIZE - 1) + "-\n"
    rows = [" | ".join(board[r]) for r in range(BOARD_SIZE)]
    print(separator.join(rows))


def is_full(board: Board) -> bool:
    return all(cell != EMPTY for row in board for cell in row)


def check_winner(board: Board) -> Optional[str]:
    lines = []
    lines.extend(board)  # rows
    lines.extend([[board[r][c] for r in range(BOARD_SIZE)] for c in range(BOARD_SIZE)])  # columns
    lines.append([board[i][i] for i in range(BOARD_SIZE)])  # main diagonal
    lines.append([board[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)])  # anti-diagonal

    for line in lines:
        if line[0] != EMPTY and all(cell == line[0] for cell in line):
            return line[0]
    return None


def evaluate(board: Board) -> int:
    winner = check_winner(board)
    if winner == AI:
        return 10
    if winner == HUMAN:
        return -10
    return 0


def minimax(board: Board, depth: int, is_maximizing: bool) -> int:
    score = evaluate(board)
    if score == 10:
        return score - depth  # prefer faster wins
    if score == -10:
        return score + depth  # prefer slower losses (or faster human wins)
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    best_score = max(best_score, minimax(board, depth + 1, False))
                    board[r][c] = EMPTY
        return best_score

    best_score = float("inf")
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                board[r][c] = HUMAN
                best_score = min(best_score, minimax(board, depth + 1, True))
                board[r][c] = EMPTY
    return best_score


def find_best_move(board: Board) -> Optional[Tuple[int, int]]:
    best_score = -float("inf")
    best_move: Optional[Tuple[int, int]] = None

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(board, 0, False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move


def prompt_human_move(board: Board) -> Tuple[int, int]:
    while True:
        try:
            raw = input("Unesite svoj potez (red i stupac u rasponu 1-3, npr. '1 3'): ").strip()
            row_str, col_str = raw.split()
            row = int(row_str) - 1
            col = int(col_str) - 1
            if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                raise ValueError
            if board[row][col] != EMPTY:
                print("Polje je zauzeto. Izaberite drugo polje.")
                continue
            return row, col
        except ValueError:
            print("Neispravan unos. Pokušajte ponovno.")


def announce_result(board: Board) -> None:
    winner = check_winner(board)
    if winner == AI:
        print("\nRačunalo pobjeđuje zahvaljujući Minimax algoritmu!")
    elif winner == HUMAN:
        print("\nČestitamo! Pobijedili ste računalo.")
    else:
        print("\nNeriješeno!")


def main() -> None:
    board = create_board()
    print("Igra XO (Tic-Tac-Toe) s Minimax algoritmom.")
    print("Vi igrate s 'O', računalo (optimalni igrač) s 'X'.")
    human_starts = input("Želite li započeti prvi? (da/ne) ").strip().lower().startswith("d")

    current_player = HUMAN if human_starts else AI

    while True:
        render_board(board)
        if current_player == HUMAN:
            row, col = prompt_human_move(board)
            board[row][col] = HUMAN
        else:
            move = find_best_move(board)
            if move is None:
                break
            r, c = move
            board[r][c] = AI
            print(f"\nRačunalo igra na polje ({r + 1}, {c + 1}).")

        winner = check_winner(board)
        if winner or is_full(board):
            render_board(board)
            announce_result(board)
            break

        current_player = HUMAN if current_player == AI else AI


if __name__ == "__main__":
    main()
