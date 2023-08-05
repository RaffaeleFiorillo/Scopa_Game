from src import Game
import src.AI
import pygame
pygame.init()

WIDTH, HEIGHT = 1080, 720
BG_COLOR = (0, 0, 0)  # default is (0, 150, 150)
BG = pygame.Surface((WIDTH, HEIGHT))
BG.fill(BG_COLOR)  # set screen with background color
FPS = 30
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scopa")


def main():
    partita = Game.partita.PartitaScopa(SCREEN, ["Raffaele", "R.F.J.8"], CLOCK)
    partita.inizia()


main()
