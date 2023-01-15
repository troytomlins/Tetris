import random
import pygame
from Tetris import Tetris

"""
Runs the game, displays UI, and handles events
"""

# set up
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 20
game = Tetris(20, 10)
counter = 0

pressing_down = False


while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0
    
    if counter % (fps // (1 + ((game.level-1) * .25)) // 2) == 0 or pressing_down:
        if game.state == "start":
            x = game.go_down()
            if x == 0:
                game.state = "gameover"
                game.check_highscore()
    
    # key press checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                x = game.go_space()
                if x == 0:
                    game.state = "gameover"
                    game.check_highscore()
            if event.key == pygame.K_ESCAPE:
                game = Tetris(20, 10)
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    
    screen.fill(WHITE)
    
    # draws current game
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])


    # End text
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    font2 = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text1 = font.render("Level: " + str(game.level), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))
    
    screen.blit(text, [10, 10])
    screen.blit(text1, [155, 10])    
    
    
    # High scores text
    scores = game.read_scores()
    high_scores = font.render("Highscores", True, BLACK)
    hs = font.render("1: " + str(scores[0]), True, BLACK)
    hs1 = font.render("2: " + str(scores[1]), True, BLACK)
    hs2 = font.render("3: " + str(scores[2]), True, BLACK)
    hs3 = font.render("4: " + str(scores[3]), True, BLACK)
    hs4 = font.render("5: " + str(scores[4]), True, BLACK)
    
    screen.blit(high_scores, [280, 10])
    screen.blit(hs, [310, 80])
    screen.blit(hs1, [310, 110])
    screen.blit(hs2, [310, 140])
    screen.blit(hs3, [310, 170])
    screen.blit(hs4, [310, 200])


    # Display game over text
    if game.state == "gameover":
        screen.blit(text_game_over, [40, 230])
        screen.blit(text_game_over1, [50, 280])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()