import pygame
import random
import sys
from pygame.locals import *


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 40
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
ADD_NEW_BADDIE_RATE = 9
PLAYER_MOVE_RATE = 5


def terminate():
    pygame.quit()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return


def player_has_hit_baddie(player_rect, baddies):
    for b in baddies:
        if player_rect.colliderect(b['rect']):
            return True
    return False


def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# set up pygame, the window, and the mouse cursor
pygame.init()
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
game_over_sound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
player_image = pygame.image.load('player.png')
player_rect = player_image.get_rect()
romulan_image = pygame.image.load('romulan.png')
klingon_image = pygame.image.load('klingon.png')

# show the "Start" screen
draw_text('Romulan War', font, window_surface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
draw_text('Mouse or Arrows to move', font, window_surface, (WINDOW_WIDTH / 5) - 35, (WINDOW_HEIGHT / 3) + 50)
draw_text('Press Z or X for cheats', font, window_surface, (WINDOW_WIDTH / 5) - 35, (WINDOW_HEIGHT / 3) + 100)
draw_text('Press a key to start.', font, window_surface, (WINDOW_WIDTH / 3) - 30, (WINDOW_HEIGHT / 3) + 150)
pygame.display.update()
wait_for_player_to_press_key()


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    score = 0
    player_rect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
    move_left = move_right = move_up = move_down = False
    reverse_cheat = slow_cheat = False
    baddie_add_counter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # the game loop runs while the game part is playing
        score += 1  # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverse_cheat = True
                if event.key == ord('x'):
                    slow_cheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    move_right = False
                    move_left = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    move_left = False
                    move_right = True
                if event.key == K_UP or event.key == ord('w'):
                    move_down = False
                    move_up = True
                if event.key == K_DOWN or event.key == ord('s'):
                    move_up = False
                    move_down = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverse_cheat = False
                    score = 0
                if event.key == ord('x'):
                    slow_cheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    move_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    move_right = False
                if event.key == K_UP or event.key == ord('w'):
                    move_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    move_down = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                player_rect.move_ip(event.pos[0] - player_rect.centerx, event.pos[1] - player_rect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverse_cheat and not slow_cheat:
            baddie_add_counter += 1
        if baddie_add_counter == ADD_NEW_BADDIE_RATE:
            baddie_add_counter = 0
            baddieSize = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)
            newBaddie1 = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                          'speed': random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED),
                          'surface': pygame.transform.scale(romulan_image, (baddieSize, baddieSize))}
            newBaddie2 = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                          'speed': random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED),
                          'surface': pygame.transform.scale(klingon_image, (baddieSize, baddieSize))}

            baddies.append(newBaddie1)
            baddies.append(newBaddie2)
            
        # Move the player around.
        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if move_right and player_rect.right < WINDOW_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if move_down and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.move_ip(0, PLAYER_MOVE_RATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(player_rect.centerx, player_rect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverse_cheat and not slow_cheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverse_cheat:
                b['rect'].move_ip(0, -5)
            elif slow_cheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in baddies:
            if b['rect'].top > WINDOW_HEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        window_surface.fill(BACKGROUND_COLOR)

        # Draw the score and top score.
        draw_text('Score: %s' % score, font, window_surface, 10, 0)
        draw_text('Top Score: %s' % topScore, font, window_surface, 10, 40)

        # Draw the player's rectangle
        window_surface.blit(player_image, player_rect)

        # Draw each baddie
        for b in baddies:
            window_surface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if player_has_hit_baddie(player_rect, baddies):
            if score > topScore:
                topScore = score  # set new top score
            break

        main_clock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    game_over_sound.play()

    draw_text('GAME OVER', font, window_surface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))
    draw_text('Press a key to play again.', font, window_surface, (WINDOW_WIDTH / 3) - 80, (WINDOW_HEIGHT / 3) + 50)
    pygame.display.update()
    wait_for_player_to_press_key()

    game_over_sound.stop()
