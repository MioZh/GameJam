import pygame 
music_playing = 0

def off_on_song():
    global music_playing
    if music_playing == 0:
        music_file = "song/music-backgraund_eISPYRiE.mp3"  # Путь к музыке
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
    elif music_playing % 2 == 0:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    music_playing += 1


def song_normal():
    music_file = "song/music-backgraund_eISPYRiE.mp3"  # Путь к музыке
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)

def check_password_and_login(username, password):
    if len(username) > 2 and len(password) > 5:
        letter_count = 0
        for char in password:
            if char.isalpha():
                letter_count += 1
                if letter_count > 2:
                    return True
    return False



def check_letter(letter, word):
    if letter in word:
        result = word.replace(letter, '')
        return True
    return False


def remote_letter(letter, word):
    word = word.replace(letter, '')
    return word



def check_letter_in_list(letter, list_let):
    if letter in list_let:
        return True
    return False
    

