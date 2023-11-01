from src.Game import Matches
from src.Globals.Configurations.Game import SCREEN, CLOCK
# import src.AI
import pygame
pygame.init()


def main():
    match = Matches.Human_VS_AI_Match(SCREEN,  CLOCK, ["Raffaele", "R.F.J.8"])
    match.start()


main()
