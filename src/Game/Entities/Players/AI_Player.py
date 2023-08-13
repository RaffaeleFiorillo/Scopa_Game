from src.Game.Entities.Players.Player import Player
from src.Animations.AI_Player import *


class AI(Player):
    def __init__(self):
        super().__init__("R.F.J.8")
        self.animations: {str, PlayerAnimation} = {"waiting": IdleAnimation(),
                                                   "choice": ChoiceAnimation(),
                                                   "take": TakeAnimation(),
                                                   "throw": ThrowAnimation()}
        self.state = "waiting"  # the player is waiting for his turn to play

    def update(self, dt):
        if self.state == "start":  # starts the process of making a move
            self.state = "choice"
            # self.start_move_choice_process()  # start the thinking thread
        self.animations[self.state].update(dt, self.cards_in_hand)
    
    def draw(self, screen):
        self.animations[self.state].draw(screen)
