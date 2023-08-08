from src import Game
from src.Globals.Configurations.Game import SCREEN, CLOCK
# import src.AI
import pygame
pygame.init()


def main():
    match = Game.Match(SCREEN, ["Raffaele", "R.F.J.8"], CLOCK)
    match.start()


main()
