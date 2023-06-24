def random_pos_grid(canvas):
    from random import randint

    w = canvas.get_width()
    h = canvas.get_height()

    x = randint(0, w-10)
    y = randint(0, h-10)

    return (x//20*20, y//20*20)


def collision(obj1, obj2):
    return (obj1[0] == obj2[0]) and (obj1[1] == obj2[1])


def moveSnake(snake_pos, current_direction, speed):
    if current_direction == 0:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1]-speed)
    if current_direction == 1:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1]+speed)
    if current_direction == 2:
        snake_pos[0] = (snake_pos[0][0]-speed, snake_pos[0][1])
    if current_direction == 3:
        snake_pos[0] = (snake_pos[0][0]+speed, snake_pos[0][1])


def collisionWithCanvas(canvas, snake_pos, scale):
    w = canvas.get_width()
    h = canvas.get_height()

    if snake_pos[0][0] < 0:
        snake_pos[0] = (w-scale, snake_pos[0][1])
    if snake_pos[0][0] > w-scale:
        snake_pos[0] = (0, snake_pos[0][1])
    if snake_pos[0][1] < 0:
        snake_pos[0] = (snake_pos[0][0], h-scale)
    if snake_pos[0][1] > h-scale:
        snake_pos[0] = (snake_pos[0][0], 0)


def getDirection(key, current_direction):
    from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d

    if key in [K_UP, K_w] and current_direction != 1:
        return 0
    if key in [K_DOWN, K_s] and current_direction != 0:
        return 1
    if key in [K_LEFT, K_a] and current_direction != 3:
        return 2
    if key in [K_RIGHT, K_d] and current_direction != 2:
        return 3

    return current_direction