#!/usr/bin/python

'''!
@package pybaccarat.playingcards
This module is collection of classes used with playing Cards.
The Card class is the representation of a single playing card.
The Shoe class is the representation of a stack of playing cards.
This stack could be a single deck (such as poker), or a multi-deck
deck (such as Baccarat).

To use:
from playingcards import Card
from playingcards import Stack

@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
'''

# http://www.stack.nl/~dimitri/doxygen/index.html
import random


class Card(object):
    '''!
    The Card class represents a single playing card.

    It is immutable. That is, once created this Card can not be changed.
    This Card is a general purpose playing card that can be use by many
    different games.

    Example usage:
    @code{.py}
        import pybaccarat.playingcards
        #create a five of spades
        card5s = pybaccarat.playingcards.Card(43) #(5, 's')
        #print this card
        print(card5s) #displays '5s'
    @endcode
    @see Shoe
    '''

    # --------------------------------------------------------------------
    def __init__(self, new_ordinal, new_suit=None):
        '''!
        Create a new playing card. There are 3 syntaxes that can be used to
        create this new card. First, a single integer in the range 0 to 51.
        Where each integer maps to a particular rank and suit. The second
        syntax is to supply a rank and suit. Third, a string naming of the
        rank and suit.

        Example usage:
        @code{.py}
            import pybaccarat.playingcards
            #create a five of spades
            card5s = pybaccarat.playingcards.Card(43) #(5, 's')
            #create a jack of diamods
            cardJh = pybaccarat.playingcards.Card(11, 'd')
            #create an ace of clubs
            cardAs = pybaccarat.playingcards.Card("Ac")
        @endcode

        The first syntax is a single integer value 0 to 51. This would likely
        be used by a program that wants to create an array of cards quickly.
        Such as a complete deck of cards. To create a complete deck of cards
        use the following code.
        @code{.py}
            from pybaccarat.playingcards import Card
            deck = []
            for c in range(52):
                deck.append(Card(c))
        @endcode

        The second syntax would be the case of creating a single specific
        playing card. This would likely be a rare useage. But, it is available
        in case a single card is wanted. The syntax would be 2 arguments:
        rank and suit. The rank is an integer in the range 1 to 13.
        The suit is a single string character.
        @code{.py}
            from pybaccarat.playingcards import Card
            c5s = Card(5, 's')  # create a five of spades
        @endcode

        The third syntax is similar to the second, only using the string
        representation of the Card. This is the same syntax used to write
        a Card object with the str() method.
        @code{.py}
            from pybaccarat.playingcards import Card
            c5s = Card('5s')  # create a five of spades
        @endcode

        @param self this object pointer reference
        @param new_ordinal integer value 0 to 51 inclusive.
            If 2 arguements are given for the creation of a card the integer
            value will be the rank in the range 1 to 13. Or a string
            representation of the Card value.
        @param new_suit Used only when 2 arguments are given for creating a
            new card. The single string character will represent the suit.
            Accepted values are 's', 'h', 'd', or 'c'.
        @exception ValueError
            If the input parameter is not valid this exception
            will be raised.

            An example of an exception is:
            @code{.py}
                import pybaccarat.playingcards
                c = pybaccarat.playingcards.Card(66)
                ValueError: new_ordinal(66) not in legal range 0..51
            @endcode
        '''

        #
        # validate data
        #
        if isinstance(new_ordinal, str) and new_suit is None:
            #
            # Third syntax, input string representation. Card('5s')
            #
            new_ordinal = new_ordinal.strip()
            if len(new_ordinal) != 2:
                raise ValueError("new_ordinal(%s) not legel length 2 string" %
                    str(new_ordinal))
            # look for legal rank
            new_rank = 'A23456789TJQK'.find(new_ordinal[0].upper())
            if new_rank == -1:
                raise ValueError("illegal rank part of new_ordinal(%s)" %
                    str(new_ordinal))
            new_rank += 1  # 1..13
            # accept upper/lower suit name
            new_suit = new_ordinal[1].lower()
            suit_index = 'cdhs'.find(new_suit)
            if suit_index == -1:
                raise ValueError("new_suit(%s) not a legal value('cdhs')" %
                                 str(new_suit))
            new_ordinal = (new_rank - 1) + (13 * suit_index)
        elif isinstance(new_ordinal, int) and new_suit is not None:
            #
            # The second syntax has been used. One integer (1 to 13) and
            # a single string character for the suit. Card(5, 's')
            #
            if (new_ordinal < 1) or (13 < new_ordinal):
                raise ValueError("new_ordinal(%s) not in rank range 1..13" %
                                 str(new_ordinal))
            if (not isinstance(new_suit, str)) or (len(new_suit) != 1):
                raise ValueError("new_suit(%s) is not a single char" %
                                 str(new_suit))
            suit_index = 'cdhs'.index(new_suit)
            if suit_index == -1:
                raise ValueError("new_suit(%s) not a legal value('cdhs')" %
                                 str(new_suit))
            new_rank = new_ordinal
            new_ordinal = (new_rank - 1) + (13 * suit_index)
        elif isinstance(new_ordinal, int) and new_suit is None:
            #
            # The first syntax has been used. new_ordinal must be an
            # integer in the range 0 to 51. Card(43)
            #
            if (new_ordinal < 0) or (51 < new_ordinal):
                raise ValueError("new_ordinal(%s) not in legal range 0..51" %
                                 str(new_ordinal))
            new_rank = 1 + (new_ordinal % 13)
            new_suit = 'cdhs'[new_ordinal // 13]
        else:
            raise ValueError("invalid syntax new_ordinal(%s) suit(%s)" % (
                str(new_ordinal),str(new_suit)))
        # we have valid new_rank, new_suit, new_ordinal

        #
        # save data
        #

        # Since this class is immutable all values are computed here.
        # No need to compute values later when methods are called.
        self.__rank = new_rank
        self.__suit = new_suit
        self.__ordinal = new_ordinal
        self.__to_string = 'A23456789TJQK'[self.__rank - 1] + self.__suit
        #
        # Extending original design...
        # face_up True/False
        # images? No. They don't belong here. Images will be loaded from
        # different sources or formats. Furthermore, weighting down this simple
        # class is a poor idea. A separate class with the images is a better
        # idea.
        #
        #self.face_up = False

    # --------------------------------------------------------------------
    def get_rank(self):
        '''!
        Return the rank of this card.

        @param self this object pointer reference
        @return integer 1..13
            <TABLE BORDER="1" ID="rank">
            <TR><TD>1</TD><TD>ace</TD></TR>
            <TR><TD>2 to 10</TD><TD>are numbered cards 2 to 10</TD></TR>
            <TR><TD>11</TD><TD>jack</TD></TR>
            <TR><TD>12</TD><TD>queen</TD></TR>
            <TR><TD>13</TD><TD>king</TD></TR>
            </TABLE>
        '''
        return self.__rank

    # --------------------------------------------------------------------
    def get_suit(self):
        '''!
        Return the suit of this card.

        @param self this object pointer reference
        @return single lower case character
            <TABLE ID="suit" BORDER="1">
            <TR><TD>'c'</TD><TD>clubs</TD></TR>
            <TR><TD>'d'</TD><TD>diamonds</TD></TR>
            <TR><TD>'h'</TD><TD>hearts</TD></TR>
            <TR><TD>'s'</TD><TD>spades</TD></TR>
            </TABLE>
        '''
        return self.__suit

    # -------------------------------------------------------------------------
    def get_ordinal(self):
        '''!
        Return the ordinal value.
        The ordinal value is computed as a single integer value for each of
        the 52 cards.

        @param self this object pointer reference
        @return integer 0..51
        '''
        return self.__ordinal

    # -------------------------------------------------------------------------
    def __str__(self):
        '''!
        Return the string representation for this card.

        This method overwrites the object class method of this same name.

        Example usage:
        @code{.py}
            card5s = Card(43) #(5, 's')
            print(card5s)   #displays '5s'
        @endcode
        @param self this object pointer reference
        @return 2 character long string; rank and suit.
        '''
        return self.__to_string

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        '''!
        Returns the result of equals (==) between this
        Card and other Card.

        Overwrites the default object class behavior. The default object
        class compares instanciated Card's addresses. Thus two cards with the
        same rank and suit will not be equal. This method will cause two cards
        of the same rank and suit to be considered equal.

        Example usage:
        @code{.py}
          import pybaccarat.playingcards
          #create a five of spades
          first = pybaccarat.playingcards.Card(43) #(5, 's')
          #create a second five of spades
          second = pybaccarat.playingcards.Card(43) #(5, 's')
          #test if they are equal
          if first == second:
             print("they are equal")
          #print the message
        @endcode

        @param self this object pointer reference
        @param other <em>object</em> A second Card to compare with
        @return True is this Card equals other Card rank and suit,
            otherwise False. If other is not of Card class type then
            it will be passed to the object class, which will return False.
        '''
        if isinstance(other, self.__class__):
            return (self.get_rank() == other.get_rank()) and \
                   (self.get_suit() == other.get_suit())
        return NotImplemented  # this sends the test to the parent object class

    # -------------------------------------------------------------------------
    def __ne__(self, other):
        '''!
        Returns the result of not equals (!=) between this
        Card and other Card.

        Overwrites the default object class behavior. The default object
        class compares instanciated Card's addresses. Thus two cards with the
        same rank and suit will not be equal. I want two cards of the same
        rank and suit will be equal.

        @param self this object pointer reference
        @param other <em>object</em> A second Card to compare with
        @return True if this Card not equal to other Card, otherwise False.
            If other is not of Card class type then passed to the object class,
            which will return True.
        '''
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    # -------------------------------------------------------------------------
    def __lt__(self, other):
        '''!
        Less than method. Less than does not have meaning for
        a general purpose playing card, so it is disabled.
        @param self this object pointer reference
        @param other <em>object</em> A second Card to compare with
        @exception NotImplmentedError
        '''
        raise NotImplementedError("LT does not have meaning, so not permitted")

    # -------------------------------------------------------------------------
    def __le__(self, other):
        '''!
        Less or equal than method. Less than or equal does not have meaning for
        a general purpose playing card, so it is disabled.
        @param self this object pointer reference
        @param other <em>object</em> A second Card to compare with
        @exception NotImplmentedError
        '''
        raise NotImplementedError("LE does not have meaning, so not permitted")

    # -------------------------------------------------------------------------
    def __gt__(self, other):
        '''!
        Greater than method. Greater than does not have meaning for
        a general purpose playing card, so it is disabled.
        @param self this object pointer reference
        @param other <em>object</em> A second Card to compare with
        @exception NotImplmentedError
        '''
        raise NotImplementedError("GT does not have meaning, so not permitted")

    # -------------------------------------------------------------------------
    def __ge__(self, other):
        '''!
        Greater than or equal method. Greater than or equal does not have
        meaning for a general purpose playing card, so it is disabled.
        @param self this object pointer reference
        @param other <em>object</em> A second Card to compare with
        @exception NotImplmentedError
        '''
        raise NotImplementedError("GE does not have meaning, so not permitted")

    # -------------------------------------------------------------------------
    def __hash__(self):
        """!
        Override the default hash behavior
        (that returns the id of the object).
        The new hash will be the two saved values that define which card
        this class represents.
        @param self this object pointer reference
        @return hash code
        """
        return hash(tuple([self.get_rank(), self.get_suit()]))
    # -------------------------------------------------------------------------
    def __bool__(self):
        """!
        This method is called when the card is used in a boolean expression.
        Since a playing card has no logical reason nor meaning in a boolean
        expression we are raising an exception to avoid an incorrect use of
        a card.
        """
        raise ValueError("bool() not permitted")

    # -------------------------------------------------------------------------
# end class Card()


class Shoe(object):
    '''!
    The Shoe class represents a playing card shoe. That is, a device designed
    to hold a large number of playing cards, and deliver them to a card game
    as requested.

    The Shoe is normally not changed. Once created, it can be reused many
    times. Normal operation would use the reset() method to start a new
    shoe process. The cards within the shoe are shuffled and reused.
    But once created, a shoe will normally remain until end of game(s).

    Example usage:
    @code{.py}
        # create an 8 deck shoe for playing Baccarat
        shoe = Shoe(8)
        shoe.shuffle()
        shoe.set_cut_card(-14)
        # deal one card to player and one card to banker
        player1 = shoe.deal()
        banker1 = shoe.deal()
    @endcode

    @see Card
    '''

    # -------------------------------------------------------------------------
    def __init__(self, number_decks=None):
        '''!
        Create a shoe of a specified number of decks of playing cards.

        The default value for <em>number_decks</em> is one.

        Different card games use a shoe composed of a different number of
        decks of cards. Normally a game of Baccarat would use 8 decks.
        Blackjack might use 1 or 2 or 6. War would use 6.

        Example usage:
        @code{.py}
            import pybaccarat.playingcards
            shoe = pybaccarat.playingcards.Shoe(8) #create 8 deck shoe
            shoe.reset()
            shoe.shuffle()
        @endcode

        An alternative syntax has been added. That allows you to create a shoe
        based on the constructor being passed an array of Cards. That is, each
        element of the array must be of type Card class. This will allow you
        to create your own unique shoe.

        Example usage:
        @code{.py}
            # Create a shoe that consists of only 6 cards specified below.
            # In this case we are running a blackjack tournament, so a special
            # deck with just these 6 cards are shuffled and dealt out to assign
            # tournament starting positions for a 6 spot tournament table.
            import pybaccarat.playingcards
            shoe = pybaccarat.playingcards.Shoe([ Card(1,'s'), Card(2,'s'),
                Card(3,'s'), Card(4,'s'), Card(5,'s'), Card(6,'s') ])
            shoe.reset()
            shoe.shuffle()
            for i in range(6):
                &nbsp;&nbsp;print(shoe.deal())
        @endcode

        @param self this object pointer reference
        @param number_decks <EM>integer</EM> number of decks.
            The default value is 1. Legal range is 1 to 12.
            The alternate constructor will allow you to pass in an arraay of
            Cards instead of just a single integer for the number of decks.
        @exception ValueError
            If the input parameter <em>number_decks</em> is not a legal
            integer.
        @todo need a finite limit to number_decks
        
        Shoe()
        Shoe(8)
        Shoe("PBPPBBB")
        Shoe([Card(43),Card(37),])
        Shoe(0)
        s.save_shoe("filespec")
        s.load_shoe("filespec")
        '''
        #
        # validate params
        #
        self.__cards = []
        if number_decks is None:
            number_decks = 1
        if not isinstance(number_decks, int):
            #
            # Not an integer. What about an array of cards?
            #
            self.__enable_shuffle = False  # don't shuffle this custom shoe
            if isinstance(number_decks, list):
                for i in number_decks:
                    if not isinstance(i, Card):
                        raise ValueError("non-card type params(%s)" % type(i))
                    self.__cards.append(i)
            elif isinstance(number_decks, str):
                ten = Card(10, 's')
                nine = Card(9, 's')
                ace = Card(1, 's')
                for i in range(2):
                    self.__cards.append(ace)
                for i in number_decks:
                    if i == "B":
                        self.__cards.append(ten)  #p1
                        self.__cards.append(ten)  #b1
                        self.__cards.append(ten)  #p2
                        self.__cards.append(nine) #b2
                    elif i == "P":
                        self.__cards.append(ten)  #p1
                        self.__cards.append(ten)  #b1
                        self.__cards.append(nine) #p2
                        self.__cards.append(ten)  #b2
                    elif i == "T":
                        self.__cards.append(nine) #p1
                        self.__cards.append(nine) #b1
                        self.__cards.append(nine) #p2
                        self.__cards.append(nine) #b2
                    else:
                        raise ValueError("number_decks(%s) invalid value(%s)" %
                                         (str(number_decks), i))
                # 7 = 14 - (4-6)(last hand) - (1-3)(pent-ultimate hand)
                for i in range(7):
                    self.__cards.append(ace)
                # pass.... filespec?
                # pass.... BPT sequence
                #raise ValueError("number_decks(%s) not a valid syntax" %
                #                 str(number_decks))
                #
            else:
                raise ValueError("number_decks(%s) not a valid syntax" %
                                 str(number_decks))
        else:
            #
            # number_decks is an integer
            #
            # number_decks==0 is permitted so that a custom shoe can be
            # loaded. Do not enable shuffle for 0 deck shoe.
            if (number_decks < 0) or (12 < number_decks):
                raise ValueError("number_decks(%s) not a legal value" %
                                 str(number_decks))
            self.__enable_shuffle = (0 < number_decks)
            for _ in range(number_decks):
                for _ in range(52):
                    self.__cards.append(Card(_))

        self.__next_card = 0
        self.__cut_card_position = 0
        self.reset()

    # -------------------------------------------------------------------------
    def reset(self):
        '''!
        Reset the shoe to start a new shoe.
        This method will not shuffle the cards nor assign the cut card
        position.

        @code{.py}
            import playingcards
            shoe = playingcards.Shoe()
            shoe.reset()
        @endcode

        @param self this object pointer reference
        '''
        self.__next_card = 0
        self.set_cut_card(0)

    # -------------------------------------------------------------------------
    def shuffle(self):
        '''!
        Shuffle cards in the shoe. Uses the standard Python
        random package shuffle method.

        Example usage:
            @code{.py}
            import playingcards
            shoe = playingcards.Shoe()
            shoe.shuffle()
        @endcode

        @param self this object pointer reference
        @see <A href=
            "https://docs.python.org/3.6/library/random.html#random.shuffle">
            random.shuffle()</A>
        @todo Find a way to attach a user's shuffle method instead of our
            own default.
        '''
        if self.__enable_shuffle:
            random.shuffle(self.__cards)

    # -------------------------------------------------------------------------
    def set_cut_card(self, position):
        '''!
        Assign the cut card position in the shoe.

        Example usage:
        @code{.py}
            import playingcards
            shoe = playingcards.Shoe()
            shoe.set_cut_card(-14)
        @endcode

        @param self this object pointer reference
        @param position <EM><B>integer</B></EM> index position within the shoe.
            0 means at the very start of the shoe.
            A position of 0 would mean that even before the first card has
            been dealt the cut card has been seen.
            The max value is the length of the shoe (the very end).
            For a 6 deck shoe that would mean a maximum value of 312
            (6 times 52). A cut card position at the very end of the shoe
            would mean the cut card would never be seen.
            A negative value is allowed and means position
            from the end of the shoe.
            So a value of -14 would mean count 14 from the end of the shoe.
        @exception ValueError
            If the input parameter <em>position</em> is not a legal integer
            value, then throw a ValueError exception.
        @see cut_card_seen()
        '''
        #
        # validate param
        #
        if not isinstance(position, int):
            raise ValueError("position(%s) not an integer" % str(position))
        if position < 0:
            # if negative position, then adjust it from the end of the shoe.
            position += len(self.__cards)
        if position < 0:
            raise ValueError("cut card position value too small")
        if len(self.__cards) < position:
            raise ValueError("cut card position value too big")
        #
        # save data
        #
        self.__cut_card_position = position

    # --------------------------------------------------------------------
    def cut_card_seen(self):
        '''!
        Return has the cut card been seen?

        Example usage:
        @code{.py}
        import playingcards
        shoe = new playingcards.Shoe()
        shoe.set_cut_card(1)
        # Query before first card dealt
        print(shoe.cut_card_seen()) #False
        card1 = shoe.deal()
        # Query after first card dealt
        print(shoe.cut_card_seen()) #True
        @endcode

        @param self this object pointer reference
        @return True if yes, False if no.
        @see set_cut_card
        '''
        return self.__cut_card_position <= self.__next_card

    # --------------------------------------------------------------------
    def deal(self):
        '''!
        Deal a Card from the Shoe.

        Example usage:
        @code{.py}
        import playinycards
        shoe = playinycards.Shoe()
        #shoe.shuffle() #no shuffle here
        card = shoe.deal()
        print(card) #displays 'Ac'
        # Since a brand new shoe was not shuffled I know ace of clubs is first.
        @endcode

        @param self this object pointer reference
        @return the next card from the Shoe, or
            None if no card is available.
        '''
        card = None
        if self.__next_card < len(self.__cards):
            # we still have cards to deal, so get the next one
            card = self.__cards[self.__next_card]
            self.__next_card += 1
        return card

    # -------------------------------------------------------------------------
    def discard_adjust_baccarat(self, type):
        '''!
        The discard pile is our shoe prior to the next_card index.
        Some games will discard the used cards in a specific manor (i.e.
        Baccarat). They do that so that when a player complains about the
        last hand after the dealer has swept the cards away, the pit card
        back the cards out of the discard pile to show the prior hands.
        
        2P2B:
            deal:  p1 b1 p2 b2 = -4 -3 -2 -1
                   ^--------^ swap -4 -1
                         ^--^ swap -2 -1
            sweep: b2 b1 p1 p2(top)
        3P2B:
            deal:  p1 b1 p2 b2 p3
                   ^--------^    swap -5 -2
                         ^--^    swap -3 -2
            sweep: b2 b1 p1 p2 p3(top)
        2P3B:
            deal:  p1 b1 p2 b2 b3
                   ^-----------^ swap -5 -1
                      ^-----^    swap -4 -2
                         ^--^    swap -3 -2
                            ^--^ swap -2 -1
            sweep: b3 b2 b1 p1 p2(top)
        3P3B:
            deal:  p1 b1 p2 b2 p3 b3
                   ^--------------^ swap -6 -1
                      ^-----^       swap -5 -3
                         ^--^       swap -4 -3
                            ^-----^ swap -3 -1
                               ^--^ swap -2 -1
            sweep: b3 b2 b1 p1 p2 p3(top)
        '''
        if type=="2P2B":
            if 3 <= self.__next_card:
                card1 = self.__cards[self.__next_card - 1]
                card2 = self.__cards[self.__next_card - 2]
                #ard3 =                               - 3]
                card4 = self.__cards[self.__next_card - 4]
                self.__cards[self.__next_card - 4] = card1
                #                             - 3] = card3
                self.__cards[self.__next_card - 2] = card4
                self.__cards[self.__next_card - 1] = card2
        elif type=="3P2B":
            if 4 <= self.__next_card:
                #ard1 =                               - 1]
                card2 = self.__cards[self.__next_card - 2]
                card3 = self.__cards[self.__next_card - 3]
                #ard4 =                               - 4]
                card5 = self.__cards[self.__next_card - 5]
                self.__cards[self.__next_card - 5] = card2
                #                             - 4] = card4
                self.__cards[self.__next_card - 3] = card5
                self.__cards[self.__next_card - 2] = card3
                #                             - 1] = card1
        elif type=="2P3B":
            if 4 <= self.__next_card:
                card1 = self.__cards[self.__next_card - 1]
                card2 = self.__cards[self.__next_card - 2]
                card3 = self.__cards[self.__next_card - 3]
                card4 = self.__cards[self.__next_card - 4]
                card5 = self.__cards[self.__next_card - 5]
                self.__cards[self.__next_card - 5] = card1
                self.__cards[self.__next_card - 4] = card2
                self.__cards[self.__next_card - 3] = card4
                self.__cards[self.__next_card - 2] = card5
                self.__cards[self.__next_card - 1] = card3
        elif type=="3P3B":
            if 5 <= self.__next_card:
                # [-6] = card1
                # [-5] = card3
                card1 = self.__cards[self.__next_card - 1]
                card2 = self.__cards[self.__next_card - 2]
                card3 = self.__cards[self.__next_card - 3]
                card4 = self.__cards[self.__next_card - 4]
                card5 = self.__cards[self.__next_card - 5]
                card6 = self.__cards[self.__next_card - 6]
                self.__cards[self.__next_card - 6] = card1
                self.__cards[self.__next_card - 5] = card3
                self.__cards[self.__next_card - 4] = card5
                self.__cards[self.__next_card - 3] = card6
                self.__cards[self.__next_card - 2] = card4
                self.__cards[self.__next_card - 1] = card2
        else:
            pass # not a legal type

    # -------------------------------------------------------------------------
    def save_shoe(self, filespec):
        '''!
        Save this shoe to a disk file specified.
        '''
        with open(filespec, 'w') as f:
            i = 0
            # write a psuedo burn first
            line = ""
            burn_size = self.__cards[i].rank()
            if burn_size > 9:
                burn_size = 10
            while i < len(self.__cards) and i < (1 + burn_size):
                line += str(self.__cards[i])+" "
                i += 1
            f.write(line+"\n")
            # walk the shoe writing psuedo hands, 5 cards
            while i < len(self.__cards)-14:
                line = ""
                j = 0
                while j < 5:
                    line += str(self.__cards[i])+" "
                    j += 1
                    i += 1
                f.write(line+"\n")
            # write a psuedo end of shoe bolt of what's left
            line = ""
            while i < len(self.__cards):
                line += str(self.__cards[i])+" "
                i += 1
            f.write(line+"\n")

    # --------------------------------------------------------------------
    def load_shoe(self, filespec):
        '''!
        Load a shoe from a disk file specified.
        '''
        with open(filespec, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("#END"):
                break
            if line.startswith("#"):
                continue
            st = line.split()
            for new_card in st:
                if new_card.startswith("#"):
                    break
                self.__cards.append(Card(new_card))

    # -------------------------------------------------------------------------
# end class Shoe()
