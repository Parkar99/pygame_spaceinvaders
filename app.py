from pygame import *

# Initialize PyGame
init()

# Set the screen var
screen = display.set_mode((800, 600))

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
player_y_move_by = 0


def move_player(x, y, speed) -> tuple:
    ''' Returns updated x and y values corresponding to the speed '''
    keys = key.get_pressed()
    if keys[ord('w')] or keys[ord('W')]:
        y -= speed

    if keys[ord('s')] or keys[ord('S')]:
        y += speed

    if keys[ord('d')] or keys[ord('D')]:
        x += speed

    if keys[ord('a')] or keys[ord('A')]:
        x -= speed

    return x, y


def draw_player(x, y) -> None:
    ''' Draws player '''
    screen.blit(player_img, (x, y))


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

    # Player movement and drawing
    player_x, player_y = move_player(player_x, player_y, player_speed)
    draw_player(player_x, player_y)

    display.update()
