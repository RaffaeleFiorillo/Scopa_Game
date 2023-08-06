from pygame import Surface
from pygame.display import set_mode, set_caption, set_icon
from pygame.image import load
from pygame.time import Clock

COO_CARDS = {"table": [(428, 250), (564, 250), (312, 250), (670, 250), (816, 250), (186, 250), (942, 250)],
             "player": [(x, 430) for x in range(300, 621, 160)]}
CARD_SCALES = {"table": (85, 147), "player": (150, 270), "player-ai": (42, 73)}

FPS = 30
card_type = "Piacentine"
WIDTH, HEIGHT = 1080, 720
BG_COLOR = (0, 0, 0)  # default is (0, 150, 150)
BG = Surface((WIDTH, HEIGHT))
BG.fill(BG_COLOR)  # set screen with background color
CLOCK = Clock()
SCREEN = set_mode((WIDTH, HEIGHT))
set_caption("Scopa")  # the name of the game on the window
set_icon(load("assets/card-icon.png").convert_alpha())  # the logo of the game on the window
