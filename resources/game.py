import pygame
from .variables import LIGHT_BLACK, WHITE, BLUE, SQUARE
from resources.board import Board

pygame.mixer.init()
move_sound = pygame.mixer.Sound('assets/move.ogg')
select_sound = pygame.mixer.Sound('assets/select.ogg')      

class Game:
    def __init__(self, window, turn): 
        self._init(turn)
        self.window = window
    
    def updating_game(self): #Обновление игры.
        self.board.drawing_elem(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self, turn):
        self.selected = None
        self.board = Board(turn)
        self.turn = LIGHT_BLACK
        self.valid_moves = {}

    def pobeda(self): #Окончание игры.
        return self.board.pobeda()

    def reset(self):
        self._init()

    def select(self, row, col): #Выбрать направление.
        if self.selected:
            result = self._moving(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        element = self.board.get_element(row, col)
        if element != 0 and element.color == self.turn:
            self.selected = element
            self.valid_moves = self.board.get_val_moves(element)
            select_sound.play()
            return True

        return False

    def _moving(self, row, col): #Система хода эелемента.
        elementce = self.board.get_element(row, col)
        if self.selected and elementce == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            jump = self.valid_moves[(row, col)]
            if jump:
                self.board.removing(jump)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, BLUE, (col * SQUARE + SQUARE//2, row * SQUARE + SQUARE//2), 15)

    def change_turn(self): #Ход игрока/оппонента.
        self.valid_moves = {}
        if self.turn == LIGHT_BLACK:
            self.turn = WHITE
            move_sound.play()
        else:
            self.turn = LIGHT_BLACK
            move_sound.play()

