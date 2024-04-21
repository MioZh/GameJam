import pygame 
from modl.db import check_credentials
from game.start import start_backraund

def log(button_sound):
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Log")

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 7)

    background_image = pygame.image.load("image/register_backgraund.jpg")
    background_image = pygame.transform.scale(background_image, (800, 600))
    background_rect = background_image.get_rect()

    original_image = pygame.image.load('image/but_l.png')
    # Resize image
    button_image = pygame.transform.scale(original_image, (180, 80))

    inputn_image = pygame.image.load('image/input_name.png')
    inputn_image = pygame.transform.scale(inputn_image, (340, 110))

    inputp_image = pygame.image.load('image/input_password.png')
    inputp_image = pygame.transform.scale(inputp_image, (300, 130))

    log_text = font_bold.render("Log in", True, (255, 255, 255))  # White color
    log_rect = log_text.get_rect()
    log_rect.bottomleft = (440, 400) 

    back_text = font_bold.render("Back", True, (255, 255, 255))  # White color
    back_rect = back_text.get_rect()
    back_rect.bottomleft = (230, 400)

    error_image = pygame.image.load('image/error_ima.png')
    error_image = pygame.transform.scale(error_image, (250, 100))

    text_name = font_bold.render("Enter name:", True, (255, 255, 255))  # White color
    text_p = font_bold.render("Enter password:", True, (255, 255, 255))  # White color

    blit_error = False
    time_error = 0
    frame_count = 0

    input_active = ""
    input_username = ""
    input_password = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 220 <= event.pos[0] <= 515 and 85 <= event.pos [1] <= 140:
                    input_active = "username"
                if 320 <= event.pos[0] <= 585 and 225 <= event.pos[1] <= 290:
                    input_active = "password"
                if 205 <= event.pos[0] <= 375 and 345 <= event.pos[1] <= 410:
                    button_sound.play()
                    return True
                if 415 <= event.pos[0] <= 580 and 345 <= event.pos[1] <= 410 and len(input_username) > 2 and len(input_password) > 5:
                    if check_credentials(input_username, input_password):
                        button_sound.play()
                        start_backraund(button_sound, input_username)
                        input_username = ""
                        input_password = ""
                        input_active = ""
                        return True
                    else:
                        # Error image blit
                        time_error = 50*60
                        blit_error = True
                        frame_count = 0



            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if input_active == "username":
                        input_username = input_username[:-1]
                    elif input_active == "password":
                        input_password = input_password[:-1]
                else:
                    if input_active == "username" and len(input_username) < 10 and event.unicode.isalnum():
                        input_username += event.unicode
                    elif input_active == "password"  and len(input_password) < 12 and event.unicode.isalnum():
                        input_password += event.unicode
                
        screen.blit(background_image, background_rect)
        
        # Blitting button image onto the screen
        screen.blit(button_image, (log_rect.x - 30, log_rect.y - 30))  # Adjust position to center the button
        screen.blit(button_image, (back_rect.x - 30, back_rect.y - 30))  # Adjust position to center the button
        
        screen.blit(inputn_image, (210, 80))
        screen.blit(inputp_image, (290, 200))

        # Blitting text images onto the screen
        screen.blit(log_text, log_rect)
        screen.blit(back_text, back_rect)

        #Enter name and password
        text_username = font_bold.render(input_username, True, (0, 0, 0))
        screen.blit(text_username, (235, 105))
        text_password = font_bold.render("*" * len(input_password), True, (0, 0, 0))
        screen.blit(text_password, (335, 255))

        # Text name and password
        screen.blit(text_name, (215, 60))
        screen.blit(text_p, (315, 195))


        frame_count += 1
        if frame_count >= time_error:
            blit_error = False

        if blit_error:
            text_error = font_bold_little.render("Invalid username or", True, (0, 0, 0))
            text_error1 = font_bold_little.render("password", True, (0, 0, 0))
            screen.blit(error_image, (570, 5))
            screen.blit(text_error, (595, 45))
            screen.blit(text_error1, (595, 60))

        pygame.display.flip()

    pygame.quit()

