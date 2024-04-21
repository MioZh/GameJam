import pygame 
from modl.db import register_user
from game.start import start_backraund
from modl.model import check_password_and_login

def register(button_sound):
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Register")

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 7)

    name_cons = pygame.draw.circle(screen, (255, 255, 255), (545, 115), 15)
    pass_cons = pygame.draw.circle(screen, (255, 255, 255), (280, 260), 15)

    text_name_const0 = font_bold_little.render("Short name should contain at", True, (0, 0, 0))
    text_name_const1 = font_bold_little.render("least three characters and no", True, (0, 0, 0))
    text_name_const2 = font_bold_little.render("more than ten, and it must be", True, (0, 0, 0))
    text_name_const3 = font_bold_little.render("unique.", True, (0, 0, 0))
    #"Short name should contain at least three characters and no more than ten, and it must be unique."
    text_pass_const0 = font_bold_little.render("The password must be at least", True, (0, 0, 0))
    text_pass_const1 = font_bold_little.render("6 characters and no more than", True, (0, 0, 0))
    text_pass_const2 = font_bold_little.render("12, and it must contain at", True, (0, 0, 0))
    text_pass_const3 = font_bold_little.render("least two digits.", True, (0, 0, 0))
    #"The password must be at least 6 characters and no more than 12, and it must contain at least two digits."

    background_image = pygame.image.load("image/register_backgraund.jpg")
    background_image = pygame.transform.scale(background_image, (800, 600))
    background_rect = background_image.get_rect()

    original_image = pygame.image.load('image/but_l.png')
    button_image = pygame.transform.scale(original_image, (180, 80))

    pass_name_image = pygame.image.load('image/pass_name.png')
    pass_name_image = pygame.transform.scale(pass_name_image, (50, 30))

    inputn_image = pygame.image.load('image/input_name.png')
    inputn_image = pygame.transform.scale(inputn_image, (340, 110))

    inputp_image = pygame.image.load('image/input_password.png')
    inputp_image = pygame.transform.scale(inputp_image, (300, 130))

    error_image = pygame.image.load('image/error_ima.png')
    error_image = pygame.transform.scale(error_image, (250, 100))

    mess_const_image = pygame.image.load('image/mess_const-removebg-preview.png')
    mess_const_image = pygame.transform.scale(mess_const_image, (300, 200))
    mess_const_rew_image = pygame.transform.rotate(mess_const_image, 180)
    mess_const_rew_image = pygame.transform.flip(mess_const_rew_image, True, False)


    register_text = font_bold.render("Sign in", True, (255, 255, 255))  # White color
    register_rect = register_text.get_rect()
    register_rect.bottomleft = (440, 400) 

    back_text = font_bold.render("Back", True, (255, 255, 255))  # White color
    back_rect = back_text.get_rect()
    back_rect.bottomleft = (230, 400)

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
                if 415 <= event.pos[0] <= 580 and 345 <= event.pos[1] <= 410 and check_password_and_login(input_username, input_password):
                    if register_user(input_username, input_password):
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
                
        
        pygame.draw.circle(screen, (255, 255, 255), (280, 260), 15)
        screen.blit(background_image, background_rect)  
        
        # Blitting button image onto the screen
        screen.blit(button_image, (register_rect.x - 30, register_rect.y - 30))  # Adjust position to center the button
        screen.blit(button_image, (back_rect.x - 30, back_rect.y - 30))  # Adjust position to center the button
        
        screen.blit(inputn_image, (210, 80))
        screen.blit(inputp_image, (290, 200))


        screen.blit(pass_name_image, (520, 100))
        screen.blit(pass_name_image, (250, 245))

        

        # Blitting text images onto the screen
        screen.blit(register_text, register_rect)
        screen.blit(back_text, back_rect)

        #Enter name and password
        text_username = font_bold.render(input_username, True, (0, 0, 0))
        screen.blit(text_username, (235, 105))
        text_password = font_bold.render(input_password, True, (0, 0, 0))
        screen.blit(text_password, (335, 250))

        # Text name and password
        screen.blit(text_name, (215, 60))
        screen.blit(text_p, (315, 195))

        

        #blittin constructors
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pass_cons.collidepoint(mouse_x, mouse_y):
            screen.blit(mess_const_image, (60, 85))
            screen.blit(text_pass_const0, (100, 150))
            screen.blit(text_pass_const1, (100, 165))
            screen.blit(text_pass_const2, (100, 180))
            screen.blit(text_pass_const3, (100, 195))
        if name_cons.collidepoint(mouse_x, mouse_y):
            screen.blit(mess_const_rew_image, (330, 100))
            screen.blit(text_name_const0, (373, 170))
            screen.blit(text_name_const1, (373, 185))
            screen.blit(text_name_const2, (373, 200))
            screen.blit(text_name_const3, (373, 215))
        
        frame_count += 1
        if frame_count >= time_error:
            blit_error = False


        if blit_error:
            text_error = font_bold_little.render("That name is already taken,", True, (0, 0, 0))
            text_error1 = font_bold_little.render("please try another one.", True, (0, 0, 0))
            screen.blit(error_image, (570, 5))
            screen.blit(text_error, (595, 45))
            screen.blit(text_error1, (595, 60))
        pygame.display.flip()


    pygame.quit()

