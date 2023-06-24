import pygame
from pygame.locals import *
from game.draw import *
from game.update import *


pygame.init()

SCALE = 20
SPEED = 20
WIDTH = 600
HEIGHT = 600

current_direction = 1

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
icon = pygame.image.load('img/apple_icon.png')
img_home = pygame.image.load('img/snake_new.png')
img_home = pygame.transform.smoothscale(img_home, (170, 140))
pygame.display.set_caption('Snake Game')
pygame.display.set_icon(icon)

score = 0

clock = pygame.time.Clock()
tick = 10

center_canvas = (WIDTH//2, HEIGHT//2)
snake_pos = [center_canvas, center_canvas, center_canvas, center_canvas]
snake = pygame.Surface((SCALE-1, SCALE-1))
snake.fill('green')

apple_pos = random_pos_grid(canvas)
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
                    current_direction = getDirection(event.key, current_direction)
                    
                if event.key == K_ESCAPE and game_paused:
                    game_state = 0
                    game_paused = False
                    SPEED = 20

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

            # Collision logic
            collisionWithCanvas(canvas, snake_pos, SCALE)

            if collision(snake_pos[0], apple_pos):
                snake_pos.append((0, 0))
                score += 1
                apple_pos = random_pos_grid(canvas)

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

    pygame.display.update()

pygame.quit()