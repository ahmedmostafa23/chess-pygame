import pygame
from math import floor
import sys
import os

pygame.init()

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


bgm_url = resource_path("Assets/bgm/bgm.mp3")
pygame.mixer.music.load(bgm_url)  # 'bgm.mp3'
pygame.mixer.music.play(-1)

# game window as a window with dimensions, a title and an icon
win_width = 768
win_height = 768
win_title = "Chess"
win_icon_url = resource_path("Assets/others/ChessIcon.jpg")
cburl = resource_path("assets/others/Board.png")
win_icon = pygame.image.load(win_icon_url)
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption(win_title)
pygame.display.set_icon(win_icon)

game_loop_ps = 10


def move_board(board, x_a, y_a):
    global win_width
    global win_height
    if (win_width - board.get_image_size() >= x_a >= 0) \
            and (win_height - board.get_image_size() >= y_a >= 0):
        board.set_cords(x_a, y_a)
    else:
        raise ValueError


def display_pieces(board):
    z = board.ready_pieces()
    for img, tup in z:
        window.blit(img, tup)


def display(img, cords):
    window.blit(img, cords)


def display_board(board):
    window.blit(board.get_image(), board.get_board_cords())


def load_image(image):
    return pygame.image.load(image)


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

