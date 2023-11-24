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
            # Standard deck creation
            self.cards = [Card(value, suit) for value in range(1, 11) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.caravans = [[], [], []]
        self.directions = [None, None, None]  # Direction for each caravan


    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)

    def refill_hand(self, hand_size=5):
        while len(self.hand) < hand_size and self.deck.cards:
            self.draw_card(self.deck)

    def play_card(self, card_index, caravan_index):
        if 0 <= card_index < len(self.hand) and 0 <= caravan_index < 3:
            card = self.hand[card_index]
            caravan = self.caravans[caravan_index]

            if self.can_play(card, caravan_index):
                self.hand.pop(card_index)
                caravan.append(card)
                if card.special:
                    self.apply_special_effect(card, caravan_index)
                return True
        return False

    def can_play(self, card, caravan_index):
        caravan = self.caravans[caravan_index]  # Access the correct caravan using the index
        direction = self.directions[caravan_index]

        if not caravan:
            return True  # Any card can start a caravan

        last_card = caravan[-1]
        if card.special:
            return True  # Special cards can be played anytime

        if len(caravan) == 1 and not card.special:
            # Set direction based on the second card
            self.directions[caravan_index] = "up" if card.value > last_card.value else "down"
            return True

        if direction and not card.special and card.suit != last_card.suit:
            if direction == "up" and card.value <= last_card.value:
                return False
            if direction == "down" and card.value >= last_card.value:
                return False

        return True

    def get_direction(self, caravan):
        if len(caravan) < 2:
            return None
        first_card = caravan[0]
        second_card = caravan[1]
        return "up" if second_card.value > first_card.value else "down"

    def apply_special_effect(self, card, caravan_index):
        caravan = self.caravans[caravan_index]
        # Special effects logic (to be implemented)
        pass

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
        # Custom deck creation (for simplicity, using standard decks here)
        deck1 = Deck(custom_cards=[Card(value, suit) for value in range(1, 11) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]] * 3)
        deck2 = Deck(custom_cards=[Card(value, suit) for value in range(1, 11) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]] * 3)

        self.players = [Player("Player 1", deck1), Player("Player 2", deck2)]
        self.current_player = 0

    def start(self):
        # Initial hand refill
        for player in self.players:
            player.refill_hand()

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def current_player_turn(self):
        player = self.players[self.current_player]
        player.refill_hand()
        print(f"\n{player.name}'s turn. Hand: {player.show_hand()}")

        # Display the status of each caravan
        for i, caravan in enumerate(player.caravans):
            caravan_value = sum(card.value for card in caravan if not card.special)
            direction = player.directions[i]
            print(f"Caravan {i+1}: Value = {caravan_value}, Direction = {direction if direction else 'Not set'}")

        try:
            card_index = int(input("Choose a card to play (index): "))
            caravan_index = int(input("Choose a caravan to place the card (0-2): "))

            if player.play_card(card_index, caravan_index):
                print(f"Played {player.caravans[caravan_index][-1]} on caravan {caravan_index}")
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
