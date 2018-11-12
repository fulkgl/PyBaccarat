#!/usr/bin/python

'''!
@package pybaccarat.baccarat
This module is collection of classes used with playing the game
<B>Baccarat</B>.
<p>Classes:
<ul compact>
<li>Hand</li>
<li>Scoreboard</li>
<li>Ties</li>
<li>Game</li>
</ul>
@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
@version 0.21
0.18 basic functions all working promperly
0.19 interactive script added to installation,remove hand_num param on hand_pre
0.20 added JustBoards
0.21 play script add, just_boards
0.22 save_shoe had small error, scoreboard no more debug
'''


from pybaccarat.playingcards import Card,Shoe

__version__ = 0.22  ##!<@version 0.22


class Hand(object):
    '''!
    This class represents a hand in the game Baccarat.

    @see playingcards.Card
    @see playingcards.Shoe
    '''
    __HIT_TABLE = [0, 3, 4, 4, 5, 5, 6, 6, 2, 3, 3, 3, 3, 3]
    # rank         x  A  2  3  4  5  6  7  8  9  T  J  Q  K
    # index        0  1  2  3  4  5  6  7  8  9 10 11 12 13

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


class Scoreboard(object):
    '''!
    TBD
    board0 = "big road"
    board1 = "big eye boy"
    board2 = "small road"
    board3 = "cockroach pig"
    '''
    RED_SAME = 's'
    BLUE_CHOP = 'C'

    def __init__(self, type, table_size=6):
        self.board_type = type
        self.h_array = [ "R%d" % type ]
        self.horiz_count = table_size * [0]
        self.lines = (table_size+1) * [None]
        self.lines[0] = "....v....1....v....2....v....3....v....4" + \
            "....v....5....v....6" + " R%d" % type
        for i in range(table_size):
            self.lines[i + 1] = " "*60 + " %2d" % self.horiz_count[i]

    def get_array(self):
        return self.h_array

    def get_horiz_count(self):
        return self.horiz_count

    def mark(self, marker):
        '''!
        Mark the scoreboard. For board type 0 marker should be "B" or "P" for
        Banker or Player. For board types 1,2,3 marker should be "C" or "s"
        for Chop or Same.
        @param self this instance of the class
        @param marker single char
        '''
        # only mark the board if it was a legal marker value
        if (self.board_type == 0 and marker != "B" and marker != "P"):
            return
        if (self.board_type > 0 and marker != "C" and marker != 's'):
            return
        if (self.board_type < 0):
            return

        # Do we need to add a new column to the horizontal array?
        # "len<2" means this is the first mark on this board.
        # "[-1][0]!=marker" means this is a different marker from the
        # last one recorded, thus requires a new column.
        if len(self.h_array) < 2 or self.h_array[-1][0] != marker:
            # add a new column with a count of 0 (incremented later)
            self.h_array.append( [marker, 0] )
        # increment the count in this column
        col = len(self.h_array) - 1
        self.h_array[col][1] += 1
        # time to mark the print lines
        row = self.h_array[col][1]
        #
        six = len(self.horiz_count)
        sixty = len(self.lines[0]) - 3
        # update the horiz count
        if row <= six:
            self.horiz_count[row - 1] += 1
            self.lines[row] = self.lines[row][:sixty + 1] + \
                "%2d" % self.horiz_count[row - 1]
        # calculate the slide
        slide = 0
        for iRow in range(row - 1):
            if six <= iRow:
                slide = row - iRow
                break
            if marker != self.lines[iRow + 1][col - 1]:
                slide = row - iRow
                break
        if slide == 0:
            if six < row:
                slide = row - six
            else:
                if " " != self.lines[row][col - 1]:
                    slide = 1
        #
        if sixty < col + slide:
            # slide too far to the right, add special mark
            self.lines[row - slide] = \
                self.lines[row - slide][:sixty] + ">" + \
                self.lines[row - slide][sixty + 1:]
        else:
            #check for same below us without slide, change to "="
            if slide == 0 and row < six:
                if marker == self.lines[row + 1][col - 1]:
                    self.lines[row + 1] = \
                        self.lines[row + 1][:col - 1] + "=" + \
                        self.lines[row + 1][col:]
            #mark it, it should be empty
            self.lines[row - slide] = \
                self.lines[row - slide][:col + slide - 1] + marker + \
                self.lines[row - slide][col + slide:]

    def get_cs_mark(self, main_array):
        '''!
        Get the CS (chop/same) (blue/red) marks for the boards.

        R2...
        if L0 == 1:
                if L1 != L3: BC
        if L0 > 1:
                if L0 == L2: BC
        Next chop side:
                if L0 != L2: BC
        '''
        col = len(main_array) - 1
        row = main_array[-1][1]
        if row == 1:
            if 0 < col - 1 - self.board_type:
                len_type_col = main_array[col - 1 - self.board_type][1]
                len_col_1 = main_array[col - 1][1]
                if len_col_1 != len_type_col:
                    return self.BLUE_CHOP
                return self.RED_SAME
        else:
            if 0 < col - self.board_type:
                len_type_col = main_array[col - self.board_type][1]
                if row - 1 == len_type_col:
                    return self.BLUE_CHOP
                return self.RED_SAME
        return " "

    def get_peek_B_array(self,arr):
        temp = []
        for i in list(arr):
            a = i[:]
            temp.append(a)
        # copy by value not reference
        last_col = len(arr) - 1
        if last_col < 1 or 'B' != arr[last_col][0]:
            temp.append(['B', 1])
        else:
            temp[last_col][1] += 1
        return temp

    def print_lines(self):
        out = ""
        for line in self.lines:
            out += line + "\n"
        return out

    def remove_last(self):
        pass

# end class Scoreboard


class Ties(object):
    '''!
    This class tracks tie results.
    '''

    # -------------------------------------------------------------------------
    def __init__(self):
        '''!
        TBD
        '''
        self.__tie_tracker = ""
        self.__prior1 = "x"
        self.__prior2 = "x"

    # -------------------------------------------------------------------------
    def mark(self, winner):
        '''!
        Record the winning hand from a game.
        @param winner char 'B' or 'P' or 'T'
        '''
        if winner == "T":
            if self.__prior1 == "x":
                #print("1st hand of new shoe is tie")
                new_tie = "X"
            elif self.__prior1 == "T":
                #print("T follow T")
                self.__prior1 = self.__prior2
                #new_tie = "T"
                #self.__tie_tracker = self.__tie_tracker[:-1] #remove tailing "?"
                self.__tie_tracker = self.__tie_tracker[:-1] + "T"
                new_tie = "?"
            else:
                #print("T at end of seq")
                new_tie = "?"
            if len(self.__tie_tracker)%(5 + 1) == 5:
                self.__tie_tracker += "-"
            self.__tie_tracker += new_tie
        else:
            #print("not a tie, look at last for CS?")
            if self.__prior1 == "T" and self.__prior2 != 'x':
                if winner == self.__prior2:
                    self.__tie_tracker = self.__tie_tracker[:-1] + "s"
                else:
                    self.__tie_tracker = self.__tie_tracker[:-1] + "C"
        #
        self.__prior2 = self.__prior1
        self.__prior1 = winner

    # -------------------------------------------------------------------------
    def __str__(self):
        '''!
        Print the current status of the tie tracker.
        '''
        return "Ties(%s)" % self.__tie_tracker
    # -------------------------------------------------------------------------
    def remove_last(self):
        if len(self.__tie_tracker) > 0:
            self.__tie_tracker = self.__tie_tracker[:-1]

    # -------------------------------------------------------------------------
# end class Ties


class Game(object):
    '''!
    This class plays a game of Baccarat
    '''

    # -------------------------------------------------------------------------
    def __init__(self, shoe=None, player=None, banker=None, system=None):
        '''!
        TBD
        '''
        #
        if shoe is None:
            shoe = Shoe(8)
            shoe.shuffle()
        if player is None:
            player = Hand()
        if banker is None:
            banker = Hand()
        #
        self.__shoe = shoe
        self.__player = player
        ##!< banker is the Hand for banker
        self.__banker = banker
        ##!< system_play is the bacc system we are tracking
        self.system_play = system
        #
        self.count_d7 = 0
        self.count_p8 = 0

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
        if self.__banker.value() < self.__player.value():
            win = "P"
            if not self.__player.is_natural():
                diff = str(self.__player.value() - self.__banker.value())
            if (self.__player.value() == 8) and \
               (self.__player.get_card(2) is not None):
                bonus = "P8"
                self.count_p8 += 1
        elif self.__banker.value() > self.__player.value():
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

    def side_count(self, hand, rc1, rc2):
        for i in range(3):
            c = hand.get_card(i)
            if c is not None:
                r = c.get_rank()
                if r == 1 or r == 2 or r == 3:
                    rc1 += 1
                elif r == 4 or r == 5 or r == 6 or r == 7:
                    rc2 += 1
                elif r == 8 or r == 9:
                    rc1 += -1
                    rc2 += -2
        return rc1,rc2

    # -------------------------------------------------------------------------
    def play(self, display=True, show_burn_cards=False, cut_card=-14):
        '''!
        Play one game of Baccarat.
        '''

        # start of new shoe procedure
        self.count_d7 = 0
        self.count_p8 = 0
        self.__shoe.reset()
        #self.__shoe.shuffle()
        self.__shoe.set_cut_card(cut_card)
        tie_track = Ties()
        boards = [Scoreboard(0), Scoreboard(1), Scoreboard(2), Scoreboard(3)]
        rc1 = 0
        rc2 = 0

        # burn procedure
        burn = self.__shoe.deal()
        if display:
            display_burn = "burn(%s)" % str(burn)
        burned_cards = [burn]
        burn = burn.get_rank()
        if burn > 9:
            burn = 10
        for _ in range(burn):
            burned_card = self.__shoe.deal()
            if show_burn_cards:
                display_burn += " " + str(burned_card)
                burned_cards.append(burned_card)
            else:
                display_burn += " XX"

        # prepare before playing entire shoe
        hand_number = 0
        last_hand = False
        bpt = {'B': 0, 'P': 0, 'T': 0}
        win = 'X'

        special_JustBoards = False
        if display:
            print(display_burn)
        if self.system_play is not None:
            special_JustBoards = self.system_play.new_shoe(burned_cards, boards)
            self.system_play.set_tie_object(tie_track)
            self.system_play.set_bpt_object(bpt)
            if special_JustBoards:
                special_card9s = Card(9, 's')
                special_cardJh = Card(11, 'h')
        #
        while not last_hand:
            # start of a hand
            hand_number += 1
            self.__player.empty()
            self.__banker.empty()
            last_hand = self.__shoe.cut_card_seen()
            system_hand_output = ""
            if self.system_play is not None:
                #
                print(79*"=")
                print(boards[0].print_lines())
                print(boards[2].print_lines())
                print(str(tie_track))
                print(self.system_play.end_shoe())
                #
                system_hand_output = self.system_play.hand_pre()
                if special_JustBoards:
                    print("***\n*** special_JustBoards\n***")
                    if system_hand_output == "B" or \
                       system_hand_output == "P" or \
                       system_hand_output == "T":
                        next_card = self.__shoe._Shoe__next_card
                        print("*** force a %s" % system_hand_output)
                        special_1 = special_cardJh
                        special_2 = special_cardJh
                        if system_hand_output != "B":
                            special_1 = special_card9s
                        if system_hand_output != "P":
                            special_2 = special_card9s
                        self.__shoe._Shoe__cards[next_card+0] = special_cardJh
                        self.__shoe._Shoe__cards[next_card+1] = special_cardJh
                        self.__shoe._Shoe__cards[next_card+2] = special_1 #p2
                        self.__shoe._Shoe__cards[next_card+3] = special_2 #b2
                    elif system_hand_output == "X":
                        print("*** backup")
                        hand_number -= 1
                        if hand_number < 0:
                            hand_number = 0
                        print("***win(%s)" % win)
                        if win == 'X':
                            print("can not clear")
                        else:
                            bpt[win] -= 1
                            if win == 'T':
                                tie_track.remove_last()
                            win = 'X'
                        boards[0].remove_last()
                        h_array = boards[0].get_array()
                        if 1 < len(h_array):
                            #last_col = len(h_array
                            h_a_index = len(h_array) - 1
                            boards[0].h_array[h_a_index][1] -= 1
                        for j in range(1,4):
                            boards[j].remove_last()
                            print("%s" % str(boards[j].get_array()))
                            print("%s" % str(boards[j].get_horiz_count()))
                        continue
                    else:
                        print("*** what is this??? (%s)" % system_hand_output)

            (win, diff, bonus) = self.play_hand()
            bpt[win] += 1
            tie_track.mark(win)
            boards[0].mark(win)
            for j in range(1,4):
                if win != "T":
                    boards[j].mark(boards[j].get_cs_mark(boards[0].get_array()))

            # shoe hand results
            if self.system_play is not None:
                system_hand_output += self.system_play.hand_post(win+diff,
                                                                 self.__player,
                                                                 self.__banker)

            #running counts
            rc1,rc2 = self.side_count(self.__player, rc1, rc2)
            rc1,rc2 = self.side_count(self.__banker, rc1, rc2)

            if display:
                board0horiz_count = boards[0].get_horiz_count()
                #
                peekB = ""
                if True:
                    board0arr = boards[0].get_array()
                    arrayB = boards[0].get_peek_B_array(board0arr)
                    peekB += boards[1].get_cs_mark(arrayB)
                    peekB += boards[2].get_cs_mark(arrayB)
                    peekB += boards[3].get_cs_mark(arrayB)
                #
                flag1 = " "
                flag2 = " "
                if (25 + hand_number // 11) < rc1:
                    flag1 = ">"
                if (32 - 4 * (hand_number // 11)) < rc2:
                    flag2 = "<"

                print(("%02d P%d%-10s B%d%-10s %s%s %s BPT=%02d-%02d-%02d" + \
                      " %02d/%02d %s%s%02d,%02d%s %s") %
                      (hand_number,
                       self.__player.value(), str(self.__player),
                       self.__banker.value(), str(self.__banker),
                       win, diff, bonus, bpt['B'], bpt['P'], bpt['T'],
                       board0horiz_count[0], board0horiz_count[1], peekB,
                       flag1, rc1, rc2, flag2, system_hand_output))
            # notify the user
            if self.__shoe.cut_card_seen() and not last_hand:
                if display:
                    print("last hand of this shoe")
            #

        #
        # end of shoe
        #
        if display:
            print("%-30s  D7(%d) P8(%d)" % \
                (str(tie_track), self.count_d7, self.count_p8))
            print(boards[0].print_lines())
            print(boards[2].print_lines())

        if self.system_play is not None:
            print(self.system_play.end_shoe())
    # -------------------------------------------------------------------------
# end class Game
