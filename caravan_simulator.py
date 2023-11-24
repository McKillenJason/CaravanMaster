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

class AIPlayer(Player):
    def __init__(self, name, deck):
        super().__init__(name, deck)

    def evaluate_game_state(self):
        my_caravan_values = [sum(card.value for card in caravan if not card.special) for caravan in self.caravans]
        opponent_caravan_values = [sum(card.value for card in caravan if not card.special) for caravan in self.game.players[1 - self.game.current_player].caravans]

        # Additional assessments could include:
        # - Which caravans are closest to winning.
        # - The potential impact of special cards.
        # - The suit and value distribution in hand.

        return {
            "my_caravans": my_caravan_values, 
            "opponent_caravans": opponent_caravan_values,
            # Include other assessments here
        }


    def choose_card_to_play(self):
        game_state = self.evaluate_game_state()

        # Implement a basic strategy:
        # - Prioritize playing on caravans that are closest to the winning range.
        # - Use special cards to disrupt the opponent's progress or boost own caravans.
        # - This is a placeholder for more advanced logic.

        card_index = random.choice(range(len(self.hand)))
        caravan_index = random.choice(range(3))
        play_on_opponent = random.choice([True, False])
        
        # Replace the above logic with more advanced decision-making.
        
        return card_index, caravan_index, play_on_opponent

    def play_turn(self):
        card_index, caravan_index, play_on_opponent = self.choose_card_to_play()
        opponent = None if not play_on_opponent else self.game.players[1 - self.game.current_player]
        self.play_card(card_index, caravan_index, opponent)

        



class Game:
    def __init__(self, ai_opponent=False):
        deck1 = Deck(custom_cards=[Card(value, suit) for value in range(1, 14) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]] * 3)
        deck2 = Deck(custom_cards=[Card(value, suit) for value in range(1, 14) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]] * 3)

        self.players = [Player("Player 1", deck1), Player("Player 2", deck2)]
        self.current_player = 0

        if ai_opponent:
            self.players[1] = AIPlayer("AI Opponent", deck2)
            self.players[1].game = self  # Provide the AI access to the game object

        self.start()

    def start(self):
        for player in self.players:
            player.refill_hand()

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def display_caravans(self, player, player_number):
        print(f"\n{player.name}'s Caravans:")
        for i, caravan in enumerate(player.caravans):
            caravan_value = sum(card.value for card in caravan if not card.special)
            direction = player.directions[i]
            print(f"  Caravan {player_number}-{i+1}: Value = {caravan_value}, Direction = {direction if direction else 'Not set'}")

    def current_player_turn(self):
        player = self.players[self.current_player]
        opponent = self.players[1 - self.current_player]

        player.refill_hand()

        # Display the player's hand (for human players)
        if not isinstance(player, AIPlayer):
            print(f"\n{player.name}'s turn. Hand: {player.show_hand()}")

        # Display all caravans
        self.display_caravans(player, 1)
        self.display_caravans(opponent, 2)

        if isinstance(player, AIPlayer):
            print("\nAI Opponent's turn.")
            successful_move = player.play_turn()
        else:
            try:
                card_index = int(input("Choose a card to play (index): "))
                caravan_index = int(input("Choose a caravan to place the card (1-3): "))
                play_on_opponent = input("Play on opponent's caravan? (yes/no): ").lower() == 'yes'

                # Validate indices and card playability
                if card_index < 0 or card_index >= len(player.hand) or caravan_index < 1 or caravan_index >= 4:
                    print("Invalid move: Index out of range. Please try again.")
                    return False

                target_player = opponent if play_on_opponent else player
                successful_move = player.play_card(card_index, caravan_index, target_player)

                if successful_move:
                    # Print the last move made
                    print(f"Played {player.hand[card_index]} on {'opponent' if play_on_opponent else 'own'} caravan {caravan_index + 1}")
                else:
                    # Print why the move is invalid
                    print("Invalid move: Cannot play the selected card in the chosen caravan. Please try again.")
            except ValueError:
                print("Invalid input: Please enter a valid number.")
                successful_move = False

        return successful_move

    def check_winner(self):
        for player in self.players:
            scores = player.calculate_caravan_scores()
            winning_caravans = sum(21 <= score <= 26 for score in scores)
            if winning_caravans >= 2:
                return player.name
        return None

    def play(self):
        while True:
            self.current_player_turn()
            winner = self.check_winner()
            if winner:
                print(f"{winner} wins the game!")
                break
            self.switch_player()

if __name__ == "__main__":
    game = Game(ai_opponent=True)
    game.play()


