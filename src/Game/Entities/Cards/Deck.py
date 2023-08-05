from src.Game.Entities.Cards.Card import Card
from random import shuffle


class Deck:
	def __init__(self, number_shuffled=2):
		self.cards = [Card(i, seme) for seme in ["Denara", "Coppe", "Spade", "Bastoni"] for i in range(1, 11)]
		self.shuffle(number_shuffled)

	def show_deck(self):
		[print(f"Seme: {card.seme} | number: {card.number}") for card in self.cards]

	"""def show_random_card(self, screen, tipo, posizione):
		self.cards[random.randint(1, len(self.cards))].draw(screen, tipo, posizione)"""

	# draw in the sense of taking and not drawing
	def draw_cards(self, card_location):  # card location refers to where the card is going (hand, table, ...)
		number_of_cards = 3 if card_location == "mano" else 4  # number of cards to remove from the deck
		cards = []
		for i in range(number_of_cards):
			card = self.cards.pop(0)
			card.load_card(card_location, i)
			cards.append(card)
		return cards

	def shuffle(self, times):
		for _ in range(times):
			shuffle(self.cards)
