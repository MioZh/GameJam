import pygame
import random

# Константы для цветов и размеров клеток
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
WIDTH = 29
HEIGHT = 22
MARGIN = 2

# Изображение персонажа
right_photo = pygame.image.load('player/right_c.png')
right_photo = pygame.transform.scale(right_photo, (WIDTH, HEIGHT))
left_photo = pygame.image.load('player/left_c.png')
left_photo = pygame.transform.scale(left_photo, (WIDTH, HEIGHT))

up_photo = pygame.image.load('player/up_c.png')
up_photo = pygame.transform.scale(up_photo, (WIDTH, HEIGHT))
down_photo = pygame.image.load('player/down_c.png')
down_photo = pygame.transform.scale(down_photo, (WIDTH, HEIGHT))

player_photo = right_photo

# Создание сетки для лабиринта
def create_grid():
    grid = []
    for row in range(25):
        grid.append([])
        for column in range(25):
            grid[row].append(1)  # 1 - стена, 0 - проход
    return grid

# Функция для создания случайного пути в лабиринте
def create_maze(grid, row, column):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        new_row = row + 2 * dr
        new_col = column + 2 * dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == 1:
            grid[row + dr][column + dc] = 0
            grid[new_row][new_col] = 0
            create_maze(grid, new_row, new_col)

def has_black_start(grid, row, col):
    if  grid[row][col+1] != 1:
        return True
    return False

def has_black_end(grid, row, col):
    if  grid[row][col-1] != 1:
        return True
    return False

def reset_game():
    global grid, start_row, start_col, end_row, end_col, coins, game_state, player_pos, timer, coin, start_game, the_end_game
    grid = create_grid()
    create_maze(grid, 1, 1)
    start_game = False
    coin = 0
    the_end_game = 0

    start_row = random.randint(1, len(grid) - 2)
    start_col = 0
    while not has_black_start(grid, start_row, start_col):
        start_row = random.randint(1, len(grid) - 2)
        start_col = 0

    end_row = random.randint(1, len(grid) - 2)
    end_col = len(grid[0]) - 1
    while not has_black_end(grid, end_row, end_col):
        end_row = random.randint(1, len(grid) - 2)
        end_col = len(grid[0]) - 1

    grid[start_row][start_col] = 2  # 2 - старт
    grid[end_row][end_col] = 1  # 3 - конец

    available_cells = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0 and (row != start_row or col != start_col):
                available_cells.append((row, col))

    coins = []
    for _ in range(15):
        coin_row, coin_col = random.choice(available_cells)
        coins.append((coin_row, coin_col))

    game_state = "playing"
    player_pos = [start_row, start_col]
    timer = 0



def start_labyrinth():
    global game_state, grid, player_pos, player_photo, timer, coin, start_game, the_end_game

    # Сброс состояния игры и генерация нового лабиринта
    reset_game()
    # Инициализация Pygame
    pygame.init()

    font_bold = pygame.font.Font("fonts/press.ttf", 18)
    font_bold_little = pygame.font.Font("fonts/press.ttf", 14)

    coins_song = "song/coins_song.mp3"
    coins_song = pygame.mixer.Sound(coins_song)

    # Установка размеров экрана
    WINDOW_SIZE = [(WIDTH + MARGIN) * 25 + MARGIN, (HEIGHT + MARGIN) * 25 + MARGIN]
    screen = pygame.display.set_mode(WINDOW_SIZE)


    mess_backgraund = pygame.image.load('image/mess_game.png')
    mess_backgraund = pygame.transform.scale(mess_backgraund, (800, 600))

    cont_text = font_bold.render("Continue", True, BLACK)

    text_mess = "Here's the first challenge: you need to \ncollect all the coins, only then will \nthe doors leading to the next level \nopen. I wish you good luck!"

    # Установка заголовка окна
    pygame.display.set_caption("Return to Present")

    # Основной цикл программы
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not start_game:
                if 530 <= event.pos[0] <= 675 and 395 <= event.pos [1] <= 420:
                    if the_end_game == 1:
                        start_game = False
                        return True, timer // 60
                    elif the_end_game == 2:
                        return False, timer // 60
                    else:
                        start_game = True
                        
            elif event.type == pygame.KEYDOWN and game_state == "playing" and start_game:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if player_pos[0] > 0 and grid[player_pos[0] - 1][player_pos[1]] != 1 and start_game:
                        player_pos[0] -= 1  # Вверх
                        player_photo = up_photo
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if player_pos[0] < len(grid) - 1 and grid[player_pos[0] + 1][player_pos[1]] != 1 and start_game:
                        player_pos[0] += 1  # Вниз
                        player_photo = down_photo
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if player_pos[1] > 0 and grid[player_pos[0]][player_pos[1] - 1] != 1:
                        player_pos[1] -= 1  # Влево
                        player_photo = left_photo
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if player_pos[1] < len(grid[0]) - 1 and grid[player_pos[0]][player_pos[1] + 1] != 1 and start_game:
                        player_pos[1] += 1  # Вправо
                        player_photo = right_photo

        # Проверка сбора монеток
        coins_to_remove = []
        for coin_row, coin_col in coins:
            if player_pos == [coin_row, coin_col]:
                coins_to_remove.append((coin_row, coin_col))
                coins_song.play()
                coin += 1 


        for coin_row, coin_col in coins_to_remove:
            coins.remove((coin_row, coin_col))

        # Проверка достижения финиша
        if player_pos == [end_row, end_col]:
            start_game = False
            the_end_game = 1
            text_mess = f"Congratulations! You have successfully \ncompleted the first stage in {timer//60} seconds. \nBut remember, this is just the beginning. \nDon't relax, even greater challenges \nawait you!"

            

        # Обновление таймера только в режиме игры
        if game_state == "playing" and start_game:
            timer += 1 
                
        
        if coin == 15:
            grid[end_row][end_col] = 3

        # Отрисовка лабиринта, персонажа и золотых монеток
        screen.fill(BLACK)
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                if grid[row][column] == 1:
                    color = WHITE
                elif grid[row][column] == 2:
                    color = RED
                elif grid[row][column] == 3:
                    color = GREEN
                else:
                    color = BLACK
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN,
                                                (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        for coin_row, coin_col in coins:
            pygame.draw.circle(screen, GOLD, ((MARGIN + WIDTH) * coin_col + MARGIN + WIDTH // 2,
                                            (MARGIN + HEIGHT) * coin_row + MARGIN + HEIGHT // 2),
                            min(WIDTH, HEIGHT) // 4)

        screen.blit(player_photo, ((MARGIN + WIDTH) * player_pos[1] + MARGIN,
                                    (MARGIN + HEIGHT) * player_pos[0] + MARGIN))

        # Отрисовка таймера
        font = pygame.font.Font(None, 36)
        text = font.render("Timer: " + str(timer // 60), True, RED)
        screen.blit(text, (10, 10))

        if not start_game:
            screen.blit(mess_backgraund, (0, -25))
            screen.blit(cont_text, (530, 400))
            lines_gg = text_mess.split('\n')
            posi_y = 180
            for line in lines_gg:
                gg_txt_block = font_bold_little.render(line, True, BLACK)
                screen.blit(gg_txt_block, (130, posi_y))
                posi_y +=20
        # Обновление экрана
        pygame.display.flip()

        # Задержка для обновления экрана
        clock.tick(60)
