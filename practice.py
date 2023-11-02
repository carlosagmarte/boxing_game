import pygame.transform


from util import *
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load(os.path.join('assets', 'retro.mp3'))
pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boxers")

PUNCH_COOLDOWN = 50  # frames, e.g., 30 frames at 60FPS would be half a second
PUNCH_DURATION = PUNCH_COOLDOWN //2  # duration of punch in frames

# coords
RING_PADDING_WC = 500
RING_PADDING_HC = 250

# padding size
RING_PADDING_W = 460
RING_PADDING_H = 240

# x,y offset values
RING_H_OFFSET = -60
RING_W_OFFSET = -60


ring_boundary = pygame.Rect(RING_PADDING_WC + RING_W_OFFSET, RING_PADDING_HC + RING_H_OFFSET, WIDTH - 2*RING_PADDING_W,
                            HEIGHT - 2*RING_PADDING_H)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('NewRoman', 60)
WINNER_FONT = pygame.font.SysFont('NewRoman', 100)
FPS = 60
VEL = 5

blue_is_blocking = False
red_is_blocking = False


HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
BLUE_HEALTH_BAR_POS = (10, 10)
RED_HEALTH_BAR_POS = (WIDTH - HEALTH_BAR_WIDTH - 10, 10)

# PUNCH_VEL = 10
MAX_PUNCHES = 100
BOXER_WIDTH, BOXER_HEIGHT = 55, 40

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


BLUE_BOXER_IMAGE = pygame.image.load(
    os.path.join('Assets', 'blue.png'))
BLUE_BOXER = pygame.transform.scale(BLUE_BOXER_IMAGE, (55, 75))


RED_BOXER_IMAGE = (pygame.image.load(os.path.join('Assets', 'red.png')))
RED_BOXER = pygame.transform.scale(RED_BOXER_IMAGE, (55, 75))
RED_BOXER = pygame.transform.flip(RED_BOXER, True, False)

BLUE_PUNCH_IMAGE = pygame.image.load(os.path.join('Assets', 'blue_punch.png'))
BLUE_PUNCH_IMAGE = pygame.transform.scale(BLUE_PUNCH_IMAGE, (55, 75))
BLUE_PUNCH_IMAGE = pygame.transform.flip(BLUE_PUNCH_IMAGE, True, False)

RED_PUNCH_IMAGE = pygame.image.load(os.path.join('Assets', 'red_punch.png'))
RED_PUNCH_IMAGE = pygame.transform.scale(RED_PUNCH_IMAGE, (55, 75))
RED_PUNCH_IMAGE = pygame.transform.flip(RED_PUNCH_IMAGE, True, False)
HEALTH_IMAGE_WIDTH = 150
HEALTH_IMAGE_HEIGHT = 150
BLUE_HEALTH_IMAGE = pygame.image.load(os.path.join('Assets', 'blue_icon.png'))
RED_HEALTH_IMAGE = pygame.image.load(os.path.join('Assets', 'red_icon.png'))
BLUE_HEALTH_IMAGE = pygame.transform.scale(BLUE_HEALTH_IMAGE, (HEALTH_IMAGE_WIDTH, HEALTH_IMAGE_HEIGHT))
RED_HEALTH_IMAGE = pygame.transform.scale(RED_HEALTH_IMAGE, (HEALTH_IMAGE_WIDTH, HEALTH_IMAGE_HEIGHT))
RED_HEALTH_IMAGE = pygame.transform.flip(RED_HEALTH_IMAGE, True, False)

RING = pygame.transform.scale(pygame.image.load('Assets/boxing_ring_dalle3.png'), (WIDTH, HEIGHT))


def title_screen():

    title_image = pygame.image.load(os.path.join('Assets', 'title_screen.png'))
    title_image = pygame.transform.scale(title_image, (WIDTH, HEIGHT))

    WIN.blit(title_image, (0, 0))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False


def draw_window(red, blue, red_health, blue_health, blue_is_punching, red_is_punching):
    WIN.blit(RING, (0, 0))

    # pygame.draw.rect(WIN, (0, 255, 0), ring_boundary, 2)  # Draws a green boundary

    # Draw Red Health Bar
    pygame.draw.rect(WIN, RED,
                     (WIDTH - HEALTH_BAR_WIDTH - 10, 10, HEALTH_BAR_WIDTH * (red_health / 100), HEALTH_BAR_HEIGHT))

    # Draw Blue Health Bar
    pygame.draw.rect(WIN, BLUE, (10, 10, HEALTH_BAR_WIDTH * (blue_health / 100), HEALTH_BAR_HEIGHT))

    # Draw Border for Red Health Bar
    pygame.draw.rect(WIN, (0, 0, 0), (WIDTH - HEALTH_BAR_WIDTH - 10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)

    # Draw Border for Blue Health Bar
    pygame.draw.rect(WIN, (0, 0, 0), (10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)

    #the code below is for if I want text instead of images for the health bars
    # red_health_text = HEALTH_FONT.render(
    #     "Health: " + str(red_health), 1, RED)
    # blue_health_text = HEALTH_FONT.render(
    #     "Health: " + str(blue_health), 1, BLUE)

    # WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    # WIN.blit(blue_health_text, (10, 10))

    WIN.blit(RED_HEALTH_IMAGE, (WIDTH - RED_HEALTH_IMAGE.get_width() - 10, -100 + RED_HEALTH_IMAGE.get_height() + 5))

    WIN.blit(BLUE_HEALTH_IMAGE, (10, -100 + BLUE_HEALTH_IMAGE.get_height() + 5))

    if blue_is_punching:
        WIN.blit(BLUE_PUNCH_IMAGE, (blue.x, blue.y))
    else:
        WIN.blit(BLUE_BOXER, (blue.x, blue.y))

    if red_is_punching:
        WIN.blit(RED_PUNCH_IMAGE, (red.x, red.y))
    else:
        WIN.blit(RED_BOXER, (red.x, red.y))


def blue_handlemovement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d]:  # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 15:  # DOWN
        blue.y += VEL

        # Clamp the blue boxer's position within the ring_boundary
    blue.clamp_ip(ring_boundary)

def red_handlemovement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
      red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
      red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
      red.y += VEL

      # Clamp the red boxer's position within the ring_boundary
    red.clamp_ip(ring_boundary)


def draw_winner(text, color):
    draw_text = WINNER_FONT.render(text, 1, color)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    title_screen()
    red = pygame.Rect(600, 300, BOXER_WIDTH, BOXER_HEIGHT)
    blue = pygame.Rect(500, 300, BOXER_WIDTH, BOXER_HEIGHT)

    red_health = 100
    blue_health = 100

    blue_is_punching = False
    red_is_punching = False

    blue_punches_thrown = 0
    red_punches_thrown = 0

    blue_punch_cooldown = 10
    red_punch_cooldown = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        red_handlemovement(keys_pressed, red)
        blue_handlemovement(keys_pressed, blue)

        if keys_pressed[pygame.K_f] and blue_punch_cooldown == 0 and blue_punches_thrown < MAX_PUNCHES:
            blue_is_punching = True
            blue_punches_thrown += 1
            blue_punch_cooldown = PUNCH_COOLDOWN


        if blue_punch_cooldown == PUNCH_DURATION//2:
            blue_is_punching = False

        if keys_pressed[pygame.K_RCTRL] and red_punch_cooldown == 0 and red_punches_thrown < MAX_PUNCHES:
            red_is_punching = True
            red_punches_thrown += 1
            red_punch_cooldown = PUNCH_COOLDOWN

        if red_punch_cooldown == PUNCH_DURATION//2:
            red_is_punching = False

        # Check for punches landing
        if blue_is_punching and blue.colliderect(red):
            red_health -= 1
        if red_is_punching and red.colliderect(blue):
            blue_health -= 1
        # Reduce cooldown counters
        if blue_punch_cooldown > 0:
            blue_punch_cooldown -= 1

        if red_punch_cooldown > 0:
            red_punch_cooldown -= 1

        if keys_pressed[pygame.K_e]:
            blue_is_blocking = not blue_is_blocking
        if keys_pressed[pygame.K_RSHIFT]:
            red_is_blocking = not red_is_blocking


        if blue_is_punching and blue.colliderect(red):
            if red_is_blocking:
                pass  # Or maybe do a reduced amount of damage
            else:
                red_health -= 1

        if red_is_punching and red.colliderect(blue):
            if blue_is_blocking:
                pass  # Or do reduced damage
            else:
                blue_health -= 1

        if red_health <= 0 and blue_health <= 0:
            draw_winner("It's a Draw!", (0, 0, 0))  # Green for Draw
            break
        elif red_health <= 0:
            draw_winner("Blue Wins!", BLUE)  # Use the predefined BLUE color
            break
        elif blue_health <= 0:
            draw_winner("Red Wins!", RED)  # Use the predefined RED color
            break

        WIN.fill(WHITE)
        draw_window(red, blue, red_health, blue_health, blue_is_punching, red_is_punching)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
   main()