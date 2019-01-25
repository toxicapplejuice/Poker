import random

#trying to see if git works
#now see different branch

class Players(object):
    def __init__(self,amount,name):
        self.chips = amount
        self.hands = list_Cards()
        self.best_cards = list_Cards()
        self.folded = False
        self.winner = False
        self.aggressive = False
        self.name = name
        self.position = None
        self.hand_rank = None
        self.all_in = None

    def fold(self):
        self.folded = True
    def is_folded(self):
        return self.folded
    def is_winner(self):
        return self.winner
    def is_all_in(self):
        return self.all_in
    def bet(self):
        self.aggressive = True
    def give_position(self,other):
        self.position = other
    def is_aggressive(self):
        return self.aggressive
    def get_position(self):
        return self.position
    def __str__(self):
        return self.amount
    def get_chip_amount(self):
        return self.chips
    def add_chips(self,other):
        return self.chips + int(other)
    def subtract_chips(self,other):
        return self.chips - int(other)
class Card(object):
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        return str(self.rank) + str(self.suit)
    def __eq__ (self, other):
        return (self.rank == other.rank)
    def __ne__ (self, other):
        return (self.rank != other.rank)
    def __lt__ (self, other):
        return (self.rank < other.rank)
    def __le__ (self, other):
        return (self.rank <= other.rank)
    def __gt__ (self, other):
        return (self.rank > other.rank)
    def __ge__ (self, other):
        return (self.rank >= other.rank)
class list_Cards(object):
    def __init__(self):
        self.deck = []
    def add_card(self,card):
        return self.deck.append(card)
    def add_deck(self,other):
        for i in range(len(other)):
            self.deck.append(other.deck[i])
        return self.deck
    def sort_deck(self):
        return(self.deck.sort(key = lambda x: x.rank, reverse = True))
    def remove_card(self,card):
        return self.deck.remove(card)
    def __len__ (self):
        return len(self.deck)
    def __add__ (self, other):
        return self.deck + other.deck
    def __str__(self):
        deck_string = ""
        for i in range(len(self.deck)):
            deck_string += str(self.deck[i].rank) + self.deck[i].suit + " "
        return deck_string
class Deck(object):
    rank = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    suit = ["H","S","C","D"]
    def __init__(self):
        self.deck = []
        for i in Deck.rank:
            for j in Deck.suit:
                card = Card(i,j)
                self.deck.append(card)
    def shuffle_deck(self):
        random.shuffle(self.deck)
    def deal_deck(self):
        return self.deck.pop()
    def __str__(self):
        deck_string = ""
        for i in range(len(self.deck)):
            deck_string += str(self.deck[i].rank) + self.deck[i].suit + " "
        return deck_string
class Poker(object):
    def __init__(self, num_players,players_list):
        self.deck = Deck()
        self.num_players = num_players
        self.community_cards = list_Cards()
        self.winners = []
        self.num_current_players = num_players
        self.minimum_to_play = 50
        self.bets = {}
        self.players = players_list
        self.rankings = {}
        self.pot = 0

    def deal(self):
        self.deck.shuffle_deck()
        for i in range(len(self.players)):
            self.players[i].hand_rank = 0
            self.players[i].num_card_value = 0
        #deal cards
        for i in range(self.num_players):
            Dealt = list_Cards()
            Dealt.add_card(self.deck.deal_deck())
            Dealt.add_card(self.deck.deal_deck())
            self.players[i].hands = Dealt
        #making dealer first
        for player in self.players:
            self.bets[player.name] = 0
        # preflop
        self.action(self.players)
        # le flop
        for i in range (3):
            self.community_cards.add_card(self.deck.deal_deck())
        print("")
        print(self.community_cards)

        if self.num_players !=2:
            #skips this if i only have one player
            if self.num_current_players != 1:
                for i in range(len(self.players)):
                    if self.players[i].get_position() == "Small Blind":
                        self.players = self.players[i:] + self.players[:i]
                        break
                self.action(self.players)
        else:
            if self.num_current_players != 1:
                for i in range(len(self.players)):
                    if self.players[i].get_position() == "Big Blind":
                        self.players = self.players[i:] + self.players[:i]
                        break
                self.action(self.players)
        #le turn
        for i in range (1):
            self.community_cards.add_card(self.deck.deal_deck())
        print("")
        print(self.community_cards)
        #skips this if i only have one player
        if self.num_current_players != 1:
            self.action(self.players)
        #le turn
        for i in range (1):
            self.community_cards.add_card(self.deck.deal_deck())
        print("")
        print(self.community_cards)
        #skips this if i only have one player
        if self.num_current_players != 1:
            self.action(self.players)

        print("Community Cards")
        print(self.community_cards)
    #returns player object(s) who have the best hand at show down. Not all players goto showdown
    def Showdown(self):
        #adding community and sorting
        for i in range(self.num_players):
            best_cards = list_Cards()
            self.players[i].hands.add_deck(self.community_cards)
            self.players[i].hands.sort_deck()
        for i in range(self.num_players):
            print("Player", i+1 , "Cards: ")
            for j in range(len(self.players[i].hands)):
                print (self.players[i].hands.deck[j])
            print(" ")
        if self.num_current_players !=1:
            #Assigns a hand rank value (Royal Flush = 8, Straight = 4) to each player at showdown. Also
            #gives a highest num card value for comparision purposes. Gives player their five best cards
            for i in range(len(self.players)):
                if not self.players[i].is_folded():
                    if self.is_straight_flush(self.players[i].hands):
                        self.players[i].hand_rank = 8
                        self.players[i].best_cards = self.is_straight_flush(self.players[i].hands)
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_quads(self.players[i].hands):
                        self.players[i].hand_rank = 7
                        self.players[i].best_cards = self.is_quads(self.players[i].hands)
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[0])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[1])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[2])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[3])
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_full_house(self.players[i].hands):
                        self.players[i].hand_rank = 6
                        self.players[i].best_cards = self.is_full_house(self.players[i].hands)
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_flush(self.players[i].hands):
                        self.players[i].hand_rank = 5
                        self.players[i].best_cards = self.is_flush(self.players[i].hands)
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_straight(self.players[i].hands):
                        self.players[i].hand_rank = 4
                        self.players[i].best_cards = self.is_straight(self.players[i].hands)
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_trips(self.players[i].hands):
                        self.players[i].hand_rank = 3
                        self.players[i].best_cards = self.is_trips(self.players[i].hands)
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[0])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[1])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[2])
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_two_pair(self.players[i].hands):
                        self.players[i].hand_rank = 2
                        self.players[i].best_cards = self.is_two_pair(self.players[i].hands)
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[0])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[1])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[2])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[3])
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    elif self.is_pair(self.players[i].hands):
                        self.players[i].hand_rank = 1
                        #puts pair into best list that will contain best 5 cards
                        self.players[i].best_cards = self.is_pair(self.players[i].hands)
                        #removes the matches from the rest of elligble cards
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[0])
                        self.players[i].hands.remove_card(self.players[i].best_cards.deck[1])
                        self.players[i].num_card_value = self.players[i].best_cards.deck[0].rank
                    else:
                        self.players[i].hand_rank = 0
                        self.players[i].num_card_value = self.players[i].hands.deck[0].rank
                    #filling rest with cards in players_hands that have the matches taken out
                    temp_counter = 0
                    while len(self.players[i].best_cards) != 5:
                        self.players[i].best_cards.deck.append(self.players[i].hands.deck[temp_counter])
                        temp_counter +=1
            for player in self.players:
                if player.is_folded():
                    player.hand_rank = 0

            for i in self.players:
                self.rankings["Player name:" + str(i.name)] = [i.hand_rank,i.num_card_value]
            print(self.rankings)

            temp_list = []
            temp_list2 = []
            for i in self.rankings:
                temp_list.append(self.rankings[i][0])
            for i in self.rankings:
                temp_list2.append(self.rankings[i][1])
            # temp_list3 = []
            # for player in self.players:
            #     temp_list3.append(player.name)

            self.winners = self.is_winner(temp_list,temp_list2)
            if isinstance(self.winners, list):
                if self.tie_checker(self.winners):
                    print("Correctly calculated Split Pot")
                else:
                    print("ERROR ERROR WRONG SPLIT POT CALCULATION")
                return (self.winners)
                for i in self.winners:
                    print(self.players[i], "is the winner xd")
                print("Split Pot")
            else:
                #winner found
                return self.players[self.winners]
                print("new", self.players[self.winners].name, "is the winner")
        else:
            for player in self.players:
                if not player.is_folded():
                    return player
                    print("Player", player.name, "is the winner")
                    print("Uncontested pot")
    def Chip_Calculation(self):
        winner = self.Showdown()
        #tie scenario
        if isinstance(winner,list):
            for i in winner:
                i.chips = i.chips + self.pot
        else:
            winner.chips = winner.chips + self.pot

    def is_complex_winner(self,competing_players,leftover_cards,winner):

        #Flush doesnt need all this other junk, can just iterarively go down best_cards
        if winner == 5:
            temp = {}
            cards_left = 3
            for i in range(len(competing_players)):
                for j in range(len(leftover_cards)):
                    if competing_players[i] == 0:
                        temp[i] = 0
                        continue
                    else:
                        temp[i] = self.players[i].best_cards
            # print("Comparing Flush")
            for i in range(1,5):
                temp_list = []
                for j in range(len(competing_players)):
                    if temp[j] != 0:
                        temp_list.append(self.players[j].best_cards.deck[i].rank)
                    else:
                        temp_list.append(0)
                flush_winner = max(temp_list)
                count = 0
                for j in range(len(temp_list)):
                    if temp_list[j] == flush_winner:
                        count +=1
                if count ==1:
                    return temp_list.index(flush_winner)
            temp_list = []
            for player in range(len(temp)):
                if temp[player] != 0:
                    temp_list.append(player)
            return temp_list
        #going through highcards iteratively
        #puts all competing players cards in a dictionary
        temp = {}
        cards_left = 3
        for i in range(len(competing_players)):
            for j in range(len(leftover_cards)):
                if competing_players[i] == 0:
                    temp[i] = 0
                    continue
                else:
                    temp[i] = leftover_cards[i]
        temp_list = []
        if winner == 6:
            for i in temp:
                if temp[i] != 0:
                    temp_list.append(self.players[i].best_cards.deck[3].rank)
                else:
                    temp_list.append(0)
            pair_winner = max(temp_list)
            count = 0
            for j in range(len(temp_list)):
                if temp_list[j] == pair_winner:
                    count+=1
            if count == 1:
                # print("Winner winner full house")
                return temp_list.index(pair_winner)
            else:
                temp_list = []
                for player in range(len(temp)):
                    if temp[player] != 0:
                        temp_list.append(player)
                return temp_list
        temp_list = []
        #is quads
        if winner == 7:
            cards_left = 1
        #comparing second pair of twopair
        elif winner == 2:
            cards_left = 1
            # print("Comparing Second Pairs")
            for i in temp:
                if temp[i] != 0:
                    temp_list.append(self.players[i].best_cards.deck[2].rank)
                else:
                    temp_list.append(0)
            second_pair_winner = max(temp_list)
            count = 0
            for j in range(len(temp_list)):
                if temp_list[j] == second_pair_winner:
                    count +=1
                else:
                    temp[j] = 0
            if count ==1:
                # print("One has higher second pair")
                return temp_list.index(second_pair_winner)
        elif winner == 3:
            cards_left = 2
        elif winner == 4:
            temp_list = []
            for i in range(len(competing_players)):
                if competing_players[i] != 0:
                    temp_list.append(i)
            return temp_list
        elif winner == 8:
            temp_list = []
            for i in range(len(competing_players)):
                if competing_players[i] != 0:
                    temp_list.append(i)
            return temp_list


        for i in range(cards_left):
            temp_list = []
            count = 0
            for j in temp:
                if isinstance(temp[j],int):
                    temp_list.append(0)
                    continue
                else:
                    temp_list.append(leftover_cards[j].hands.deck[i].rank)
            print("high card rank-off")
            winner3 = max(temp_list)
            for k in range(len(temp_list)):
                if temp_list[k] == winner3:
                    count +=1
                else:
                    temp[k] = 0
            if count == 1:
                return temp_list.index(winner3)
        temp_list = []
        #Split Pot or Tie
        for player in range(len(temp)):
            if temp[player] != 0:
                temp_list.append(player)
        return temp_list
    def is_winner(self,rankings,highest_card):
        winner = max(rankings)
        num_best_hand = 0
        best_hand_high_card = []
        #counting number of players that have the best hand
        for i in range(len(rankings)):
            if rankings[i] == winner:
                num_best_hand +=1
                best_hand_high_card.append(highest_card[i])
            else:
                best_hand_high_card.append(0)
        #one clear winner with best hand
        if num_best_hand == 1:
            return rankings.index(winner)

        #more than one person has the best hand point, but one has the highest pair/trip/
        temp_list = []
        num_best_hand = 0
        winner2 = max(best_hand_high_card)
        for i in range(len(best_hand_high_card)):
            if best_hand_high_card[i] == winner2:
                num_best_hand += 1
            else:
                best_hand_high_card[i] = 0
        if num_best_hand == 1:
            return best_hand_high_card.index(winner2)

        #what happens if more than one person has best hand point and same high_card, need to go iteratively
        print("going through the complex winner function")
        # print(best_hand_high_card)
        return (self.is_complex_winner(best_hand_high_card,self.players,winner))
    def is_straight_flush(self,hands):
        unique_cards = list_Cards()
        #gets rid of pairs in hand
        flush = False
        temp_suits = []
        for i in range(len(hands)):
            temp_suits.append(hands.deck[i].suit)
        for i in (self.deck.suit):
            if temp_suits.count(i) >= 5:
                match = i
                flush = list_Cards()
                x = 0
                for j in range(len(hands)):
                    if hands.deck[j].suit == match:
                        flush.add_card(hands.deck[j])
                        x +=1
                    if x == 5:
                        break
                flush = True
        if flush == False:
            return False
        else:
            for i in range(len(hands)):
                if hands.deck[i].suit == match:
                    unique_cards.add_card(hands.deck[i])
        if unique_cards.deck[0].rank == 14:
            unique_cards.add_card(Card(1,unique_cards.deck[0].suit))
        #
        print(unique_cards)
        print("")
        straight = list_Cards()
        for i in range(len(unique_cards)-4):
            if unique_cards.deck[i].rank == (unique_cards.deck[i+1].rank+1):
                if unique_cards.deck[i].rank == (unique_cards.deck[i+2].rank+2):
                    if unique_cards.deck[i].rank == (unique_cards.deck[i+3].rank+3):
                        if unique_cards.deck[i].rank == (unique_cards.deck[i+4].rank+4):
                            straight.add_card(unique_cards.deck[i])
                            straight.add_card(unique_cards.deck[i+1])
                            straight.add_card(unique_cards.deck[i+2])
                            straight.add_card(unique_cards.deck[i+3])
                            straight.add_card(unique_cards.deck[i+4])
                            return straight
        return False
    def is_quads(self,hands):
        for i in range(len(hands)-3):
            if hands.deck[i] == hands.deck[i+1]:
                if hands.deck[i] == hands.deck[i+2]:
                    if hands.deck[i] == hands.deck[i+3]:
                        quads = list_Cards()
                        quads.add_card(hands.deck[i])
                        quads.add_card(hands.deck[i+1])
                        quads.add_card(hands.deck[i+2])
                        quads.add_card(hands.deck[i+3])
                        return quads
        return False
    def is_full_house(self,hands):
        is_trips = False
        temp_holder = []
        for i in range(len(hands)-2):
            if hands.deck[i] == hands.deck[i+1] and hands.deck[i] == hands.deck[i+2]:
                full_house = list_Cards()
                is_trips = True
                full_house.add_card(hands.deck[i])
                full_house.add_card(hands.deck[i+1])
                full_house.add_card(hands.deck[i+2])
                temp_holder.append(hands.deck[i])
                break
        if is_trips == True:
            for i in range(len(hands)-1):
                if hands.deck[i] == hands.deck[i+1] and hands.deck[i] != temp_holder[0]:
                    full_house.add_card(hands.deck[i])
                    full_house.add_card(hands.deck[i+1])
                    return full_house
        return False
    def is_flush(self,hands):
        temp_suits = []
        for i in range(len(hands)):
            temp_suits.append(hands.deck[i].suit)
        for i in (self.deck.suit):
            if temp_suits.count(i) >= 5:
                match = i
                flush = list_Cards()
                x = 0
                for j in range(len(hands)):
                    if hands.deck[j].suit == match:
                        flush.add_card(hands.deck[j])
                        x +=1
                    if x == 5:
                        break
                return flush
        return False
    def is_straight(self,hands):
        unique_cards = list_Cards()
        #gets rid of pairs in hand
        unique_cards.add_card(hands.deck[0])
        for i in range(1,len(hands)):
            if hands.deck[i] != unique_cards.deck[-1]:
                unique_cards.add_card(hands.deck[i])
        if hands.deck[0].rank == 14:
            unique_cards.add_card(Card(1,hands.deck[0].suit))

        for i in range(len(unique_cards)-4):
            if unique_cards.deck[i].rank == (unique_cards.deck[i+1].rank+1):
                if unique_cards.deck[i].rank == (unique_cards.deck[i+2].rank+2):
                    if unique_cards.deck[i].rank == (unique_cards.deck[i+3].rank+3):
                        if unique_cards.deck[i].rank == (unique_cards.deck[i+4].rank+4):
                            straight = list_Cards()
                            straight.add_card(unique_cards.deck[i])
                            straight.add_card(unique_cards.deck[i+1])
                            straight.add_card(unique_cards.deck[i+2])
                            straight.add_card(unique_cards.deck[i+3])
                            straight.add_card(unique_cards.deck[i+4])
                            return straight
        return False
    def is_trips(self,hands):
        for i in range(len(hands)-2):
            if hands.deck[i] == hands.deck[i+1] and hands.deck[i] == hands.deck[i+2]:
                trips = list_Cards()
                trips.add_card(hands.deck[i])
                trips.add_card(hands.deck[i+1])
                trips.add_card(hands.deck[i+2])
                return trips
        return False
    def is_two_pair(self,hands):
        counter = 0
        values = []
        two_pair = list_Cards()
        for i in range(len(hands)-1):
            if hands.deck[i] == hands.deck[i+1]:
                 counter += 1
                 two_pair.add_card(hands.deck[i])
                 two_pair.add_card(hands.deck[i+1])
                 # values.append(hands[i].rank)
            if counter == 2:
                return two_pair
        return False
    def is_pair(self,hands):
        for i in range(len(hands)-1):
            if hands.deck[i] == hands.deck[i+1]:
                pair = list_Cards()
                pair.add_card(hands.deck[i])
                pair.add_card(hands.deck[i+1])
                return pair
    def tie_checker(self,winners):
        temp_list = []
        for i in winners:
            temp_list.append(self.players[i].best_cards)
        for i in range(len(temp_list)-1):
            if temp_list[i].deck != temp_list[i+1].deck:
                return False
        return True

    def action(self,players):
        villain = 100
        x = True
        while x:
            for player in players:
                if not player.is_folded() and not player.is_all_in():
                    if player.name != villain:
                        print("")
                        print("Player", player.name, "it is your action")
                        print(player.hands)
                        print(player.get_chip_amount(),"remaining in your stack")
                        print("It is ", self.minimum_to_play - self.bets[player.name], "to play")
                        print("there is a total of", self.pot,"in the pot")

                        decision = input("You must Call/Fold/Bet: ")
                        if decision == "fold":
                            player.fold()
                            self.num_current_players -= 1
                        if decision == "bet":
                            amount = input("How much would you like to bet: ")
                            villain = player.name
                            if (self.bets[player.name] + int(amount)) > self.minimum_to_play:
                                self.minimum_to_play = self.bets[player.name] + int(amount)
                            self.bets[player.name] += int(amount)
                            self.pot += int(amount)
                            player.chips = player.subtract_chips(amount)
                            if player.get_chip_amount() == 0:
                                player.all_in = True
                            continue
                        if decision == "call":
                            self.pot += (self.minimum_to_play - self.bets[player.name])
                            player.chips = player.subtract_chips(self.minimum_to_play - self.bets[player.name])
                            if player.get_chip_amount() == 0:
                                player.all_in = True
                            self.bets[player.name] = self.minimum_to_play
                        if self.num_current_players == 1:
                            x = False
                            break
                #once i return back to person who was aggressive i can move on
                if player.name == villain:
                    x = False
                    break
            print("gone over the table once")
            print(self.bets)

            if self.num_current_players == 1:
                x = False
            if unanimous(self.bets.values()):
                x = False
                break
            if villain == 100:
                x = False
class Game(object):
    def __init__ (self,num_players,num_simulations):
        self.players_stacks = {}
        self.num_players = num_players
        self.num_simulations = num_simulations
        self.players_list = []
        self.position = ["Dealer", "Small Blind", "Big Blind","UTG"]
        #special rules for three players
        if self.num_players == 3:
            self.position(remove("UTG"))

        #special rules for headsup
        elif self.num_players == 2:
            self.position.remove("Small Blind")
            self.position.remove("UTG")
    def create_players(self):
        # self.players_stacks["Michael"] = 500
        # self.players_stacks["Linh"] = 500
        # self.players_stacks["Christian"] = 500
        # self.players_stacks["Grant"] = 500
        self.players_list.append(Players(500,"Michael"))
        self.players_list.append(Players(500,"Linh"))
        # self.players_list.append(Players(500,"Christian"))
        # self.players_list.append(Players(500,"Grant"))
        #picking a dealer
        dealer = random.randint(0,self.num_players-1)
        self.players_list = self.players_list[dealer:] + self.players_list[:dealer]

        for player in self.players_list:
            player.give_position(self.position.pop(0))
            #giving all positions to players
            if len(self.position) == 0:
                break
    def play(self):
        one_hand = Poker(self.num_players, self.players_list)
        one_hand.deal()
        one_hand.Chip_Calculation()
        for i in self.players_list:
            print(i.name, i.chips)
        print("")
        print("Best Five Cards")
        for i in range(len(one_hand.players)):
            print("Player", one_hand.players[i].name, "best Cards:")
            print(one_hand.players[i].best_cards)

def unanimous(seq):
   it = iter(seq)
   try:
     first = next(it)
   except StopIteration:
     return True
   else:
     return all(i == first for i in it)
def main():

    sim = Game(2,1)
    sim.create_players()
    sim.play()
main()
