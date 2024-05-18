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

bg = pygame.image.load('assets/background_menu.png')
black = pygame.image.load('assets/black.png')
white = pygame.image.load('assets/white.png')

pygame.mixer.init()
music = pygame.mixer.music.load('assets/music.ogg')
pygame.mixer.music.play(-1)

turn = LIGHT_BLACK

def draw_text(text, font, color, surface, x, y): #Отрисовка текста
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu(): #Главное меню
    global click
    while True:

        WINDOW.blit(bg, (0, 0))
        draw_text('Шашки', font, (0, 0, 0), WINDOW, 282, 100)

        mx, my = pygame.mouse.get_pos()

        play = pygame.image.load ('assets/play.png')
        option = pygame.image.load ('assets/option.png')
        exit = pygame.image.load ('assets/exit.png')

        button_1 = WINDOW.blit(play, (260, 200))
        button_2 = WINDOW.blit(option, (260, 350))
        button_3 = WINDOW.blit(exit, (260, 500))

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
            restart_panel()
            mainClock.tick(1)
            restart()

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


def options(): #Меню настройки
    global click
    running = True
    while running:
        WINDOW.blit(bg, (0, 0))
        
        draw_text('Настройки', font, (0, 0, 0), WINDOW, 230, 100)
        
        draw_text('Кто ходит первым:', font_small, (0, 0, 0), WINDOW, 250, 200)
        
        mx, my = pygame.mouse.get_pos()

        button_4 = WINDOW.blit(white, (260, 250))
        
        button_5 = WINDOW.blit(black, (460, 250))

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

def restart_panel(): #Экран рестарта
    global mainClock

    WINDOW.fill((20, 20, 20))

    font = pygame.font.SysFont('Arial', 32)
    text = font.render('Нажмите пробел для рестарта', True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (WIDTH//2, HEIGHT//2)

    WINDOW.blit(text, textRect)

    pygame.display.update()

def restart(): #Функция рестарта
    for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    main()
                if event.type == K_ESCAPE:
                    quit()

            if event.type == pygame.QUIT:
                quit()

main_menu()



