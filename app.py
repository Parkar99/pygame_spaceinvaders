from pygame import *

import random
import math


# Direction Enum
class Direction:
    LEFT, RIGHT = range(2)


# Bullet State Enum
class BulletState:
    READY, FIRED = range(2)


# Enemy class
class Enemy:
    def __init__(self, image, x, y, x_speed, y_speed, move_direction):
        self.image = image
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.move_direction = move_direction


# Initialize PyGame
init()

# Set the screen var
screen_x = 800
screen_y = 600
screen = display.set_mode((screen_x, screen_y))
screen_img = image.load('images/background.jpg')
screen_img = transform.scale(
    screen_img,
    (int(screen_y * screen_img.get_width() / screen_img.get_height()), screen_y + 1),
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
player_speed = 0.6

# Enemy
enemies = []

enemy_img = image.load('images/enemy.png')
# enemy_x = random.randint(0, screen_x - 64)
# enemy_y = random.randint(0, 150)
enemy_x_speed = 0.2
enemy_y_speed = 20
# enemy_move_direction = random.randint(0, 1)
number_of_enemies = 6

for _ in range(number_of_enemies):
    enemies.append(
        Enemy(
            enemy_img,
            random.randint(0, screen_x - 64),
            random.randint(0, 150),
            enemy_x_speed,
            enemy_y_speed,
            random.randint(0, 1),
        )
    )

# Bullet
bullet_img = image.load('images/bullet.png')
bullet_x = player_x
bullet_y = player_y
bullet_speed = 1
bullet_state = BulletState.READY

score = 0

# Font for displaying score
game_font = font.SysFont('monospace', 18)
game_over_font = font.SysFont('monospace', 28)

is_game_over = False


def reset_enemy(index):
    global enemies

    enemies[index].x = random.randint(0, screen_x - 64)
    enemies[index].y = random.randint(0, 150)
    enemies[index].move_direction = random.randint(0, 1)


def distance(x1, x2, y1, y2) -> float:
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def detect_collision(bx, by, ex, ey) -> bool:
    if distance(bx + 16, ex + 32, by, ey + 32) < 25:
        return True

    return False


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
    screen.blit(player_img, (int(x), int(y)))


def draw_enemy(x, y) -> None:
    ''' Draws enemy '''
    screen.blit(enemy_img, (int(x), int(y)))


def is_close_event(events) -> bool:
    ''' Returns whether close event was triggered '''
    for e in events:
        if e.type == QUIT:
            return True
    return False


def reset_bullet():
    global bullet_state
    global bullet_y

    bullet_state = BulletState.READY
    bullet_y = player_y


def check_for_shoot_and_update_bullet(events):
    ''' Checks if player has shot a bullet '''

    global bullet_state
    global bullet_x
    global bullet_y

    for e in events:
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullet_state == BulletState.READY:
                    bullet_state = BulletState.FIRED
                    bullet_x = player_x

    if bullet_state == BulletState.FIRED:
        if bullet_y > 0:
            bullet_y -= bullet_speed
        else:
            reset_bullet()


def game_over():
    global enemies, player_y

    for enemy in enemies:
        if enemy.y > player_y - 60:
            return True

    return False


# Game Loop
while not DONE:
    events = event.get()

    # Close game if close event
    DONE = is_close_event(events)

    screen.fill((0, 0, 0))
    screen.blit(screen_img, (-int((screen_img.get_width() - screen_x) / 2), -1))

    if is_game_over:
        label = game_over_font.render(
            f'Game Over! Final Score: {score}', 1, (255, 255, 255)
        )
        screen.blit(label, (screen_x // 4, screen_y // 4))
        display.update()
        continue

    is_game_over = game_over()

    # Bullet Logic
    check_for_shoot_and_update_bullet(events)
    if bullet_state == BulletState.FIRED:
        screen.blit(bullet_img, (int(bullet_x), int(bullet_y)))

    # Player Logic
    player_x, player_y = move_player(player_x, player_y, player_speed)
    draw_player(player_x, player_y)

    # Enemy Logic
    for index, enemy in enumerate(enemies):
        enemy.x, enemy.y, enemy.move_direction = move_enemy(
            enemy.x, enemy.y, enemy.x_speed, enemy.move_direction
        )
        draw_enemy(enemy.x, enemy.y)

        if detect_collision(bullet_x, bullet_y, enemy.x, enemy.y):
            reset_bullet()
            score += 1
            reset_enemy(index)
            if score % 1 == 0:
                for e in enemies:
                    e.x_speed += 0.1
                    e.y_speed += 0.2

    label = game_font.render(f'Score: {score}', 1, (255, 255, 255))

    screen.blit(label, (10, 10))

    display.update()
