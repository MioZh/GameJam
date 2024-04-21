import pygame
import sys
import random
import time
from modl.db import get_quetion
from modl.model import check_letter, check_letter_in_list, remote_letter


def start_Field_of_Dreams():
    # Инициализация Pygame
    pygame.init()

    # Размеры экрана
    screen_width = 800
    screen_height = 600
    music_file = "song/field_of_song.mp3"  # Путь к музыке
    pygame.mixer.music.load(music_file)

    correct = "song/yes_letter.mp3"
    correct = pygame.mixer.Sound(correct)

    wrong = "song/no_letter.mp3"
    wrong = pygame.mixer.Sound(wrong)

    exit_song = "song/exit_field.mp3"
    exit_song = pygame.mixer.Sound(exit_song)

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 8)
    font_bold_no = pygame.font.Font("fonts/press.ttf", 14)

    # Создание экрана
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Field of Wonders")

    # Размеры и положение игровой области
    game_area_width = 640  # Ширина сетки 16 * 40
    game_area_height = 200
    game_area_x = 80  # Уменьшено смещение по X для центрирования
    game_area_y = 40

    edit_txt = "Welcome to the Field \nof Wonders!"
    gg_txt = "Thank you"
    #попытка пользователя
    attempt = 5


    # фотографии 
    backgraund = pygame.image.load('image/pole_chudes.jpg')
    backgraund = pygame.transform.scale(backgraund, (800, 600))

    quetion_back = pygame.image.load('image/quetions-removebg-preview.png')
    quetion_back = pygame.transform.scale(quetion_back, (800, 100))
    quetion_back = pygame.transform.flip(quetion_back, True, False)


    message_back = pygame.image.load('image/message.png')
    message_back = pygame.transform.scale(message_back, (230, 150))
    message_back = pygame.transform.rotate(message_back, 180)
    message_gg_back = pygame.transform.scale(message_back, (200, 100))
    message_gg_back = pygame.transform.flip(message_gg_back, True, False)
    
    mess_backgraund = pygame.image.load('image/mess_game.png')
    mess_backgraund = pygame.transform.scale(mess_backgraund, (800, 600))

    cont_text = font_bold.render("Continue", True, BLACK)


    # Размеры клетки
    cell_width = game_area_width // 16  # Делим на 16 для 16 клеток в строке
    cell_height = game_area_height // 5 # Делим на 5 для 5 клеток в столбце

    
    # Генерация случайного числа от 1 до 20
    randomNum = random.randint(1, 20)
    quetion = get_quetion(randomNum)
    length = len(quetion[2])
    word = quetion[2]

    quetion_table = font_bold_little.render(quetion[1], True, BLACK)
    quetion_rect = quetion_table.get_rect()
    quetion_rect.center = (400, 50)

    even_and_odd = 0
    if length % 2 == 1:
        even_and_odd = 1

    # Функция для создания сетки клеток
    def create_grid():
        grid = []
        for i in range(16):  # Изменено на 16
            grid.append([])
            for j in range(5):
                # Используем словарь для хранения информации о клетке
                cell_info = {
                    "rect_color": BLUE if j == 2 and (i >= (16 - length) // 2 and i < 16 - (((16 - length) // 2)) - even_and_odd) else WHITE,
                    "x": game_area_x + i * cell_width,
                    "y": game_area_y + j * cell_height,
                    "width": cell_width,
                    "height": cell_height,
                    "border_color": BLACK,
                    "text": ""
                }
                grid[i].append(cell_info)  # Исправлено: добавляем клетку во внутренний список
        return grid
    
    # Создание сетки клеток
    grid = create_grid()

    start_game = False
    text_mess = "You have successfully overcome all \ndifficulties and reached the last \nstage - the field of miracles! Now you \nhave your final test. You are only \nallowed 5 mistakes, if you make more \nyou will lose. Try not to make too \nmany mistakes and end the game with \na victory!"


    cnt_word = (16 - length) // 2  # Изменено на 16


    list_letter = []
    # Основной игровой цикл
    running = True
    quit_game = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not start_game:
                if 530 <= event.pos[0] <= 675 and 395 <= event.pos [1] <= 420:
                    if quit_game == 1:
                        return True
                    elif quit_game == 2:
                        return False
                    else:
                        start_game = True       
                        pygame.mixer.music.play(-1)

            elif event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z and cnt_word <= length+(16 - length) // 2 and start_game:
                    # Обновляем текст в синем блоке
                    letter = chr(event.key).lower()
                    list_gg_txt = [f"Maybe letter {letter.upper()}?", f"Next letter is {letter.upper()}.", f"I choose letter {letter.upper()}.", f"Let's check if \nthere is letter {letter.upper()}."]
                    gg_txt = random.choice(list_gg_txt)
                    if check_letter_in_list(letter, list_letter):
                        edit_txt = f"This letter \nhas already \nbeen selected \npreviously. Please \nchoose another one."
                    else:
                        list_letter.append(letter)
                        if check_letter(letter, word):
                            correct.play()
                            edit_txt = f"Let's reveal the \nletter {letter.upper()}."
                            i = cnt_word
                            for let in quetion[2]:
                                if letter == let:
                                    grid[i][2]["text"] = letter.upper()
                                i += 1
                            word = remote_letter(letter, word)
                        elif attempt == 2:
                            wrong.play()
                            attempt -= 1
                            edit_txt = "Sorry, but that \nletter is not in the \nword. You have one \nattempt left, use \nit wisely."
                        elif attempt > 2:
                            wrong.play()
                            attempt -= 1
                            edit_txt = f"You didn't guess, \nyou have only {attempt} \nattempts left."
                        elif attempt == 1:
                            pygame.mixer.music.pause()
                            exit_song.play()
                            edit_txt = f"You lost, the word was \n{quetion[2].upper()}."
                            quit_game = 2
                    if not word:
                        pygame.mixer.music.pause()
                        exit_song.play()
                        edit_txt = "Congratulations, \nyou guessed \nthe word correctly!!"
                        quit_game = 1
                        

        # Заливка фона
        screen.fill(WHITE)
        screen.blit(backgraund, (0, 0))
        
        # Рисуем рамку игровой области
        pygame.draw.rect(screen, BLACK, (game_area_x, game_area_y, game_area_width, game_area_height), 2)
        
        # Рисуем заштрихованные клетки и текст
        for i in range(16):  # Изменено на 16
            for j in range(5):
                pygame.draw.rect(screen, grid[i][j]["rect_color"], (grid[i][j]["x"] + 1, grid[i][j]["y"] + 1, grid[i][j]["width"] - 2, grid[i][j]["height"] - 2), 0)
                pygame.draw.rect(screen, grid[i][j]["border_color"], (grid[i][j]["x"], grid[i][j]["y"], grid[i][j]["width"], grid[i][j]["height"]), 1)
                # Рисуем текст
                
                text_surface = font_bold.render(grid[i][j]["text"], True, WHITE)
                text_rect = text_surface.get_rect(center=(grid[i][j]["x"] + grid[i][j]["width"] // 2, grid[i][j]["y"] + grid[i][j]["height"] // 2))
                screen.blit(text_surface, text_rect)

        screen.blit(quetion_back, (0, 10))
        screen.blit(quetion_table, quetion_rect)

        if start_game:
            screen.blit(message_gg_back, (180, 370))
            screen.blit(message_back, (400, 360))

            # ответы героя
            lines_gg = gg_txt.split('\n')
            posi_y = 420
            for line in lines_gg:
                gg_txt_block = font_bold_little.render(line, True, BLACK)
                screen.blit(gg_txt_block, (200, posi_y))
                posi_y +=15

            # ответы ведущего
            lines = edit_txt.split('\n')
            pos_y = 420
            for line in lines:
                edit_txt_block = font_bold_little.render(line, True, BLACK)
                screen.blit(edit_txt_block, (430, pos_y))
                pos_y +=15
        
        if not start_game:
            screen.blit(mess_backgraund, (0, -25))
            screen.blit(cont_text, (530, 400))
            lines_gg = text_mess.split('\n')
            posi_y = 180
            for line in lines_gg:
                gg_txt_block = font_bold_no.render(line, True, BLACK)
                screen.blit(gg_txt_block, (130, posi_y))
                posi_y +=20
        # Обновление экрана
        pygame.display.flip()
        if quit_game == 1 and start_game:
            text_mess = "Congratulations! You have successfully \nhelped our hero return to their time.\nYour efforts and perseverance were \ninvaluable.Now, they can continue their \nadventure, inspired by your assistance.\nBut remember, the world is full of many \nmore mysteries and challenges.Please, \ndon't forget to come back and explore \nnew horizons with us!"
            time.sleep(3)
            start_game = False
        elif quit_game == 2 and start_game:
            text_mess = "What a pity, the last challenge wasn't \neasy, so I understand you... Don't be \nupset. New challenges are an \nopportunity to become even stronger \nand smarter. I'm sure someday you'll \nhelp Tyler return to the present \ntime and complete his adventure. Your \nsupport and ability to overcome \nobstacles are what makes you a true hero!"
            time.sleep(3)
            start_game = False
    # Выход из Pygame
    pygame.quit()
    sys.exit()
