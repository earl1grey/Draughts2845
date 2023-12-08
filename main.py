#Является главным файлом, отвечающим за запуск игры.
#Именно тут расположены все переменные и настройки корректного запуска игры.
import pygame
from resources.variables import WIDTH, HEIGHT, SQUARE
from resources.game import Game

FPS = 60 #Кадров в секунду.

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) #Отображение игры.
pygame.display.set_caption('Шашки') #Название игры.

def get_pos_mouse(position): #Считывание позиции мыши.
    x, y = position
    row = y // SQUARE
    col = x // SQUARE
    return row, col

def main(): #Запуск игры. Функция цикла событий. Отвечает за прорисовку и обновление действий в программе.
    run = True
    speed = pygame.time.Clock() #Отвечает за стабильную скорость игры.
    game = Game(WINDOW)
    
    while run:
        speed.tick(FPS) #Отвечает за количество кадров в секунду.
        
        if game.pobeda() != None: #Отвечает за окончание игры (победу в игре).
            print(game.pobeda())
            run = False

        for event in pygame.event.get(): #Набор событий.
            if event.type == pygame.QUIT: #Отвечает за выход из программы.
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: #Отвечает за действия при нажатии кнопки мыши.
                position = pygame.mouse.get_pos()
                row, col = get_pos_mouse(position)
                game.select(row, col)

        game.updating_game()
    
    pygame.quit()

main()



