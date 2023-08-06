from src.Game.Entities import Deck, Human, AI, TableCards
# from src.Game.scopa_functions import *
# from src.Animations.animation_collection import play_animation
import pygame
from src.global_variables import FPS


class Match:
    def __init__(self, screen, names, clock):
        self.background = pygame.image.load("assets\\background.jpg").convert_alpha()
        self.deck = Deck()
        self.table_cards = TableCards()
        self.turn = None
        self.player1 = Human(names[0])
        self.player2 = AI()
        self.clock = clock
        self.screen = screen

        # the mode says if the player is "choosing" (the card to play), "taking" (cards on the table) or "waiting"
        # (the other player to make a move)
        self.mode = "choice"
        # play_animation(self.screen, "choosing_player")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.table_cards.draw(self.screen)

    def refresh(self):
        self.draw(self.screen)
        pygame.display.update()

    def game_loop(self):
        while len(self.deck.cards):  # if there are no more cards in the deck the match is over
            if not (len(self.player1.cards_in_hand) and len(self.player2.cards_in_hand)):
                self.give_cards()
            mouse_pos = pygame.mouse.get_pos()  # avoid multiples execution of the same function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                # human has clicked and is its turn to choose a card to play
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.mode != "wait":
                    # player has chosen a card in his hand
                    if self.mode == "choice" and self.player1.activate_card(mouse_pos):
                        # changing mode in order to enable the player to take cards on the table
                        self.mode = "take"
                        print(self.mode)
                        # 1- create a list of possible moves for the chosen card
                        # 2- activate the cards on the table that would be taken using the selected card
                    # player has chosen a card on the table
                    elif self.mode == "take" and self.table_cards.activate_cards(mouse_pos):
                        # check if the sum of the cards selected:
                        #   if sum > card chosen to play: deselect all cards on table
                        #   if sum <= card chosen to play: activate flag to show a "press enter to take" label
                        # 1- highlight/de-highlight selected card
                        # 2- highlight the cards in the player's hand which take the combination of selected card on the
                        #    table
                        pass

            self.highlight_hovered_card(mouse_pos)
            self.refresh()
            self.clock.tick(FPS)
        self.end_of_match()

    def end_of_match(self):
        print("Game Over")
        self.deck.show_deck()

    def give_cards(self):
        self.player1.cards_in_hand = self.deck.draw_cards("player")
        # 2- animation of player 1 getting his cards into his hands
        self.player2.cards_in_hand = self.deck.draw_cards("player")
        # 4- animation of player 2 getting his cards into his hands

    def highlight_hovered_card(self, coo_mouse: (int, int)):
        self.player1.highlight_hovered_card(coo_mouse)
        self.table_cards.highlight_hovered_card(coo_mouse)

    def start(self):
        # 1- animation of the cards going to the table: move from deck to table (face down) and the get facing up
        self.table_cards.cards = self.deck.draw_cards("table")  # put the cards on the table
        self.game_loop()  # starting the actual game
