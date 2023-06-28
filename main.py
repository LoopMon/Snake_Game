import pygame
from pygame.locals import *
from game.draw import *
from game.update import *


pygame.init()

SCALE = 20
SPEED = 20
WIDTH = 600
HEIGHT = 600

current_direction = 1 # DOWN

game_states = {
    'home': 0,
    'play': 1,
    'options': 2,
    'credits': 3,
    'gameover': 4
}
game_state = 0
game_paused = False

game_menu = [
    ['play', (WIDTH//2, HEIGHT//3), True],
    ['options', (WIDTH//2, HEIGHT//3+50), False],
    ['credits', (WIDTH//2, HEIGHT//3+100), False],
    ['exit', (WIDTH//2, HEIGHT//3+150), False]
]
current_menu = 0
max_menu_itens = len(game_menu)

area1 = pygame.Rect(0, 80, WIDTH//2, HEIGHT//4)
area2 = pygame.Rect(area1.w, 80, WIDTH//2, HEIGHT//4)
area3 = pygame.Rect(0, area1.y+area1.h, WIDTH//2, HEIGHT//4)
area4 = pygame.Rect(0, area3.y+area3.h, WIDTH//2, HEIGHT//4)

snake_colors = [
    [pygame.Rect(area1.x+10, area1.y+50, 40, 30), ('green'), True],
    [pygame.Rect(area1.x+60, area1.y+50, 40, 30), ('blue'), False],
    [pygame.Rect(area1.x+110, area1.y+50, 40, 30), ('yellow'), False],
    [pygame.Rect(area1.x+10, area1.y+90, 40, 30), ('red'), False],
    [pygame.Rect(area1.x+60, area1.y+90, 40, 30), ('purple'), False],
    [pygame.Rect(area1.x+110, area1.y+90, 40, 30), ('white'), False],
]
current_snake_color = 0

apple_colors = [
    [pygame.Rect(area2.x+10, area2.y+50, 40, 30), ('green'), False],
    [pygame.Rect(area2.x+60, area2.y+50, 40, 30), ('blue'), False],
    [pygame.Rect(area2.x+110, area2.y+50, 40, 30), ('yellow'), False],
    [pygame.Rect(area2.x+10, area2.y+90, 40, 30), ('red'), True],
    [pygame.Rect(area2.x+60, area2.y+90, 40, 30), ('purple'), False],
    [pygame.Rect(area2.x+110, area2.y+90, 40, 30), ('white'), False],
]
current_apple_color = 3

volume_bar = pygame.Rect(30, area3.y+80, 100, 5)
volume_switch = pygame.Rect(volume_bar.x+volume_bar.w, volume_bar.y-13, 5, 30)
volume_audio = 100

pygame.mixer.music.load('audio/menu_som.mp3')
pygame.mixer.music.set_volume(volume_audio/100)

buttons_mode = [
    [pygame.Rect(10, area4.y+70, 150, 50), 'Pacific', 0],
    [pygame.Rect(area4.x+area4.w+10, area4.y+70, 150, 50), 'Normal', 1]
]
current_mode = 1

canvas = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load('img/apple_icon.png')
img_home = pygame.image.load('img/snake_new.png')
img_home = pygame.transform.smoothscale(img_home, (170, 140))
pygame.display.set_caption('Snake Game')
pygame.display.set_icon(icon)

score = 0
posX, posY = 0, 0
left_click = False
collid = False

clock = pygame.time.Clock()
tick = 10

center_canvas = (WIDTH//2, HEIGHT//2)
snake_pos = [center_canvas, center_canvas, center_canvas, center_canvas]
snake = pygame.Surface((SCALE-1, SCALE-1))
snake.fill(snake_colors[current_snake_color][1])

apple_pos = random_pos_grid(canvas)
apple = pygame.Surface((SCALE-1, SCALE-1))
apple.fill(apple_colors[current_apple_color][1])

done = False
while not done:
    canvas.fill('black')
    clock.tick(tick)
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if game_states['home'] == game_state:
                if event.key == K_RETURN and game_menu[current_menu][0] == 'play':
                    pygame.mixer.music.load('audio/comer.mp3')
                    tick = 10
                    game_state = 1

                if event.key == K_RETURN and game_menu[current_menu][0] == 'options':
                    tick = 60
                    game_state = 2
                
                if event.key == K_RETURN and game_menu[current_menu][0] == 'credits':
                    print('credits')

                if event.key == K_RETURN and game_menu[current_menu][0] == 'exit':
                    done = True

                if event.key in [K_UP, K_w]:
                    if current_menu == 0:
                        pygame.mixer.music.play()
                        current_menu = max_menu_itens-1
                        game_menu[current_menu][2] = True
                        game_menu[0][2] = False
                    else:
                        pygame.mixer.music.play()
                        current_menu -= 1
                        game_menu[current_menu+1][2] = False
                        game_menu[current_menu][2] = True

                if event.key in [K_DOWN, K_s]:
                    current_menu += 1
                    if current_menu < max_menu_itens:
                        pygame.mixer.music.play()
                        game_menu[current_menu-1][2] = False
                        game_menu[current_menu][2] = True
                    else: 
                        pygame.mixer.music.play()
                        game_menu[current_menu-1][2] = False
                        current_menu = 0
                        game_menu[current_menu][2] = True

            if game_states['play'] == game_state:
                if event.key == K_p:
                    if not game_paused:            
                        game_paused = True
                        SPEED = 0
                    else:
                        game_paused = False
                        SPEED = 20

                if not game_paused:
                    current_direction = getDirection(event.key, current_direction)
                    
                if event.key == K_ESCAPE and game_paused:
                    pygame.mixer.music.load('audio/menu_som.mp3')
                    game_state = 0
                    game_paused = False
                    SPEED = 20

            if game_states['options'] == game_state:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.load('audio/menu_som.mp3')
                    game_state = 0
            
            if game_states['gameover'] == game_state:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.load('audio/menu_som.mp3')
                    game_state = 0
                    snake_pos = [center_canvas, center_canvas, center_canvas, center_canvas]
                    apple_pos = random_pos_grid(canvas)
                    score = 0
                    SPEED = 20
                    current_direction = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click = True

        if event.type == pygame.MOUSEBUTTONUP:
            left_click = False
            collid = False

        if event.type == pygame.MOUSEMOTION:
            posX, posY = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN and left_click:
            for c, item in enumerate(snake_colors):
                if item[0].collidepoint(posX, posY):
                    pygame.mixer.music.load('audio/button.mp3')
                    pygame.mixer.music.play()
                    current_snake_color = c
                else:
                    pygame.mixer.music.load('audio/button.mp3')
                    pygame.mixer.music.play()
                    item[2] = False

            for c, item in enumerate(apple_colors):
                if item[0].collidepoint(posX, posY):
                    pygame.mixer.music.load('audio/button.mp3')
                    pygame.mixer.music.play()
                    current_apple_color = c
                else:
                    pygame.mixer.music.load('audio/button.mp3')
                    pygame.mixer.music.play()
                    item[2] = False

            for button in buttons_mode:
                if button[0].collidepoint(posX, posY):
                    pygame.mixer.music.load('audio/button.mp3')
                    pygame.mixer.music.play()
                    current_mode = button[2]
        
        if volume_switch.collidepoint(posX, posY):
            collid = True

        if collid and left_click:
            volume_switch.x = posX - 3
    
            if volume_switch.x > volume_bar.x + volume_bar.w:
                volume_switch.x = volume_bar.x + volume_bar.w - 3

            if volume_switch.x < volume_bar.x:
                volume_switch.x = volume_bar.x

            volume_audio = volume_switch.x - volume_bar.x + 3

    if game_states['home'] == game_state:
        canvas.blit(img_home, (WIDTH//2-90, 20))

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 36)
        for item in game_menu:
            font_menu, font_rect = drawItem(font, item)
            canvas.blit(font_menu, font_rect)

    if game_states['play'] == game_state:
        if not game_paused:
            # Moviment logic
            moveSnake(snake_pos, current_direction, SPEED)

            if current_mode == 0:
                # Collision logic
                collisionWithCanvas(canvas, snake_pos, SCALE)

            if collision(snake_pos[0], apple_pos):
                pygame.mixer.music.play()
                snake_pos.append((0, 0))
                score += 1
                apple_pos = random_pos_grid(canvas)

            if current_mode == 1:
                for pos in range(2, len(snake_pos)):
                    if pygame.Rect(
                        snake_pos[0][0], snake_pos[0][1], 19, 19
                    ).colliderect(pygame.Rect(
                        snake_pos[pos][0], snake_pos[pos][1], 19, 19
                    )) and len(snake_pos) > 4:
                        pygame.mixer.music.load('audio/game-over.mp3')
                        pygame.mixer.music.play()
                        game_state = 4
                        SPEED = 0

                if snake_pos[0][0] < 0 or snake_pos[0][0]+19 > WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1]+19 > HEIGHT:
                    pygame.mixer.music.load('audio/game-over.mp3')
                    pygame.mixer.music.play()
                    game_state = 4
                    SPEED = 0

            if game_states['gameover'] != game_state:
                # Snake body logic  
                for i in range(len(snake_pos)-1, 0, -1):
                    snake_pos[i] = (snake_pos[i-1][0], snake_pos[i-1][1])

        for pos in snake_pos:
            canvas.blit(snake, pos)

        # Render Text - Score
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_score = font.render(f'Score: {score}', True, ('gray'))
        canvas.blit(font_score, (10, 10))
        canvas.blit(apple, apple_pos)

    if game_paused:
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 48)
        font_pause, font_rect = drawText(font, 'Game Paused', center_canvas, True)
        canvas.blit(font_pause, font_rect)

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_back, font_rect = drawText(font, '[Esc] Back', (20, HEIGHT-40))
        canvas.blit(font_back, font_rect)

    if game_states['options'] == game_state:
        # TITULO DA AREA - OPTIONS
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 40)
        font_options = font.render('Options', True, ('white'))
        font_rect = font_options.get_rect()
        font_rect.center = (WIDTH//2, 30)
        canvas.blit(font_options, font_rect)

        # Area para as cores da snake
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 32)
        font_snake_colors = font.render('Snake Colors:', True, ('white'))
        font_rect = font_snake_colors.get_rect()
        font_rect.topleft = (area1.x+10, area1.y+10)
        canvas.blit(font_snake_colors, font_rect)

        snake_colors[current_snake_color][2] = True

        for rect, color, active in snake_colors:
            if active:
                pygame.draw.rect(canvas, color, rect)
                pygame.draw.rect(canvas, ('white'), rect, 4)
            else: 
                pygame.draw.rect(canvas, color, rect)

        # Area para as cores da maçã
        apple_colors[current_apple_color][2] = True

        font_apple_colors = font.render('Apple Colors:', True, ('white'))
        font_rect = font_apple_colors.get_rect()
        font_rect.topleft = (area2.x+10, area2.y+10)
        canvas.blit(font_apple_colors, font_rect)

        for rect, color, active in apple_colors:
            if active:
                pygame.draw.rect(canvas, color, rect)
                pygame.draw.rect(canvas, ('white'), rect, 4)
            else: 
                pygame.draw.rect(canvas, color, rect)

        # Area para o volume do jogo
        font_game_volume = font.render('Game Volume:', True, ('white'))
        font_rect = font_game_volume.get_rect()
        font_rect.topleft = (area3.x+10, area3.y+10)
        canvas.blit(font_game_volume, font_rect)

        pygame.draw.rect(canvas, ('white'), volume_bar)
        pygame.draw.rect(canvas, ('green'), volume_switch)
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_volume_audio = font.render(f'{volume_audio}', True, ('white'))
        font_rect = font_volume_audio.get_rect()
        font_rect.topleft = (volume_bar.x + volume_bar.w + 15, volume_bar.y-10)
        canvas.blit(font_volume_audio, font_rect)

        # Area para o modo de jogo
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 32)
        font_game_mode = font.render('Game Mode:', True, ('white'))
        font_rect = font_game_mode.get_rect()
        font_rect.topleft = (area4.x+10, area4.y+10)
        canvas.blit(font_game_mode, font_rect)

        for rect, txt, active in buttons_mode:
            if active == current_mode:
                font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
                font_txt = font.render(txt, True, ('green'))
                pygame.draw.rect(canvas, ('green'), rect, 4)
                canvas.blit(font_txt, (rect.x+20, rect.y+10))
            else:
                font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
                font_txt = font.render(txt, True, ('white'))
                pygame.draw.rect(canvas, ('white'), rect, 4)
                canvas.blit(font_txt, (rect.x+20, rect.y+10))

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_back = font.render('[Esc] Back', True, ('white'))
        font_rect = font_back.get_rect()
        font_rect.bottomleft = (20, HEIGHT-20)
        canvas.blit(font_back, font_rect)

        snake.fill(snake_colors[current_snake_color][1])
        apple.fill(apple_colors[current_apple_color][1])
        pygame.mixer.music.set_volume(volume_audio/100)

    if game_states['gameover'] == game_state:

        for pos in snake_pos:
            canvas.blit(snake, pos)

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_score = font.render(f'Score: {score}', True, ('gray'))
        canvas.blit(font_score, (10, 10))
        canvas.blit(apple, apple_pos)

        pygame.draw.rect(canvas, ('red'), (snake_pos[0][0], snake_pos[0][1], 19, 19))

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 48)
        font_game_over, font_rect = drawText(font, 'Game Over', center_canvas, True)
        canvas.blit(font_game_over, font_rect)

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_back, font_rect = drawText(font, '[Esc] Back', (20, HEIGHT-40))
        canvas.blit(font_back, font_rect)

    pygame.display.update()

pygame.quit()