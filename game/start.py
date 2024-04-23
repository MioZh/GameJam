import pygame
import webbrowser
from game.start_field import starting_fields
from modl.model import off_on_song, song_normal
from game.rating import rating

def open_webpage():
    webbrowser.open('https://miozh.github.io/web')  

def start_backraund(button_sound, username):
    pygame.init()

    WIDTH, HEIGHT = 800, 600


    font_bold = pygame.font.Font("fonts/press.ttf", 18)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("start")

    backgraund = pygame.image.load('image/start_backgraund.jpg')
    backgraund = pygame.transform.scale(backgraund, (800, 600))

    button = pygame.image.load('image/but_l.png')
    button = pygame.transform.scale(button, (180, 80))

    song_on = pygame.image.load('image/song_on.png')
    song_on = pygame.transform.scale(song_on, (35, 35))

    song_off = pygame.image.load('image/song_off.png')
    song_off = pygame.transform.scale(song_off, (35, 35))

    document_icon = pygame.image.load('image/document_icon.png')
    document_icon = pygame.transform.scale(document_icon, (35, 35))

    song_image = song_on

    little_button = pygame.image.load('image/but_q.png')
    little_button = pygame.transform.scale(little_button, (80, 80))

    button_rect_start = button.get_rect()
    button_rect_start.center = (WIDTH // 2, 200)
    
    button_rect_record = button.get_rect()
    button_rect_record.center = (WIDTH // 2, 290)

    button_rect_exit = button.get_rect()
    button_rect_exit.center = (WIDTH // 2, 380)

    log_text = font_bold.render("Start", True, (255, 255, 255)) 
    log_rect = log_text.get_rect()
    log_rect.center = (WIDTH // 2, 200) 

    rec_text = font_bold.render("Rating", True, (255, 255, 255)) 
    rec_rect = rec_text.get_rect()
    rec_rect.center = (WIDTH // 2, 290) 

    exit_text = font_bold.render("Exit", True, (255, 255, 255)) 
    exit_rect = exit_text.get_rect()
    exit_rect.center = (WIDTH // 2, 380) 



    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 315 <= event.pos[0] <= 480 and 165 <= event.pos[1] <= 230:
                    button_sound.play()
                    if song_image == song_on:
                        pygame.mixer.music.pause()
                        
                    starting_fields(username)
                    song_normal()
                    if song_image == song_off:
                        pygame.mixer.music.pause()
                if 315 <= event.pos[0] <= 480 and 260 <= event.pos[1] <= 320:
                    button_sound.play()
                    rating(button_sound, username)
                if 315 <= event.pos[0] <= 480 and 350 <= event.pos[1] <= 410:
                    button_sound.play()
                    return False
                
                if 25 <= event.pos[0] <= 95 and 505 <= event.pos[1] <= 570:
                    button_sound.play()
                    if song_image == song_off:
                        song_image = song_on

                    else:
                        song_image = song_off
                    off_on_song()

                if 115 <= event.pos[0] <= 185 and 505 <= event.pos[1] <= 570:
                    button_sound.play()
                    open_webpage()

        screen.blit(backgraund, (0, 0))
        screen.blit(button, button_rect_start)
        screen.blit(log_text, log_rect)

        screen.blit(button, button_rect_record)
        screen.blit(rec_text, rec_rect)

        screen.blit(button, button_rect_exit)
        screen.blit(exit_text, exit_rect)

        screen.blit(little_button, (20, 500))
        screen.blit(little_button, (110, 500))

        screen.blit(song_image, (45, 520))
        screen.blit(document_icon, (135, 520))

        pygame.display.flip()
        
    pygame.quit()
