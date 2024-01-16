import copy
from Gin_rummy import Gin_rummy
from Player import Player
from Hand import Hand
from Deck import Deck, Card
class StateManager():
    def __init__(self, game_state, state, known_cards = [], depth = 0):
        self.game_state = copy.deepcopy(game_state)

        self.children = []
        self.depth = depth

        self.states = ["draw", "discard", "knock"]
        self.current_state = state
        self.round_number = self.game_state.round_number
        self.GIN_POINTS = self.game_state.GIN_POINTS
        self.UNDERCUT_POINTS = self.game_state.UNDERCUT_POINTS
        self.WINNING_SCORE = self.game_state.WINNING_SCORE

        self.players = self.game_state.players
        self.current_player = self.game_state.players[self.game_state.turn_index]

        if self.current_player.hand.deadwood == 0:
            self.current_deadwood = self.current_player.hand.get_hand_score()
        else:
            self.current_deadwood = self.current_player.hand.deadwood
        
        self.score = self.current_player.score

        other_player = self.game_state.players[self.game_state.turn_index + 1 % 2]
        self.other_player_score = other_player.score

        self.hand = self.current_player.hand

        self.turn_index = self.game_state.turn_index
        self.player_turns = ["current_player", "other_player"]
        self.player_turn = self.player_turns[self.turn_index]

        self.discard_pile = self.game_state.discard_pile
        self.top_card_discard_pile = self.discard_pile[-1]

        self.known_cards = known_cards # TODO add the known cards from the other player's hand, that are known to the current player
    
    def change_player_hands(self, hand):
        self.game_state.players[self.game_state.turn_index].hand = hand
        self.hand = hand
    
    def draw_from_discard_pile(self):
        self.hand.add(self.top_card_discard_pile)
        self.discard_pile.pop()

    def discard_from_hand(self, card):
        self.hand.cards.remove(card)
        self.game_state.players[self.game_state.turn_index].hand.cards.remove(card)
        self.discard_pile.append(card)
        self.game_state.discard_pile.append(card)

    def print_state(self):
        print("--------------------")
        print("State: ", self.current_state)
        print("Current player: ", self.current_player.name)
        print("Current player's hand: ", self.hand)
        print("Current player's deadwood: ", self.current_deadwood)
        print("Round number: ", self.round_number)
        print("Depth: ", self.depth)
        print("Player turn: ", self.player_turn)
        
        return

    def create_children_tree(self, state, depth):
        if depth == 0:
            return
        else:
            state.create_children()
            for c in state.children:
                c.create_children_tree(c, depth - 1)

    def create_children(self):
        if self.player_turn == "current_player":
            if self.current_state == "draw":

                child = StateManager(self.game_state, "discard", self.known_cards)

                child.game_state = self
                child.depth += 1
                child.current_state = "discard"
                child.hand.add(child.top_card_discard_pile)
                child.discard_pile.pop()
                child.current_deadwood = child.hand.get_hand_score()
                self.children.append(child)
                child.print_state()

                deck = Deck()
                deck.make_smaller_deck()

                #Remove cards from deck that are in the current player's hand
                for c in self.hand.cards:
                    deck.remove(c)
                
                for c in self.known_cards:
                    deck.remove(c)
                
                for c in self.discard_pile:
                    deck.remove(c)

                for c in deck:
                    child = StateManager(self.game_state, "discard", self.known_cards, self.depth + 1)
                    child.hand.add(c)
                    child.current_deadwood = child.hand.get_hand_score()
                    child.print_state()
                    self.children.append(child)
            
            elif self.current_state == "discard":

                for i in range(len(self.hand.cards)):
                    print("i: ", i)
                    child = StateManager(self.game_state, "draw", self.known_cards, self.depth + 1)
                    print("hand length child: ", len(child.hand.cards))
                    child.discard_pile.append(child.hand.cards[i])
                    child.hand.cards.remove(child.hand.cards[i])
                    child.current_deadwood = child.hand.get_hand_score()

                    if child.current_deadwood <= 10:
                        child.current_state = "knock"
                    
                    self.turn_index = (self.turn_index + 1) % 2
                    if self.turn_index == 0:
                        self.round_number += 1

                    if self.player_turn == "current_player":
                        self.player_turn = "other_player"
                    else:
                        self.player_turn = "current_player"

                    child.print_state()
                    self.children.append(child)
            
        else: #Other player's turn
            if self.current_state == "draw":
                child = StateManager(self.game_state, "discard", self.known_cards, self.depth + 1)
                child.depth += 1
                child.known_cards.append(child.discard_pile.pop())
                child.known_cards.append(child.top_card_discard_pile)





def main():
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    game = Gin_rummy(player1, player2)
    game.start_new_game()
    start_state = StateManager(game, "draw")
    start_state.create_children_tree(start_state, 2)
        
if __name__ == "__main__":
        main()