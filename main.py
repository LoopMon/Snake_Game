import pygame
from random import randint
from pygame.locals import *


def random_pos_grid():
    x = randint(0, WIDTH-10)
    y = randint(0, HEIGHT-10)

    return (x//20*20, y//20*20)


def collision(obj1, obj2):
    return (obj1[0] == obj2[0]) and (obj1[1] == obj2[1])


pygame.init()

SCALE = 20
SPEED = 20
WIDTH = 600
HEIGHT = 600
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

current_direction = DOWN

game_states = {
    'home': 0,
    'play': 1,
    'options': 2,
    'credits': 3,
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

canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

score = 0

clock = pygame.time.Clock()
tick = 10

center_canvas = (WIDTH//2, HEIGHT//2)
snake_pos = [center_canvas, center_canvas, center_canvas, center_canvas]
snake = pygame.Surface((SCALE-1, SCALE-1))
snake.fill('green')

apple_pos = random_pos_grid()
apple = pygame.Surface((SCALE, SCALE))
apple.fill('red')

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
                    game_state = 1
                if event.key == K_RETURN and game_menu[current_menu][0] == 'exit':
                    done = True

                if event.key in [K_UP, K_w]:
                    if current_menu == 0:
                        current_menu = max_menu_itens-1
                        game_menu[current_menu][2] = True
                        game_menu[0][2] = False
                    else:
                        current_menu -= 1
                        game_menu[current_menu+1][2] = False
                        game_menu[current_menu][2] = True

                if event.key in [K_DOWN, K_s]:
                    current_menu += 1
                    if current_menu < max_menu_itens:
                        game_menu[current_menu-1][2] = False
                        game_menu[current_menu][2] = True
                    else: 
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
                    if event.key in [K_UP, K_w] and current_direction != DOWN:
                        current_direction = UP
                    if event.key in [K_DOWN, K_s] and current_direction != UP:
                        current_direction = DOWN
                    if event.key in [K_LEFT, K_a] and current_direction != RIGHT:
                        current_direction = LEFT
                    if event.key in [K_RIGHT, K_d] and current_direction != LEFT:
                        current_direction = RIGHT
                    
                if event.key == K_ESCAPE and game_paused:
                    game_state = 0
                    game_paused = False
                    SPEED = 20

    if game_states['home'] == game_state:
        for txt, pos, actived in game_menu:
            if actived:
                font = pygame.font.Font('fonts/Roboto-Regular.ttf', 36)
                font_menu = font.render(f'<< {txt.upper()} >>', True, ('yellow'))
                font_rect = font_menu.get_rect()
                font_rect.center = pos
                canvas.blit(font_menu, font_rect)
            else:
                font = pygame.font.Font('fonts/Roboto-Regular.ttf', 36)
                font_menu = font.render(f'{txt.upper()}', True, ('white'))
                font_rect = font_menu.get_rect()
                font_rect.center = pos
                canvas.blit(font_menu, font_rect)

    if game_states['play'] == game_state:
        # Moviment logic
        if not game_paused:
            if current_direction == UP:
                snake_pos[0] = (snake_pos[0][0], snake_pos[0][1]-SPEED)
            if current_direction == DOWN:
                snake_pos[0] = (snake_pos[0][0], snake_pos[0][1]+SPEED)
            if current_direction == LEFT:
                snake_pos[0] = (snake_pos[0][0]-SPEED, snake_pos[0][1])
            if current_direction == RIGHT:
                snake_pos[0] = (snake_pos[0][0]+SPEED, snake_pos[0][1])

            # Collision logic
            if snake_pos[0][0] < 0:
                snake_pos[0] = (WIDTH-SCALE, snake_pos[0][1])
            if snake_pos[0][0] > WIDTH-SCALE:
                snake_pos[0] = (0, snake_pos[0][1])
            if snake_pos[0][1] < 0:
                snake_pos[0] = (snake_pos[0][0], HEIGHT-SCALE)
            if snake_pos[0][1] > HEIGHT-SCALE:
                snake_pos[0] = (snake_pos[0][0], 0)

            if collision(snake_pos[0], apple_pos):
                snake_pos.append((0, 0))
                score += 1
                apple_pos = random_pos_grid()

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
        font_pause = font.render('Game Paused', True, ('white'))
        font_rect = font_pause.get_rect()
        font_rect.center = center_canvas
        canvas.blit(font_pause, font_rect)

        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 24)
        font_back = font.render('[Esc] Back', True, ('white'))
        canvas.blit(font_back, (20, HEIGHT-40))

    pygame.display.update()

pygame.quit()