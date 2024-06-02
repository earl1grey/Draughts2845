# Данный файл является полем игры.
import pygame
from .variables import BLACK, ROWS, COLS, WHITE, SQUARE, LIGHT_BLACK, \
    BROWN  # Импортирование значений из variables.py общей директории resources.
from .elements import Elements  # Импортирование значений из elements.py общей директории resources.
from dataclasses import dataclass, field
from typing import Generator, Tuple, List


@dataclass
class Move:  # Класс хода элементов.
    row_from: int
    col_from: int
    row_to: int
    col_to: int
    kill: List[Tuple[int, int]] = field(default_factory=list)


@dataclass
class Cross(Move):
    pass


class Board:
    def __init__(self, turn):
        self.turn = turn
        self.board: List[List[Elements]] = []
        self.blacks = self.whites = 12  # Количество шашек.
        self.black_damas = self.white_damas = 0  # Количество дамок.
        self.board_create()  # Создание доски.

    def squares(self, window):  # Прорисовывает квадраты поля.
        window.fill(BLACK)

        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, BROWN, (row * SQUARE, col * SQUARE, SQUARE, SQUARE))

    def move(self, element, row, col):  # Движение элемента.
        self.board[element.row][element.col], self.board[row][col] = self.board[row][col], self.board[element.row][
            element.col]  # Изменение позиции элемента перестановкой изначальных значений.
        element.move(row, col)

        if row == ROWS - 1 or row == 0:
            element.damas()
            if element.color == WHITE:
                self.white_damas += 1
            else:
                self.black_damas += 1

    def get_element(self, row, col):
        return self.board[row][col]

    def board_create(self):  # Параметры создания поля.
        for row in range(ROWS):
            self.board.append([])  # Заполнение.
            for col in range(COLS):
                if col % 2 == ((
                                       row + 1) % 2):  # Подсчёт каждого столбца и строки поля для избежания неправильной подстановки элемента поля.
                    if row < 3:  # Подсчитывает первые 3 строки поля для заполнения.
                        self.board[row].append(Elements(row, col, WHITE, self.turn))  # Заполнение белыми элементами.
                    elif row > 4:  # Подсчитывает остальные строки поля для заполнения.
                        self.board[row].append(
                            Elements(row, col, LIGHT_BLACK, self.turn))  # Заполение чёрными элементами.
                    else:
                        self.board[row].append(
                            0)  # Служит разделителем для элементов поля. Чередуется с существующими значениями. Является пустотой.
                else:
                    self.board[row].append(0)

    def drawing_elem(self, window):  # Отображение поля с элементами.
        self.squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                element = self.board[row][col]
                if element != 0:
                    element.drawing_elem(window)

    def removing(self, elements):  # Удаление элемента.
        for element in elements:
            self.board[element.row][element.col] = 0
            if element != 0:
                if element.color == LIGHT_BLACK:
                    self.blacks -= 1
                else:
                    self.whites -= 1

    def pobeda(self):  # Завершение игры.
        if self.blacks <= 0:
            return WHITE
        elif self.whites <= 0:
            return LIGHT_BLACK

        return None

    def get_val_moves(self, element):
        moves = {
            (move.row_to, move.col_to): move.kill
            for move in self._check_is_move(element.row, element.col, element.color)
        }
        if any(moves.values()):
            moves = {
                coords: kills
                for coords, kills in moves.items()
                if kills
            }
        return moves

    def _check_is_cross(self, row: int, col: int, player_color) -> Generator[Cross, None, None]:
        drow = 1 if player_color == WHITE else -1
        for dcol in (-1, 1):
            r2 = row + 2 * drow
            c2 = col + 2 * dcol
            if r2 < 0 or c2 < 0 or r2 >= ROWS or c2 >= COLS:
                continue
            neightbour = self.board[row + drow][col + dcol]
            over_neightbour = self.board[r2][c2]
            if neightbour != 0 and neightbour.color != player_color and over_neightbour == 0:
                yield Cross(row, col, r2, c2, [neightbour])

    def _check_is_move(self, row: int, col: int, player_color) -> Generator[Move, None, None]:
        if self.board[row][col].dama:
            yield from self._check_is_dama_move(row, col, player_color)
        yield from self._check_is_default_move(row, col, player_color)

    def _check_is_default_move(self, row: int, col: int, player_color) -> Generator[Move, None, None]:
        drow = 1 if player_color == WHITE else -1
        for dcol in (-1, 1):
            r2 = row + drow
            c2 = col + dcol
            if r2 < 0 or c2 < 0 or r2 >= ROWS or c2 >= COLS:
                continue
            if self.board[r2][c2] == 0:
                yield Move(row, col, r2, c2)
        for cross in self._check_is_cross(row, col, player_color):
            r2 = cross.row_to
            c2 = cross.col_to
            kill = cross.kill.copy()
            while True:
                try:
                    cross = next(self._check_is_cross(r2, c2, player_color))
                    r2 = cross.row_to
                    c2 = cross.col_to
                    kill += cross.kill
                except:
                    break
            yield Move(row, col, r2, c2, kill)

    def _check_is_dama_move(self, row: int, col: int, player_color) -> Generator[Move, None, None]:
        for dcol in (-1, 1):
            for drow in (-1, 1):
                killed = []
                count_repeated_enemy = 0
                for step in range(1, 8):
                    r2 = row + step * drow
                    c2 = col + step * dcol
                    if r2 < 0 or c2 < 0 or r2 >= ROWS or c2 >= COLS:
                        break
                    if self.board[r2][c2] == 0:
                        yield Move(row, col, r2, c2, killed.copy())
                        count_repeated_enemy = 0
                    elif self.board[r2][c2].color == player_color:
                        break
                    elif self.board[r2][c2].color != player_color:
                        count_repeated_enemy += 1
                        if count_repeated_enemy > 1:
                            break
                        killed.append(self.board[r2][c2])
