import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.special = value > 10  # True for face cards
        self.special_type = None
        if self.special:
            self.special_type = {11: 'Jack', 12: 'Queen', 13: 'King'}[value]

    def __repr__(self):
        if self.special:
            return f"{self.special_type} of {self.suit}"
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self, custom_cards=None):
        if custom_cards:
            self.cards = custom_cards
        else:
            # Ensure face cards (Jacks, Queens, Kings) are included
            self.cards = [Card(value, suit) for value in range(1, 14) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def print_deck(self):
        for card in self.cards:
            print(card)


class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.caravans = [[], [], []]
        self.directions = [None, None, None]

    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)

    def refill_hand(self, hand_size=5):
        while len(self.hand) < hand_size and self.deck.cards:
            self.draw_card(self.deck)

    def play_card(self, card_index, caravan_index, opponent=None):
        if 0 <= card_index < len(self.hand) and 0 <= caravan_index < 3:
            card = self.hand[card_index]
            target_player = opponent if opponent else self

            if target_player.can_play(card, caravan_index):
                self.hand.pop(card_index)
                target_player.caravans[caravan_index].append(card)
                if card.special:
                    target_player.apply_special_effect(card, caravan_index)
                return True
        return False

    def can_play(self, card, caravan_index):
        caravan = self.caravans[caravan_index]
        direction = self.directions[caravan_index]

        if not caravan:
            return True  # Any card can start a caravan

        last_card = caravan[-1]
        if card.special:
            return True

        if len(caravan) == 1 and not card.special:
            self.directions[caravan_index] = "up" if card.value > last_card.value else "down"
            return True

        if direction and not card.special and card.suit != last_card.suit:
            if direction == "up" and card.value <= last_card.value:
                return False
            if direction == "down" and card.value >= last_card.value:
                return False

        return True

    def apply_special_effect(self, card, caravan_index):
        caravan = self.caravans[caravan_index]

        if card.special_type == 'Jack':
            # Remove the last card from the caravan (excluding the Jack itself)
            for i in range(len(caravan) - 2, -2, -2):
                if not caravan[i].special:
                    removed_card = caravan.pop(i)
                    print(f"Jack removed {removed_card} from caravan {caravan_index + 1}")
                    break
            
          
                

        elif card.special_type == 'Queen':
            # Reverse the direction of the caravan
            current_direction = self.directions[caravan_index]
            self.directions[caravan_index] = "down" if current_direction == "up" else "up"

        elif card.special_type == 'King':
            # Find the last non-special card to double
            for i in range(len(caravan) - 1, -1, -1):
                if not caravan[i].special:
                    caravan.append(Card(caravan[i].value, caravan[i].suit))
                    break

    def calculate_caravan_scores(self):
        scores = []
        for caravan in self.caravans:
            score = sum(card.value for card in caravan if not card.special)
            scores.append(score)
        return scores

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)


class Game:
    def __init__(self):
        # Ensure standard deck creation is used if custom deck is not provided
        deck1 = Deck() 
        deck2 = Deck()  

        self.players = [Player("Player 1", deck1), Player("Player 2", deck2)]
        self.current_player = 0

        # Debug: Print deck composition
        self.players[0].deck.print_deck()


    def start(self):
        for player in self.players:
            player.refill_hand()

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def current_player_turn(self):
        player = self.players[self.current_player]
        opponent = self.players[1 - self.current_player]

        player.refill_hand()
        print(f"\n{player.name}'s turn. Hand: {player.show_hand()}")

        for i, caravan in enumerate(player.caravans):
            caravan_value = sum(card.value for card in caravan if not card.special)
            direction = player.directions[i]
            print(f"Caravan {i+1}: Value = {caravan_value}, Direction = {direction if direction else 'Not set'}")

        try:
            card_index = int(input("Choose a card to play (index): "))
            caravan_index = int(input("Choose a caravan to place the card (0-2): "))
            play_on_opponent = input("Play on opponent's caravan? (yes/no): ").lower() == 'yes'

            target_player = opponent if play_on_opponent else player

            if player.play_card(card_index, caravan_index, target_player):
                print(f"Played {target_player.caravans[caravan_index][-1]} on caravan {caravan_index}")
                return True
            else:
                print("Invalid move. Please try again.")
                return False
        except ValueError:
            print("Invalid input. Please enter a number.")
            return False

    def check_winner(self):
        for player in self.players:
            scores = player.calculate_caravan_scores()
            winning_caravans = sum(21 <= score <= 26 for score in scores)
            if winning_caravans >= 2:
                return player.name
        return None

    def play(self):
        self.start()
        while True:
            valid_move = self.current_player_turn()
            if valid_move:
                winner = self.check_winner()
                if winner:
                    print(f"{winner} wins the game!")
                    break
                self.switch_player()

if __name__ == "__main__":
    game = Game()
    game.play()

