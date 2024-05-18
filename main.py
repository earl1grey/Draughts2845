#Является главным файлом, отвечающим за запуск игры.
#Именно тут расположены все переменные и настройки корректного запуска игры.
import pygame, sys
from resources.variables import WIDTH, HEIGHT, SQUARE
from resources.game import Game
from pygame.locals import *
from resources.variables import WHITE, LIGHT_BLACK

pygame.init()

FPS = 60 #Кадров в секунду.

mainClock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) #Отображение игры.
pygame.display.set_caption('Шашки') #Название игры.

font = pygame.font.SysFont(None, 100)
font_small = pygame.font.SysFont(None, 50)

turn = LIGHT_BLACK

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    global click
    while True:

        WINDOW.fill((255, 255, 255))
        draw_text('Шашки', font, (0, 0, 0), WINDOW, 282, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(260, 200, 300, 100)
        button_2 = pygame.Rect(260, 350, 300, 100)
        button_3 = pygame.Rect(260, 500, 300, 100)

        if button_1.collidepoint((mx, my)):
            if click:
                main()

        if button_2.collidepoint((mx, my)):
            if click:
                WINDOW.fill((255, 255, 255))
                options()

        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()

        pygame.draw.rect(WINDOW, (255, 0, 0), button_1)
        pygame.draw.rect(WINDOW, (255, 0, 0), button_2)
        pygame.draw.rect(WINDOW, (255, 0, 0), button_3)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def get_pos_mouse(position): #Считывание позиции мыши.
    x, y = position
    row = y // SQUARE
    col = x // SQUARE
    return row, col

def main(): #Запуск игры. Функция цикла событий. Отвечает за прорисовку и обновление действий в программе.
    run = True
    speed = pygame.time.Clock() #Отвечает за стабильную скорость игры.
    game = Game(WINDOW, turn)
    
    while run:
        speed.tick(FPS) #Отвечает за количество кадров в секунду.
        
        if game.pobeda() != None: #Отвечает за окончание игры (победу в игре).
            print(game.pobeda())
            run = False

        for event in pygame.event.get(): #Набор событий.
            if event.type == pygame.QUIT: #Отвечает за выход из программы.
                run = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN: #Отвечает за действия при нажатии кнопки мыши.
                position = pygame.mouse.get_pos()
                row, col = get_pos_mouse(position)
                game.select(row, col)

        game.updating_game()
    
    pygame.quit()

def options():
    global click
    running = True
    while running:
        draw_text('Настройки', font, (0, 0, 0), WINDOW, 230, 100)
        
        draw_text('Кто ходит первым:', font_small, (0, 0, 0), WINDOW, 250, 200)
        
        mx, my = pygame.mouse.get_pos()

        button_4 = pygame.Rect(260, 250, 100, 100)
        pygame.draw.rect(WINDOW, (255, 0, 0), button_4)
        
        button_5 = pygame.Rect(460, 250, 100, 100)
        pygame.draw.rect(WINDOW, (255, 0, 0), button_5)

        if button_4.collidepoint((mx, my)):
            global turn
            if click:
                turn = WHITE
        
        if button_5.collidepoint((mx, my)):
            if click:
                turn = LIGHT_BLACK

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

main_menu()



