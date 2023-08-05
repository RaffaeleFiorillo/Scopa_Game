import random
import pygame

COO_CARTE = {"tavolo": [(428, 250), (564, 250), (312, 250), (670, 250), (186, 250), (816, 250), (60, 250), (942, 250)],
             "mano": [(x, 430) for x in range(300, 621, 160)]}
SCALA_CARTA = {"tavolo": (85, 147), "mano": (150, 270), "hand-ai": (42, 73)}


class Carta:
    def __init__(self, numero, seme):
        self.numero = numero  # number between 1 and 10 representing the value of the card
        self.seme = seme  # represents the "house" of the card: Denara, Bastoni, Spade, Coppe
        self.img_dir = f"assets/{seme}/{numero}.png"  # directory of the image of the card
        self.attiva = False  # card has been selected
        self.hoovered = False  # card has the cursor on it
        self.image = None  # image of the card
        self.coo = None  # where the card is printed on the screen
        self.size = None  # size of the card. It depends if the card is on the table (small) or in player's hand (big)

    def carica_carta(self, tipo, ordine):
        image = pygame.image.load(self.img_dir).convert_alpha()
        self.image = pygame.transform.scale(image, SCALA_CARTA[tipo])
        self.coo = COO_CARTE[tipo][ordine]
        self.size = SCALA_CARTA[tipo]

    def mouse_dentro(self, coo_mouse: (int, int)):
        cursor_x, cursor_y = coo_mouse[0], coo_mouse[1]
        dentro_orizontalmente = self.coo[0] <= cursor_x <= self.coo[0] + self.size[0]
        dentro_verticalmente = self.coo[1] <= cursor_y <= self.coo[1] + self.size[1]
        self.hoovered = True if (dentro_orizontalmente and dentro_verticalmente) else False
        return self.hoovered

    def draw(self, screen):
        if self.attiva:
            print("active")
            pygame.draw.rect(screen, (0, 255, 255), (self.coo[0]-12, self.coo[1]-12, self.size[0]+24, self.size[1]+24))
        elif self.hoovered:
            pygame.draw.rect(screen, (0, 255, 100), (self.coo[0]-5, self.coo[1]-5, self.size[0]+10, self.size[1]+10))
        screen.blit(self.image, self.coo)


class Mazzo:
    def __init__(self, numero_mischiate=2):
        self.carte = [Carta(i, seme) for seme in ["Denara", "Coppe", "Spade", "Bastoni"] for i in range(1, 11)]
        self.mischia(numero_mischiate)

    def mostra_mazzo(self):
        [print(f"Seme: {carta.seme} | Numero: {carta.numero}") for carta in self.carte]

    """def mostra_carta_a_caso(self, screen, tipo, posizione):
        self.carte[random.randint(1, len(self.carte))].draw(screen, tipo, posizione)"""

    def prendi_carte(self, tipo):
        number_of_cards = 3 if tipo == "mano" else 4  # number of cards to remove from the deck
        carte = []
        for i in range(number_of_cards):
            carta = self.carte.pop(0)
            carta.carica_carta(tipo, i)
            carte.append(carta)
        return carte

    def mischia(self, quantita):
        for _ in range(quantita):
            random.shuffle(self.carte)


class Giocatore:
    def __init__(self, nome):
        self.punti_totale: int = 0
        self.punti_partita: int = 0
        self.nome: str = nome
        self.carte_in_mano: [Carta] = []
        self.carte_prese: [Carta] = []

    def conta_punti(self):
        pass


class GiocatoreAI(Giocatore):
    def __init__(self):
        super().__init__("R.F.J.8")
        image = pygame.image.load("assets/retro/1.png").convert_alpha()
        self.card_in_hand_image = pygame.transform.scale(image, SCALA_CARTA["hand-ai"])

    def draw(self, screen):
        if len(self.carte_in_mano) == 3:
            screen.blit(self.card_in_hand_image, (480, 150))
            screen.blit(self.card_in_hand_image, (510, 150))
            screen.blit(self.card_in_hand_image, (540, 150))
        elif len(self.carte_in_mano) == 2:
            screen.blit(self.card_in_hand_image, (495, 150))
            screen.blit(self.card_in_hand_image, (530, 150))
        elif len(self.carte_in_mano) == 1:
            screen.blit(self.card_in_hand_image, (512, 150))


class GiocatoreHumano(Giocatore):
    def __init__(self, nome):
        super().__init__(nome)

    def activate_cards_in_hand(self, mouse_pos):
        for carta in self.carte_in_mano:
            if carta.mouse_dentro(mouse_pos):
                carta.attiva = not carta.attiva  # reverts the state of the card to its opposite
                return carta.attiva

    def draw(self, screen):
        if not self.carte_prese:
            pygame.draw.rect(screen, (120, 74, 50), (930, 476, 135, 227))
        for i, carta in enumerate(self.carte_in_mano):
            carta.draw(screen)


