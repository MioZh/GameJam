import pygame
import sys
from game.field_of_dreams import start_Field_of_Dreams
from game.labyrinth import start_labyrinth
from game.pacman import start_pacman

# Инициализация Pygame
def starting_fields():
    pygame.init()

    # Размеры окна
    WIDTH, HEIGHT = 800, 600
    # Цвета
    WHITE = (255, 255, 255)


    music_file = "song/step_tyler.mp3"  # Путь к музыке
    step_sound = pygame.mixer.Sound(music_file)
    

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 14)

    text_mess = "In the deep laboratories, scientist \nTyler Chronos and his colleagues \nworked on an experimental time \nmachine. They sought to create \na device with which they could \ntravel through time. Despite the \nwarnings and suggestions, Tyler was \nconvinced of the success of his \nproject. One day, when they \nintroduced the time machine, \nsomething went wrong. A sudden \nglitch took Tyler out of time and \nspace, leaving him in a time \nlabyrinth."
    font_bold.render(text_mess, True, (255, 255, 255))

    start_steps = False

    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Анимация ходьбы")

    backgraund = pygame.image.load('image/backgraund.jpg')
    backgraund = pygame.transform.scale(backgraund, (800, 600))

    mess_backgraund = pygame.image.load('image/mess_start.png')
    mess_backgraund = pygame.transform.scale(mess_backgraund, (800, 600))

    cont_text = font_bold.render("Continue", True, WHITE)

    # Загрузка изображений для анимации ходьбы
    walk_images_left = [pygame.image.load('player/left_a.png'),
                pygame.image.load('player/left_b.png'),
                pygame.image.load('player/left_c.png')]

    walk_images_right = [pygame.image.load('player/right_a.png'),
                pygame.image.load('player/right_c.png'),
                pygame.image.load('player/right_b.png')]

    walk_images_up = [pygame.image.load('player/up_a.png'),
                pygame.image.load('player/up_b.png'),
                pygame.image.load('player/up_c.png')]



    # Начальное положение персонажа
    x, y = 700, 500

    # Индекс текущего кадра анимации
    current_frame = 0

    left_step = False
    up_step = True
    right_step = False

    begin = False

    # Скорость анимации (чем меньше, тем быстрее)
    animation_speed =  100
    walk_images = walk_images_up
    # Основной игровой цикл
    running = True
    while running:
        screen.blit(backgraund, (0, 0))
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= event.pos[0] <= 590 and 500 <= event.pos [1] <= 520:
                    begin = True
        
        if not begin:
            screen.blit(mess_backgraund, (0, 0))
            screen.blit(cont_text, (450, 500))
            lines_gg = text_mess.split('\n')
            posi_y = 75
            for line in lines_gg:
                gg_txt_block = font_bold_little.render(line, True, WHITE)
                screen.blit(gg_txt_block, (130, posi_y))
                posi_y +=20
            start_steps = True
        if begin:
            if start_steps:
                step_sound.play(-1)
                start_steps = False
            # Достижение цели и изменение направление
            if y == 460:
                walk_images = walk_images_left
                up_step = False
                left_step = True
                
            if x == 244:
                step_sound.stop()
                start_labyrinth()
                step_sound.play(-1)
                walk_images = walk_images_up
                left_step = False
                up_step = True
                x, y = 150, 400

            if y == 264:
                walk_images = walk_images_right
                up_step = False
                right_step = True

            if x == 470:
                walk_images = walk_images_up
                right_step = False
                up_step = True

            if y == 248:
                step_sound.stop()
                start_pacman()
                step_sound.play(-1)
                x, y = 640, 130
            
            if y == 74:
                walk_images = walk_images_left
                left_step = True
                up_step = False

            if x == 240:
                walk_images = walk_images_up
                left_step = False
                up_step = True

            if y == 50:
                step_sound.stop()
                start_Field_of_Dreams()
                up_step = False
                return True
                


            # Обновляем текущий кадр анимации
            current_frame = (current_frame + 1) % len(walk_images)

            # Скорость движение
            if up_step:
                y -= 8

            if left_step:
                x -= 8

            if right_step:
                x += 8


            # Отображение фона и текущего кадра анимации персонажа
            
            screen.blit(walk_images[current_frame], (x, y))  # x и y - координаты персонажа на экране

        # Обновление экрана
        pygame.display.flip()

        # Задержка для плавности анимации
        pygame.time.delay(animation_speed)
        

    # Завершение работы Pygame
    pygame.quit()
    sys.exit()
