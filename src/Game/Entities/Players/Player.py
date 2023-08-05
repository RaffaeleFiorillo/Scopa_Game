from src.Game.Entities.Cards.Card import Card


class Player:
    def __init__(self, nome):
        self.total_score: int = 0
        self.match_score: int = 0
        self.nome: str = nome
        self.cards_in_hand: [Card] = []
        self.cards_taken: [Card] = []

    def count_score(self):
        pass
