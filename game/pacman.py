import pygame, time
from game.player import *
from game.enemies import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

def start_pacman():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 40)
    game_over = False
    win = False
    score = 0
    time = 0
    start_game = False

    mess_backgraund = pygame.image.load('image/mess_game.png')
    mess_backgraund = pygame.transform.scale(mess_backgraund, (800, 600))

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 14)

    cont_text = font_bold.render("Continue", True, BLACK)

    text_mess = "You coped very well with the maze, but \nnow it's time for a new challenge. Will \nyou be able to collect all the coins \nwhile running away from enemies? This \nwill be a real test of your skills and \nreaction speed."

    player = Player(32,128,"game/images_pacman/player.png")
    # Create the blocks that will set the paths where the player can go
    horizontal_blocks = pygame.sprite.Group()
    vertical_blocks = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    for i,row in enumerate(environment()):
        for j,item in enumerate(row):
            if item == 1:
                horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
            elif item == 2:
                vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
    # Add the dots inside the game
    for i,row in enumerate(environment()):
        for j,item in enumerate(row):
            if item != 0:
                dot = Ellipse(j*32+12,i*32+12,WHITE,8,8)
                dots.add(dot)

    enemies.add(Slime(288,96,0,2))
    enemies.add(Slime(288,320,0,-2))
    enemies.add(Slime(160,64,2,0))
    enemies.add(Slime(448,64,-2,0))
    enemies.add(Slime(640,448,2,0))
    
    game_over_sound = pygame.mixer.Sound("game/audio_pacman/game_over_sound.mp3")
    win_sound = pygame.mixer.Sound("game/audio_pacman/win_sound.mp3")

    the_end_game = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not start_game:
                if 530 <= event.pos[0] <= 675 and 395 <= event.pos [1] <= 420:
                    if the_end_game == 1:
                        start_game = False
                        return True, time // 30
                    elif the_end_game == 2:
                        return False, time // 30
                    else:
                        start_game = True
            elif event.type == pygame.KEYDOWN and start_game:
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()
            
            elif event.type == pygame.KEYUP and start_game:
                if event.key == pygame.K_RIGHT:
                    player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    player.stop_move_left()
                elif event.key == pygame.K_UP:
                    player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    player.stop_move_down()
        if start_game:
            player.update(horizontal_blocks, vertical_blocks)

        block_hit_list = pygame.sprite.spritecollide(player, dots, True)
        if block_hit_list :
            score += 1

        if start_game:
            time += 1

        if len(dots) == 0:
            win = True
            game_over = True
        
        block_hit_list = pygame.sprite.spritecollide(player, enemies, True)
        if block_hit_list:
            text_mess = f"Oh... failure! Now Tyler Chronos can't \nreturn to his time.Your efforts were \nmagnificent, but sometimes fate has its \nown plans.But don't worry, your \nadventures are just beginning."
            game_over_sound.play()
            start_game = False
            the_end_game = 2

        
        game_over = player.game_over
        if start_game:
            enemies.update(horizontal_blocks, vertical_blocks)
        
        screen.fill(BLACK)
        horizontal_blocks.draw(screen)
        vertical_blocks.draw(screen)
        draw_environment(screen)
        dots.draw(screen)
        enemies.draw(screen)
        screen.blit(player.image, player.rect)
        text = font_bold_little.render("Score: " + str(score), True, WHITE)
        screen.blit(text, [20, 20])

        if win:
            start_game = False
            text_mess = f"Wow! You completed the second \nstage successfully in {time//30} seconds. But \nthat is not all..."
            the_end_game = 1

        if not start_game:
            screen.blit(mess_backgraund, (0, -25))
            screen.blit(cont_text, (530, 400))
            lines_gg = text_mess.split('\n')
            posi_y = 180
            for line in lines_gg:
                gg_txt_block = font_bold_little.render(line, True, BLACK)
                screen.blit(gg_txt_block, (130, posi_y))
                posi_y +=20
        pygame.display.flip()
        clock.tick(30)
        
    time.sleep(2)
    pygame.quit()

