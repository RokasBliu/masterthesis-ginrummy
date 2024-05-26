from copy import deepcopy
import math
from keras.models import Sequential
from keras.layers import Dense, Lambda, Dropout, Flatten, LSTM, Conv2D, MaxPool2D
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import json

class NeuralNetBinary():
    def __init__(self):
        self.handSize = 8
        self.maxKnownCards = 10
        self.maxDiscardPile = 20
        self.turnNumber = 1
        self.score = 1
        self.bits = 38
        self.one_hot_bits = [0] * self.bits

        self.draw_value_mapping = {
            "random": 0,
            "discard": 1
        }

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

        self.suit_mapping = {
            "Hearts": 0,
            "Diamonds": 1,
            "Spades": 2,
            "Clubs": 3,
        }

        self.value_mapping = {
            "5": 0,
            "6": 1,
            "7": 2,
            "8": 3,
            "9": 4,
            "10": 5,
            "Jack": 6,
            "Queen": 7,
            "King": 8,
        }

    def build_neural_net(self, action="draw"):
        """Input dimentions:
        1. Hand size = 8
        2. Maximum amount of known cards = 10
        3. Maximum amount of cards in the discard pile = 20
        4. Turn number = 1
        5. Score = 1
        Total = 35"""

        model = Sequential()

        # Tried many different network structures here. LSTM provided best results.

        # model.add(Dense(1))
        # model.add(Dense(32, input_shape=(4, len(self.one_hot_bits)), activation='relu'))
        # model.add(Dense(16, activation='relu'))
        # model.add(Dense(8, activation='relu'))

        # model.add(Conv2D(32, (2, 2), activation='relu', input_shape=(4, 9, 4)))
        # model.add(Conv2D(64, (1, 1), activation='relu'))
        # model.add(Conv2D(64, (1, 1), activation='relu'))
        # model.add(Flatten())
        # model.add(Dense(64, activation='relu'))

        if action == "draw":
            model.add(LSTM(32, input_shape=(4, len(self.one_hot_bits)), return_sequences=True))
            model.add(LSTM(16, return_sequences=True))
            model.add(LSTM(8))
            model.add(Dense(2, activation='sigmoid'))
        else:
            model.add(LSTM(128, input_shape=(4, len(self.one_hot_bits)), return_sequences=True))
            model.add(LSTM(64, return_sequences=True))
            model.add(LSTM(32))
            # model.add(LSTM(16))
            # model.add(LSTM(8))
            model.add(Dense(8, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.summary()
        self.model = model
        
    def transform_data(self, data="draw-100K-both-values.csv"):
        #Read data from csv
        df = pd.read_csv(data)
        data_list = df.to_numpy()

        training_data = data_list[:, 1:-1]
        target_data = data_list[:, -1]

        #Hand cards
        hand_cards = training_data[:, 0]
        hand_cards_unchanged = []
        for i in range(len(hand_cards)):
            phantom_counter = 0
            hand_cards[i] = hand_cards[i][1:-1].split(", ")
            hand_cards_unchanged.append(hand_cards[i])
            hand_cards_one_hot = [0] * self.bits
            for j in range(len(hand_cards[i])):
                if hand_cards[i][j] == '':
                    continue
                if hand_cards[i][j] == "Phantom Card":
                    hand_cards_one_hot[self.card_to_value_mapping["Phantom Card"] + phantom_counter] = 1
                    phantom_counter += 1
                else:
                    hand_cards_one_hot[self.card_to_value_mapping[hand_cards[i][j]]] = 1
            hand_cards[i] = hand_cards_one_hot

        #Discard pile
        discard_pile = training_data[:, 1]
        
        for i in range(len(discard_pile)):
            discard_pile[i] = discard_pile[i][1:-1].split(", ")
            discard_pile_one_hot = [0] * self.bits
            for j in range(len(discard_pile[i])):
                if discard_pile[i][j] == '':
                    continue
                discard_pile_one_hot[self.card_to_value_mapping[discard_pile[i][j]]] = 1
            discard_pile[i] = discard_pile_one_hot

        #Top of discard pile
        top_of_discard_pile = training_data[:, 2]
        
        for i in range(len(top_of_discard_pile)):
            top_of_discard_pile_one_hot = [0] * self.bits
            if top_of_discard_pile[i] == top_of_discard_pile[i]:
                top_of_discard_pile_one_hot[self.card_to_value_mapping[top_of_discard_pile[i]]] = 1
            top_of_discard_pile[i] = top_of_discard_pile_one_hot

        #Known cards
        known_cards = training_data[:, 3]
        
        for i in range(len(known_cards)):
            if known_cards[i] is str:
                known_cards[i] = known_cards[i][1:-1].split(", ")
            known_cards_one_hot = [0] * self.bits
            for j in range(len(known_cards[i])):
                if known_cards[i][j] not in self.card_to_value_mapping:
                    continue
                known_cards_one_hot[self.card_to_value_mapping[known_cards[i][j]]] = 1
            known_cards[i] = known_cards_one_hot

        training_data = []
        for i in range(len(hand_cards)):
            data_to_append = [hand_cards[i]] + [discard_pile[i]] + [top_of_discard_pile[i]] + [known_cards[i]]
            training_data.append(data_to_append)

        converted_target_data = []
        for i, prediction in enumerate(target_data):
            if prediction == "random":
                converted_target_data.append([0, 1])
            elif prediction == "discard":
                converted_target_data.append([1, 0])
            else:
                predicted_index = prediction - 1
                #predicted_card = hand_cards_unchanged[i][predicted_index]
                n = len(hand_cards_unchanged[i])
                sorted_hand = [0] * n
                for j in range(n):
                    for k in range(0, n - j - 1):
                        if self.card_to_value_mapping[hand_cards_unchanged[i][k]] > self.card_to_value_mapping[hand_cards_unchanged[i][k + 1]]:
                            if predicted_index == k:
                                predicted_index = k + 1
                            elif predicted_index == k + 1:
                                predicted_index = k
                            sorted_hand[k], sorted_hand[k + 1] = sorted_hand[k + 1], sorted_hand[k]
                        else:
                            sorted_hand[k], sorted_hand[k + 1] = sorted_hand[k], sorted_hand[k + 1]
                onehot_target_data = [0] * 8
                onehot_target_data[predicted_index] = 1
                converted_target_data.append(onehot_target_data)
        x_train, x_test, y_train, y_test = train_test_split(training_data, converted_target_data, test_size=0.2, random_state=42)
        return x_train, x_test, y_train, y_test

def main():
    nn = NeuralNetBinary()
    nn.build_neural_net(action="draw")
    x_train, x_test, y_train, y_test = nn.transform_data()
    print(np.shape(np.array(x_train)))
    nn.model.fit(x_train, y_train, epochs=20, batch_size=100, validation_data=(x_test, y_test), verbose=1)
    loss, acc = nn.model.evaluate(x_test, y_test)
    print("Accuracy: ", acc)
    print("Loss: ", loss)
    predictions = nn.model.predict(x_test)
    for i in range(10):
        print("Prediction: ", predictions[i], "Actual: ", y_test[i])

    nn.model.save("draw_binary_model.h5")
main()


    # def transform_data_draw(self, data="draw-100K-both-values.csv"):
    #     #Read data from csv
    #     df = pd.read_csv(data)
    #     data_list = df.to_numpy()

    #     training_data = data_list[:, 1:-1]
    #     target_data = data_list[:, -1]

    #     #Embedding and converting data to numbers

    #     # Split data
    #     hand_cards = training_data[:, 0]
    #     discard_pile = training_data[:, 1]
    #     top_of_discard_pile = training_data[:, 2]
    #     known_cards = training_data[:, 3]

    #     training_data = []
    #     for i in range(len(hand_cards)):
    #         card_embed = [[0] * 4] * 9

    #         hand_cards[i] = hand_cards[i][1:-1].split(", ")
    #         discard_pile[i] = discard_pile[i][1:-1].split(", ")
    #         if known_cards[i] is str:
    #             known_cards[i] = known_cards[i][1:-1].split(", ")

    #         for j in range(len(known_cards[i])):
    #             if known_cards[i][j] not in self.card_to_value_mapping:
    #                 continue
    #             card = known_cards[i][j].split(" of ")
    #             card_embed[self.value_mapping[card[0]]][self.suit_mapping[card[1]]] = -2

    #         for j in range(len(hand_cards[i])):
    #             if hand_cards[i][j] == '' or hand_cards[i][j] == "Phantom Card":
    #                 continue
    #             card = hand_cards[i][j].split(" of ")
    #             card_embed[self.value_mapping[card[0]]][self.suit_mapping[card[1]]] = 1
            
    #         for j in range(len(discard_pile[i])):
    #             if discard_pile[i][j] == '' or discard_pile[i][j] == "Phantom Card":
    #                 continue
    #             if top_of_discard_pile[i] == '' or top_of_discard_pile[i] == "Phantom Card":
    #                 continue
    #             card = discard_pile[i][j].split(" of ")
    #             top_card = top_of_discard_pile[i].split(" of ")
    #             card_embed[self.value_mapping[card[0]]][self.suit_mapping[card[1]]] = -1
    #             card_embed[self.value_mapping[top_card[0]]][self.suit_mapping[top_card[1]]] = 2

    #         training_data.append(card_embed)

    #     converted_target_data = []
    #     for prediction in target_data:
    #         if prediction == "random":
    #             converted_target_data.append([0, 1])
    #         elif prediction == "discard":
    #             converted_target_data.append([1, 0])
    #         else:
    #             converted_target_data.append(self.card_to_value_mapping[prediction])
    #     x_train, x_test, y_train, y_test = train_test_split(training_data, converted_target_data, test_size=0.2, random_state=42)
    #     return x_train, x_test, y_train, y_test

    # def transform_data_draw2(self, data="discard-100K-both-values.csv"):
    #     #Read data from csv
    #     df = pd.read_csv(data)
    #     data_list = df.to_numpy()

    #     training_data = data_list[:, 1:-1]
    #     target_data = data_list[:, -1]

    #     # Split data
    #     hand_cards = training_data[:, 0]
    #     discard_pile = training_data[:, 1]
    #     top_of_discard_pile = training_data[:, 2]
    #     known_cards = training_data[:, 3]

    #     #Hand cards
    #     for i in range(len(hand_cards)):
    #         card_embed = [[0] * 4] * 9
    #         hand_cards[i] = hand_cards[i][1:-1].split(", ")
    #         for j in range(len(hand_cards[i])):
    #             if hand_cards[i][j] == '' or hand_cards[i][j] == "Phantom Card":
    #                 continue
    #             card = hand_cards[i][j].split(" of ")
    #             card_embed[self.value_mapping[card[0]]][self.suit_mapping[card[1]]] = 1
    #         hand_cards[i] = card_embed

    #     #Discard pile
    #     for i in range(len(discard_pile)):
    #         card_embed = [[0] * 4] * 9
    #         discard_pile[i] = discard_pile[i][1:-1].split(", ")
    #         for j in range(len(discard_pile[i])):
    #             if discard_pile[i][j] == '' or discard_pile[i][j] == "Phantom Card":
    #                 continue
    #             card = discard_pile[i][j].split(" of ")
    #             card_embed[self.value_mapping[card[0]]][self.suit_mapping[card[1]]] = 1
    #         discard_pile[i] = card_embed

    #     #Top of discard pile
    #     for i in range(len(top_of_discard_pile)):
    #         card_embed = [[0] * 4] * 9
    #         if top_of_discard_pile[i] == '' or top_of_discard_pile[i] == "Phantom Card":
    #             top_of_discard_pile[i] = card_embed
    #             continue
    #         top_card = top_of_discard_pile[i].split(" of ")
    #         card_embed[self.value_mapping[top_card[0]]][self.suit_mapping[top_card[1]]] = 1
    #         top_of_discard_pile[i] = card_embed

    #     #Known cards
    #     for i in range(len(known_cards)):
    #         if known_cards[i] is str:
    #             known_cards[i] = known_cards[i][1:-1].split(", ")
    #         card_embed = [[0] * 4] * 9
    #         for j in range(len(known_cards[i])):
    #             if known_cards[i][j] not in self.card_to_value_mapping:
    #                 continue
    #             card = known_cards[i][j].split(" of ")
    #             card_embed[self.value_mapping[card[0]]][self.suit_mapping[card[1]]] = -2
    #         known_cards[i] = card_embed

    #     training_data = []
    #     for i in range(len(hand_cards)):
    #         data_to_append = []
    #         data_to_append.append(hand_cards[i])
    #         #data_to_append.append(discard_pile[i])
    #         data_to_append.append(top_of_discard_pile[i])
    #         #data_to_append.append(known_cards[i])
    #         training_data.append(data_to_append)

    #     converted_target_data = []
    #     for prediction in target_data:
    #         if prediction == "random":
    #             converted_target_data.append([0, 1])
    #         elif prediction == "discard":
    #             converted_target_data.append([1, 0])
    #         else:
    #             converted_target_data.append(self.card_to_value_mapping[prediction])
    #     x_train, x_test, y_train, y_test = train_test_split(training_data, converted_target_data, test_size=0.2, random_state=42)
    #     return x_train, x_test, y_train, y_test