import src.Game.Objects as Objects
from src.Animations.animation_collection import play_animation
import pygame


class PartitaScopa:
    def __init__(self, screen, nomi, clock):
        self.sfondo = pygame.image.load("assets\\sfondo.jpg").convert_alpha()
        self.mazzo = Objects.Mazzo()
        self.carte_sul_tavolo: [Objects.Carta] = "Vuoto"
        self.turno = None
        self.giocatore1 = Objects.GiocatoreHumano(nomi[0])
        self.giocatore2 = Objects.GiocatoreAI()
        self.clock = clock
        self.screen = screen
        # play_animation(self.screen, "choosing_player")

    def draw(self, screen):
        screen.blit(self.sfondo, (0, 0))
        self.giocatore1.draw(self.screen)
        self.giocatore2.draw(self.screen)
        [carta.draw(self.screen) for carta in self.carte_sul_tavolo]

    def refresh(self):
        self.draw(self.screen)
        pygame.display.update()

    def gioco(self):
        while len(self.mazzo.carte):  # non ci sono piu carte nel mazzo. La partita è finita
            if not (len(self.giocatore1.carte_in_mano) and len(self.giocatore2.carte_in_mano)):
                self.dai_le_carte()
            mouse_pos = pygame.mouse.get_pos()  # avoid multiples execution of the same function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # human has selected a card
                    print("click")
                    if self.giocatore1.activate_cards_in_hand(mouse_pos):  # card selected is in the h-player's hand
                        print("card activated")
                        # 1- create a list of possible moves for the chosen card
                        # 2- activate the cards on the table that would be taken using the selected card
                        pass
                    elif None:  # card selected is on the hand
                        # 1- highlight/de-highlight selected card
                        # 2- highlight the cards in the player's hand which take the combination of selected card on the
                        #    table
                        pass

            self.evidenzia_carta_sotto_mouse(mouse_pos)
            self.refresh()
            self.clock.tick(60)
        self.fine_partita()

    def fine_partita(self):
        print("Game Over")
        pass

    def dai_le_carte(self):
        self.giocatore1.carte_in_mano = self.mazzo.prendi_carte("mano")
        # 2- animation of player 1 getting his cards into his hands
        self.giocatore2.carte_in_mano = self.mazzo.prendi_carte("mano")
        # 4- animation of player 2 getting his cards into his hands

    def evidenzia_carta_sotto_mouse(self, coo_mouse: (int, int)):
        for carta in self.giocatore1.carte_in_mano:
            if carta.mouse_dentro(coo_mouse):
                carta.hoovered = True
                return None
            else:
                carta.hoovered = False
        for carta in self.carte_sul_tavolo:
            if carta.mouse_dentro(coo_mouse):
                carta.hoovered = True
                return None
            else:
                carta.hoovered = False

    def inizia(self):
        # 1- animation of the cards going to the table: move from deck to table (face down) and the get facing up
        self.carte_sul_tavolo = self.mazzo.prendi_carte("tavolo")  # put the cards on the table
        self.gioco()  # starting the actual game

