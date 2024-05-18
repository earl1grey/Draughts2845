#Элементы поля игры.
import pygame
from .variables import LIGHT_BLACK, GREY, SQUARE, CORONA, WHITE
class Elements: #Параметры элементов.
    VOID = 10 #Отступ от каждого края квадрата поля.
    OUTLINE = 2 #Обводка элемента.
    
    def __init__(self, row, col, color, turn):
        self.row = row
        self.col = col
        self.color = color
        self.drawing_color = color
        if turn == WHITE:
            if self.drawing_color == WHITE:
                self.drawing_color = LIGHT_BLACK
            else:
                self.drawing_color = WHITE
        self.dama = False
        self.x = 0
        self.y = 0
        self.calculate_position() #Необходим, если параметры значений будут меняться.
    
    def calculate_position(self): #Расчёт позиций элементов на игровом поле. Необходим, если параметры значений будут меняться.
        self.x = SQUARE * self.col + SQUARE // 2
        self.y = SQUARE * self.row + SQUARE // 2
    
    def damas(self): #Элемент дамки.
        self.dama = True
    
    def drawing_elem(self, window): #Отображение элементов на игровом поле.
        radius = SQUARE // 2 - self.VOID #Радиус элемента.
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE) #Отображение обводки элемента.
        pygame.draw.circle(window, self.drawing_color, (self.x, self.y), radius) #Отображение самого элемента.
        if self.dama:
            window.blit(CORONA, (self.x - CORONA.get_width()//2, self.y - CORONA.get_height()//2)) #Вывод короны.
    
    def move(self, row, col): #Движение элемента.
        self.row = row
        self.col = col
        self.calculate_position()

    def __repr__(self): #Функция для избежание системной печати на объект и создания собственной печати.
        if self.color == LIGHT_BLACK:
            return f'BLACK<{self.row} {self.col}>'
        return f'WHITE<{self.row} {self.col}>'

