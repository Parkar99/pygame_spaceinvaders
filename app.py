import random

from pygame import *


# Direction Enum
class Direction:
    LEFT, RIGHT = range(2)


# Initialize PyGame
init()

# Set the screen var
screen_x = 800
screen_y = 600
screen = display.set_mode((screen_x, screen_y))
screen_img = image.load('images/background.jpg')
screen_img = transform.scale(
    screen_img,
    (int(screen_y * screen_img.get_width() / screen_img.get_height()), screen_y),
)

# Window title and icon
display.set_caption('Spaceinvaders')
display.set_icon(image.load('images/ufo.png'))

# Game run status
DONE = False


# Player
player_img = image.load('images/player.png')
player_x = 370
player_y = 480
player_speed = 0.3
player_x_move_by = 0

# Enemy
enemy_img = image.load('images/enemy.png')
enemy_x = random.randint(0, screen_x - 64)
enemy_y = random.randint(0, 150)
enemy_x_speed = 0.3
enemy_y_speed = 10
enemy_move_direction = Direction.LEFT
enemy_x_move_by = 0
enemy_y_move_by = 0


def move_player(x, y, speed) -> tuple:
    ''' Returns updated x and y values corresponding to the speed '''
    keys = key.get_pressed()

    if x < screen_x - 64 and keys[ord('d')] or keys[ord('D')]:
        x += speed

    if x > 0 and keys[ord('a')] or keys[ord('A')]:
        x -= speed

    return x, y


def move_enemy(x, y, speed, direction: Direction) -> tuple:
    ''' Move enemy in specific direction '''

    if direction == Direction.RIGHT:
        if x < screen_x - 64:
            x += speed
        else:
            direction = Direction.LEFT
            y += 10
    elif direction == Direction.LEFT:
        if x > 0:
            x -= speed
        else:
            direction = Direction.RIGHT
            y += 10

    return x, y, direction


def draw_player(x, y) -> None:
    ''' Draws player '''
    screen.blit(player_img, (x, y))


def draw_enemy(x, y) -> None:
    ''' Draws enemy '''
    screen.blit(enemy_img, (x, y))


def is_close_event() -> bool:
    ''' Returns whether close event was triggered '''
    for e in event.get():
        if e.type == QUIT:
            return True
    return False


# Game Loop
while not DONE:
    # Close game if close event
    DONE = is_close_event()

    screen.fill((0, 0, 0))
    screen.blit(screen_img, (-int((screen_img.get_width() - screen_x) / 2), 0))

    # Player movement and drawing
    player_x, player_y = move_player(player_x, player_y, player_speed)
    draw_player(player_x, player_y)

    # Enemy drawing
    enemy_x, enemy_y, enemy_move_direction = move_enemy(
        enemy_x, enemy_y, enemy_x_speed, enemy_move_direction
    )
    draw_enemy(enemy_x, enemy_y)

    display.update()
