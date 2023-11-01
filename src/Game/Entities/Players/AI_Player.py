from src.Game.Entities.Players.Player import Player
from src.Game.Entities.Cards.TableCards import TableCards
from src.AI import RandomBehaviour
from src.Animations.AI_Player import *
import threading


class AI(Player):
    def __init__(self, table_cards: TableCards):
        super().__init__("R.F.J.8", 230)
        
        animations = {"waiting": IdleAnimation(),
                      "choice": ChoiceAnimation(),
                      "take": TakeAnimation(),
                      "throw": ThrowAnimation()}
        self.animations: {str, PlayerAnimation} = animations
        
        self.state = "waiting"  # the player is waiting for his turn to play
        self.is_ready_to_make_a_move = False
        self.AI = RandomBehaviour(table_cards)
        self.thinking_thread: threading.Thread = threading.Thread(target=self.AI.choose_the_move)
    
    def take_cards_from_deck(self, cards):
        super(AI, self).take_cards_from_deck(cards)
        self.AI.cards_in_hand = cards
        
    def end_turn(self):
        super(AI, self).end_turn()
        self.is_ready_to_make_a_move = False
        
    def set_up_for_thinking(self):
        self.state = "start"
        self.thinking_thread: threading.Thread = threading.Thread(target=self.AI.choose_the_move)

    def start_choosing_process(self):
        self.thinking_thread.start()

    def update(self, dt):
        # print(f"Has chosen: {self.AI.has_chosen}")
        if self.state == "start":  # starts the process of making a move
            self.state = "choice"
            self.start_choosing_process()  # start the thinking thread
        elif self.AI.has_chosen and self.state == "choice":
            self.state = self.AI.move_type
        elif self.animations[self.state].has_ended and self.state in ("take", "throw"):
            self.selected_card = self.cards_in_hand[self.AI.chosen_hand_card_index]
            self.selected_card.active = True
            self.is_ready_to_make_a_move = True
            
        self.animations[self.state].update(dt, self.cards_in_hand)
    
    def draw(self, screen):
        super(AI, self).draw(screen)
        self.animations[self.state].draw(screen)
