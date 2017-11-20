#!/usr/bin/python

'''!
@package pybaccarat
This module is collection of classes used with playing the game
<B>Baccarat</B>.
@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
@version 0.01
'''

from pybaccarat.playingcards import Card


class Hand(object):
    '''!
    This class represents a hand in the game Baccarat.

    @see playingcards.Card
    @see playingcards.Shoe
    '''
    __HIT_TABLE = [0, 3, 4, 4, 5, 5, 6, 6, 2, 3, 3, 3, 3, 3]
    #              x  A  2  3  4  5  6  7  8  9  T  J  Q  K
    #              0  1  2  3  4  5  6  7  8  9 10 11 12 13

    # -------------------------------------------------------------------------
    def __init__(self):
        '''!
        Create a new hand in Baccarat.

        Example usage:
        @code{.py}
        player = Hand()
        player.add(Card(5,'s')
        player.add(shoe.deal())
        @endcode
        '''
        #
        # save data
        #
        self.__cards = [None, None, None]  # max 3 cards per hand
        self.__size = 0
        self.__bacc_value = 0
        self.empty()

    # -------------------------------------------------------------------------
    def empty(self):
        '''!
        Reset the hand, that is, clear all cards
        '''
        self.__size = 0
        self.__bacc_value = 0

    # -------------------------------------------------------------------------
    def add(self, new_card):
        '''!
        Add a card to the hand
        @param new_card the card to add to the hand
        @exception ValueError
            Raised by either a non-type compatible Card, or
            too many cards already in this Hand.
        '''
        if not isinstance(new_card, Card):
            raise ValueError("add() requires a Card but found type(%s)" %
                             type(new_card))
        size = self.__size
        if size >= 3:
            raise ValueError("too many cards in hand, can not add more")
        else:
            self.__cards[size] = new_card
            self.__size = size + 1
            rank = new_card.get_rank()  # 1..13
            if rank > 9:
                rank = 0
            self.__bacc_value = (self.__bacc_value + rank) % 10

    # -------------------------------------------------------------------------
    def __add__(self, right):
        '''!
        Use the "+" operator to also add a Card to this Hand.
        @param right <em>Card</em>
        '''
        self.add(right)
        return self

    # -------------------------------------------------------------------------
    def value(self):
        '''!
        Get the baccarat hand value
        @return value of the hand
        '''
        return self.__bacc_value

    # -------------------------------------------------------------------------
    def need_hit(self, other_hand):
        '''!
        Does this hand need to hit a third card?
        Checking if the player needs a third card, other_hand should be None.
        The player's hand does not depend on the banker's hand. Only on
        itself.
        Checking if the banker needs a third card, other_hand should be the
        player's hand. The banker's third card decision is depends on the
        player's hand and cards.

        @param other_hand <em>baccarat.Hand</em> or None.
        @return True if yes, False if no.
        '''
        max_hit = 5
        if (other_hand is not None) and isinstance(other_hand, Hand):
            # other_hand should be the player, and this should be banker
            player3 = other_hand.get_card(2)  # player's third card
            if player3 is not None:
                max_hit = self.__HIT_TABLE[player3.get_rank()]
        return self.value() <= max_hit

    # -------------------------------------------------------------------------
    def get_card(self, index):
        '''!
        Return the specified card.
        @param index <em>integer</em> 0 to 2 indicates which Card of this
            Hand to return. If no such Card exists, then None is returned.
        '''
        card = None
        if isinstance(index, int) and (0 <= index) and (index < self.__size):
            card = self.__cards[index]
        return card

    # -------------------------------------------------------------------------
    def is_natural(self):
        '''!
        Is this hand a natural?
        @return True for yes, False for no.
        '''
        return (self.__size == 2) and (self.value() >= 8)

    # -------------------------------------------------------------------------
    def __str__(self):
        '''!
        Return the string representation for this hand.

        This method overrights the method of the same name in the object class.
        @return string with cards contained inside "[...]", comma separated
        '''
        to_string = ""
        for i in range(self.__size):
            if i > 0:
                to_string += ","
            to_string += str(self.__cards[i])
        return "[" + to_string + "]"

    # -------------------------------------------------------------------------
    def __cmp__(self, other):
        '''!
        Compare this hand to <em>other</em> hand.
        @return 0 if the two hands are equal, &gt;0 if other hand has a
            greater value, &lt;0 if other hand has a lesser value. The
            difference in value between the hands is also reflected in
            the magnitude of the difference here. If this hand has a
            value of 3 and other hand has a value of 5, then this compare
            method will return +2.
        '''
        if not isinstance(other, Hand):
            raise ValueError("other type(%s) not type Hand" % type(other))
        return self.value() - other.value()
    # -------------------------------------------------------------------------
# end class Hand


class Game(object):
    '''!
    This class plays a game of Baccarat
    '''

    # -------------------------------------------------------------------------
    def __init__(self, the_shoe, the_player, the_banker, the_system=None):
        '''!
        TBD
        '''
        self.__shoe = the_shoe
        self.__player = the_player
        ##!< banker is the Hand for bank
        self.__banker = the_banker
        ##!< system_play is the bacc system we are tracking
        self.system_play = the_system
        self.count_d7 = 0

    # -------------------------------------------------------------------------
    def play_hand(self):
        '''!
        play a single hand
        zparam hand_number <em>int</em>
        @return (win,diff)
        '''
        bonus = "  "
        # deal first 4 cards
        self.__player.add(self.__shoe.deal())
        self.__banker.add(self.__shoe.deal())
        self.__player.add(self.__shoe.deal())
        self.__banker.add(self.__shoe.deal())
        # if not naturals, then third hits?
        diff = "n"
        if (not self.__player.is_natural()) and \
           (not self.__banker.is_natural()):
            diff = "0"
            if self.__player.need_hit(None):
                self.__player.add(self.__shoe.deal())
            if self.__banker.need_hit(self.__player):
                self.__banker.add(self.__shoe.deal())
        # get winning hand
        if self.__banker < self.__player:
            win = "P"
            if not self.__player.is_natural():
                diff = str(self.__player.value() - self.__banker.value())
        elif self.__banker > self.__player:
            win = "B"
            if not self.__banker.is_natural():
                diff = str(self.__banker.value() - self.__player.value())
            if (self.__banker.value() == 7) and \
               (self.__banker.get_card(2) is not None):
                bonus = "D7"
                self.count_d7 += 1
        else:
            win = "T"
        return (win, diff, bonus)

    # -------------------------------------------------------------------------
    def play(self, display=True, show_burn_cards=False):
        '''!
        TBD
        '''
        # start of new shoe procedure
        self.count_d7 = 0
        self.__shoe.reset()
        self.__shoe.shuffle()
        self.__shoe.set_cut_card(-14)
        burn = self.__shoe.deal()
        if display:
            display_burn = "burn(%s)" % str(burn)
        if self.system_play is not None:
            self.system_play.new_shoe(burn)
        burn = burn.get_rank()
        if burn > 9:
            burn = 10
        for _ in range(burn):
            burned_card = self.__shoe.deal()
            if show_burn_cards:
                display_burn += " " + str(burned_card)
            else:
                display_burn += " XX"
        if display:
            print(display_burn)
        # play the entire shoe
        hand_number = 0
        last_hand = False
        bpt = {'B': 0, 'P': 0, 'T': 0}
        while not last_hand:
            # start of a hand
            hand_number += 1
            self.__player.empty()
            self.__banker.empty()
            last_hand = self.__shoe.cut_card_seen()

            (win, diff, bonus) = self.play_hand()
            bpt[win] += 1

            # shoe hand results
            if self.system_play is not None:
                glf_hand = self.system_play.hand(hand_number,
                                                 win+diff,
                                                 self.__player,
                                                 self.__banker)
            else:
                glf_hand = ""
            if display:
                print("%02d P%d%-10s B%d%-10s %s%s %s BPT=%02d-%02d-%02d %s" %
                      (hand_number,
                       self.__player.value(), str(self.__player),
                       self.__banker.value(), str(self.__banker),
                       win, diff, bonus,
                       bpt['B'], bpt['P'], bpt['T'], glf_hand))
            # notify the user
            if self.__shoe.cut_card_seen() and not last_hand:
                if display:
                    print("last hand of this shoe")
            #
        #
        # end of shoe
        #
        if display:
            print("                                D7(%d)" % self.count_d7)
        if self.system_play is not None:
            print(self.system_play.end_shoe())
    # -------------------------------------------------------------------------
# end class Game
