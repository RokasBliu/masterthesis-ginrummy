from keras.models import Sequential
from keras.layers import Dense, Lambda, Dropout, Flatten, LSTM
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import json

class NeuralNetManager():
    def __init__(self):
        self.handSize = 8
        self.maxKnownCards = 10
        self.maxDiscardPile = 20
        self.turnNumber = 1
        self.score = 1
        self.bits = 38
        self.one_hot_bits = [0] * self.bits

        self.card_to_value_mapping = {
            "5 of Hearts": 0,
            "5 of Diamonds": 1,
            "5 of Clubs": 2,
            "5 of Spades": 3,
            "6 of Hearts": 4,
            "6 of Diamonds": 5,
            "6 of Clubs": 6,
            "6 of Spades": 7,
            "7 of Hearts": 8,
            "7 of Diamonds": 9,
            "7 of Clubs": 10,
            "7 of Spades": 11,
            "8 of Hearts": 12,
            "8 of Diamonds": 13,
            "8 of Clubs": 14,
            "8 of Spades": 15,
            "9 of Hearts": 16,
            "9 of Diamonds": 17,
            "9 of Clubs": 18,
            "9 of Spades": 19,
            "10 of Hearts": 20,
            "10 of Diamonds": 21,
            "10 of Clubs": 22,
            "10 of Spades": 23,
            "Jack of Hearts": 24,
            "Jack of Diamonds": 25,
            "Jack of Clubs": 26,
            "Jack of Spades": 27,
            "Queen of Hearts": 28,
            "Queen of Diamonds": 29,
            "Queen of Clubs": 30,
            "Queen of Spades": 31,
            "King of Hearts": 32,
            "King of Diamonds": 33,
            "King of Clubs": 34,
            "King of Spades": 35,
            "Phantom Card": 36,
        }

    def build_neural_net(self):
        """Input dimentions:
        1. Hand size = 8
        2. Maximum amount of known cards = 10
        3. Maximum amount of cards in the discard pile = 20
        4. Turn number = 1
        5. Score = 1
        Total = 35"""

        model = Sequential()

        # model.add(LSTM(64, input_shape=(3, self.bits), return_sequences=True))
        # model.add(LSTM(32, return_sequences=True))
        # model.add(LSTM(8))
        # model.add(Dense(1))
        model.add(Dense(256, activation='relu', input_shape=(4, self.bits)))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(16, activation='relu'))
        model.add(Flatten())
        model.add(Dense(1, activation='linear'))

        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
        model.summary()
        self.model = model
        
    def transform_data(self, data="test-data-draw-3.csv"):
        #Read data from csv
        df = pd.read_csv(data)
        data_list = df.to_numpy()

        training_data = data_list[:, 1:-1]
        target_data = data_list[:, -1]

        #Embedding and converting data to numbers

        #Hand cards
        hand_cards = training_data[:, 0]
        for i in range(len(hand_cards)):
            phantom_counter = 0
            hand_cards[i] = hand_cards[i][1:-1].split(", ")
            hand_cards_one_hot = [0] * self.bits
            # if len(hand_cards[i]) < self.handSize:
            #     hand_cards[i].extend(["0"] * (self.handSize - len(hand_cards[i])))
            for j in range(len(hand_cards[i])):
                if hand_cards[i][j] == '':
                    continue
                if hand_cards[i][j] == "Phantom Card":
                    #hand_cards[i][j] = self.card_to_value_mapping["Phantom Card"] + phantom_counter
                    hand_cards_one_hot[self.card_to_value_mapping["Phantom Card"] + phantom_counter] = 1
                    phantom_counter += 1
                else:
                    hand_cards_one_hot[self.card_to_value_mapping[hand_cards[i][j]]] = 1
                    #hand_cards[i][j] = self.card_to_value_mapping[hand_cards[i][j]]  
            hand_cards[i] = hand_cards_one_hot
        
        #Hot one encoding of hand cards
        # for i in range(len(hand_cards)):
        #     hand_cards_one_hot = [0] * 40
        #     for j in range(len(hand_cards[i])):
        #         if hand_cards[i][j] < 0:
        #             continue
        #         hand_cards_one_hot[hand_cards[i][j]] = 1
        #     hand_cards[i] = hand_cards_one_hot

        #print("Hand cards after one hot encoding:", hand_cards)

        #Known cards
        known_cards = training_data[:, 1]

        for i in range(len(known_cards)):
            known_cards[i] = known_cards[i][1:-1].split(", ")
            known_cards_one_hot = [0] * self.bits
            # if len(known_cards[i]) < self.maxKnownCards:
            #     known_cards[i].extend(["0"] * (self.maxKnownCards - len(known_cards[i])))
            for j in range(len(known_cards[i])):
                if known_cards[i][j] == '':
                    continue
                # known_cards[i][j] = self.card_to_value_mapping[known_cards[i][j]]
                known_cards_one_hot[self.card_to_value_mapping[known_cards[i][j]]] = 1
            known_cards[i] = known_cards_one_hot

        # for i in range(len(known_cards)):
        #     known_cards_one_hot = [0] * 40
        #     for j in range(len(known_cards[i])):
        #         if known_cards[i][j] < 0:
        #             continue
        #         known_cards_one_hot[known_cards[i][j]] = 1
        #     known_cards[i] = known_cards_one_hot

        #print("Known cards after embedding:", known_cards)

        discard_pile = training_data[:, 2]

        for i in range(len(discard_pile)):
            discard_pile[i] = discard_pile[i][1:-1].split(", ")
            discard_pile_one_hot = [0] * self.bits
            # if len(discard_pile[i]) < self.maxDiscardPile:
            #     discard_pile[i].extend(["0"] * (self.maxDiscardPile - len(discard_pile[i])))
            for j in range(len(discard_pile[i])):
                if discard_pile[i][j] == '':
                    continue
                # discard_pile[i][j] = self.card_to_value_mapping[discard_pile[i][j]]
                discard_pile_one_hot[self.card_to_value_mapping[discard_pile[i][j]]] = 1
            discard_pile[i] = discard_pile_one_hot
        
        # for i in range(len(discard_pile)):
        #     discard_pile_one_hot = [0] * 40
        #     for j in range(len(discard_pile[i])):
        #         if discard_pile[i][j] < 0:
        #             continue
        #         discard_pile_one_hot[discard_pile[i][j]] = 1
        #     discard_pile[i] = discard_pile_one_hot

        # cards_left_in_deck = [[0 for i in range(40)] for j in range(len(discard_pile))]

        # for i in range(len(discard_pile)):
        #     cards_left_in_deck[i] = [0]*40
        #     for j in range(len(discard_pile[i])):
        #         if discard_pile[i][j] == 0 and hand_cards[i][j] == 0 and known_cards[i][j] == 0:
        #             cards_left_in_deck[i][j] = 1

        turn_number = training_data[:, -2]
        for i in range(len(turn_number)):
            turn_number_one_hot = [0] * self.bits
            for j in range(turn_number[i]):
                if j > self.bits:
                    break
                turn_number_one_hot[j] = 1
            turn_number[i] = turn_number_one_hot

        training_data = []
        for i in range(len(hand_cards)):
            data_to_append = [hand_cards[i]] + [known_cards[i]] + [discard_pile[i]] + [turn_number[i]] #+ [cards_left_in_deck[i]]
            training_data.append(data_to_append)

        draw_phase_training_data = training_data[:int(len(training_data)/2)]
        discard_phase_training_data = training_data[int(len(training_data)/2):]
        #print("Discard pile after embedding:", discard_pile)
        #print("Training data after embedding:", training_data)

        #Split data into training and testing
        #target_data = target_data.reshape(-1, 1)
        target_data = target_data.tolist()
        #print("Target data:", target_data)
        x_train, x_test, y_train, y_test = train_test_split(training_data, target_data, test_size=0.2, random_state=42)
        return x_train, x_test, y_train, y_test

def main():
    nn = NeuralNetManager()
    nn.build_neural_net()
    x_train, x_test, y_train, y_test = nn.transform_data()
    nn.model.fit(x_train, y_train, epochs=100, batch_size=128, validation_data=(x_test, y_test), verbose=1)
    loss, mse = nn.model.evaluate(x_test, y_test)
    print("Mean squared error: ", mse)
    print("Loss: ", loss)
    predictions = nn.model.predict(x_test)
    for i in range(10):
        print("Prediction: ", predictions[i], "Actual: ", y_test[i])

main()
