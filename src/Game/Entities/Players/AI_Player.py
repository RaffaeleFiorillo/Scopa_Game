from src.Game.Entities.Players.Player import Player
from src.AI import RandomBehaviour
from src.Animations.AI_Player import *
import threading


class AI(Player):
    def __init__(self):
        super().__init__("R.F.J.8")
        self.selected_card = None
        
        idle_animation = IdleAnimation()
        animations = {"waiting": idle_animation,
                      "choice": ChoiceAnimation(),
                      "take": TakeAnimation(),
                      "throw": ThrowAnimation()}
        self.animations: {str, PlayerAnimation} = animations
        
        self.state = "waiting"  # the player is waiting for his turn to play
        self.is_ready_to_make_a_move = False
        self.AI = RandomBehaviour()
        self.thinking_thread: threading.Thread = threading.Thread(target=self.AI.choose_the_move)

    def end_turn(self):
        super(AI, self).end_turn()
        self.is_ready_to_make_a_move = False
        
    def set_up_for_thinking(self, table_cards):
        self.AI.table_cards = table_cards
        self.state = "start"
        self.thinking_thread: threading.Thread = threading.Thread(target=self.AI.choose_the_move)

    def start_choosing_process(self):
        self.AI.hand_cards = self.cards_in_hand
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
        self.animations[self.state].draw(screen)
