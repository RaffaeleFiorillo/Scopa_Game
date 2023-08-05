from src.Game.Entities import Card, Deck, Human, AI
# from src.Animations.animation_collection import play_animation
import pygame


class Match:
    def __init__(self, screen, names, clock):
        self.background = pygame.image.load("assets\\background.jpg").convert_alpha()
        self.deck = Deck()
        self.cards_on_table: [Card] = []
        self.turn = None
        self.player1 = Human(names[0])
        self.player2 = AI()
        self.clock = clock
        self.screen = screen
        # play_animation(self.screen, "choosing_player")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        [carta.draw(self.screen) for carta in self.cards_on_table]

    def refresh(self):
        self.draw(self.screen)
        pygame.display.update()

    def game_loop(self):
        while len(self.deck.cards):  # if there are no more cards in the deck the match is over
            if not (len(self.player1.cards_in_hand) and len(self.player2.cards_in_hand)):
                self.dai_le_carte()
            mouse_pos = pygame.mouse.get_pos()  # avoid multiples execution of the same function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # human has selected a card
                    print("click")
                    if self.player1.activate_cards_in_hand(mouse_pos):  # card selected is in the h-player's hand
                        print("card activated")
                        # 1- create a list of possible moves for the chosen card
                        # 2- activate the cards on the table that would be taken using the selected card
                        pass
                    elif None:  # card selected is on the hand
                        # 1- highlight/de-highlight selected card
                        # 2- highlight the cards in the player's hand which take the combination of selected card on the
                        #    table
                        pass

            self.highlight_hovered_card(mouse_pos)
            self.refresh()
            self.clock.tick(60)
        self.end_of_match()

    def end_of_match(self):
        print("Game Over")
        self.deck.show_deck()

    def dai_le_carte(self):
        self.player1.cards_in_hand = self.deck.draw_cards("mano")
        # 2- animation of player 1 getting his cards into his hands
        self.player2.cards_in_hand = self.deck.draw_cards("mano")
        # 4- animation of player 2 getting his cards into his hands

    def highlight_hovered_card(self, coo_mouse: (int, int)):
        for card in self.player1.cards_in_hand:
            if card.mouse_is_inside(coo_mouse):
                card.hoovered = True
                return None
            else:
                card.hoovered = False
        for card in self.cards_on_table:
            if card.mouse_is_inside(coo_mouse):
                card.hoovered = True
                return None
            else:
                card.hoovered = False

    def start(self):
        # 1- animation of the cards going to the table: move from deck to table (face down) and the get facing up
        self.cards_on_table = self.deck.draw_cards("tavolo")  # put the cards on the table
        self.game_loop()  # starting the actual game
