#!/usr/bin/python

'''!
@package pybaccarat.baccaratsystems
This module is collection of classes used with
systems for playing the game <B>Baccarat</B>.
@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
'''

import readchar


class Dragon(object):
    '''!
    TBD
    '''

    # --------------------------------------------------------------------
    def __init__(self):
        '''!
        TBD
        '''
        self.dragon_play = "    "
        self.dragon_count = 0
        self.dragon_dict = {}
        self.hand_number = 0

    # --------------------------------------------------------------------
    def update_count(self, rank):
        '''!
        Add these ranks to the count.
        @param rank <em>int</em> card rank's to add to system count
        '''
        if (rank == 1) or (rank == 2) or (rank == 3):
            self.dragon_count += 1
        if (rank == 8) or (rank == 9):
            self.dragon_count -= 1

    # --------------------------------------------------------------------
    def new_shoe(self, burn_cards):
        '''!
        Begin a new shoe.
        @param burn_cards <em>Card</em>
        '''
        ##!< dragon_count used to count my system
        self.dragon_count = 0
        self.update_count(burn_cards[0].get_rank())
        ##!< dragon_play is used for display out
        self.dragon_play = "    "
        ##!< dragon_dict tracks the side bet difference results
        self.dragon_dict = {
            'B9': 0, 'B8': 0, 'B7': 0, 'B6': 0, 'B5': 0, 'B4': 0, 'B3': 0,
            'B2': 0, 'B1': 0, 'P9': 0, 'P8': 0, 'P7': 0, 'P6': 0, 'P5': 0,
            'P4': 0, 'P3': 0, 'P2': 0, 'P1': 0, 'Bn': 0, 'Pn': 0, 'Tn': 0,
            'T0': 0}

    # --------------------------------------------------------------------
    def hand_pre(self):
        self.hand_number += 1
        return ""

    # --------------------------------------------------------------------
    def hand_post(self, win_diff, player, banker):
        '''!
        TBD
        '''
        #
        #             01 >25         =0+25
        #             11 >26         =1+25
        #             33 >28         =3
        #             66 >31         =6
        # hand_number 77 >32    h//11=7+25
        #
        threshold = 25 + (self.hand_number // 11)
        if threshold < self.dragon_count:
            self.dragon_play = " <<<"
            self.dragon_dict[win_diff] += 1
        else:
            self.dragon_play = "    "

        # update count
        for i in range(3):
            card = player.get_card(i)
            if card is not None:
                self.update_count(card.get_rank())
            card = banker.get_card(i)
            if card is not None:
                self.update_count(card.get_rank())
        return "dragon=%s<%02d%s" % \
            (str(threshold), self.dragon_count, self.dragon_play)

    # --------------------------------------------------------------------
    def end_shoe(self):
        '''!
        TBD
        '''
        dragon_p_money = 0
        dragon_b_money = 0
        dragon_plays = 0
        for k, v in self.dragon_dict.items():
            dragon_plays += v
            if   'P4' == k: dragon_p_money += v*1
            elif 'P5' == k: dragon_p_money += v*2
            elif 'P6' == k: dragon_p_money += v*4
            elif 'P7' == k: dragon_p_money += v*6
            elif 'P8' == k: dragon_p_money += v*10
            elif 'P9' == k: dragon_p_money += v*30
            elif 'Pn' == k: dragon_p_money += v*1
            elif 'Tn' == k: dragon_p_money += v*0
            else:           dragon_p_money -= v
            if   'B4' == k: dragon_b_money += v*1
            elif 'B5' == k: dragon_b_money += v*2
            elif 'B6' == k: dragon_b_money += v*4
            elif 'B7' == k: dragon_b_money += v*6
            elif 'B8' == k: dragon_b_money += v*10
            elif 'B9' == k: dragon_b_money += v*30
            elif 'Bn' == k: dragon_b_money += v*1
            elif 'Tn' == k: dragon_b_money += v*0
            else:           dragon_b_money -= v

        out = ""
        if False:
            out += "Tn" + "=" + str(self.dragon_dict['Tn'])
            out += " Bn" + "=" + str(self.dragon_dict['Bn'])
            for i in range(1, 10):
                out += " B"+str(i)+"="+str(self.dragon_dict['B'+str(i)])
            out += "\nT0" + "=" + str(self.dragon_dict['T0'])
            out += " Pn" + "=" + str(self.dragon_dict['Pn'])
            for i in range(1, 10):
                out += " P"+str(i)+"="+str(self.dragon_dict['P'+str(i)])
            out += '\n'
            print(self.dragon_dict)
        out += "dragon_p_money(%d,%d/%d)" % \
            (dragon_p_money, dragon_b_money, dragon_plays)
        return out
    # --------------------------------------------------------------------


class EZDragon(object):
    '''!
    Card count system for EZ-Baccarat Dragon side bet. EZ-Baccarat is the
    shuffle master commission free game. The Dragon side bet pays 40 to 1
    for a banker win of 3 card totalling 7.
    '''

    # --------------------------------------------------------------------
    def __init__(self):
        '''!
        TBD
        '''
        self.play_w = 0
        self.play_l = 0
        self.count = 0
        self.hand_number = 0

    # --------------------------------------------------------------------
    def add_count(self, card_rank):
        '''!
        Local routine to add a card to the count
        '''
        debug = False
        if debug:
            print("rank(%d) count(%d)" % (card_rank, self.count))
        if (4 <= card_rank) and (card_rank <= 7):
            self.count += 1
            if debug:
                print("     plus 1")
        if (card_rank == 8) or (card_rank == 9):
            self.count -= 2
            if debug:
                print("     minus 2")
        if debug:
            print("         count(%d)" % self.count)

    # --------------------------------------------------------------------
    def new_shoe(self, burn_cards):
        '''!
        Start of a new shoe. Start the new count. The burn card is exposed
        so we can record that as an initial value.
        @param <em>burn_rank</em> is the rank of the burn card. Add it to
            the count.
        '''
        self.count = 0
        self.add_count(burn_cards[0].get_rank())
        self.play_w = 0
        self.play_l = 0

    # --------------------------------------------------------------------
    def hand_pre(self):
        self.hand_number += 1
        return ""

    def hand_post(self, win_diff, player, banker):
        '''!
        This is the result of a hand being played.
        @param hand_number <em>int</em>
        @param win_diff <em>TBD?</em> win('BPT') and diff('n' or '0'..'9')
        @param player <em>Hand</em> player hand just played
        @param banker <em>Hand</em> banker hand just played
        @return String for display purposes
        '''
        # save the count for later use
        this_hand_count = self.count
        # add all the cards just played into the count
        for i in range(3):
            card = banker.get_card(i)
            if card is not None:
                self.add_count(card.get_rank())
            card = player.get_card(i)
            if card is not None:
                self.add_count(card.get_rank())
        # who won
        if win_diff[0] == 'B':
            pass
        else:
            pass
        # return string
        true_count = this_hand_count
        # burn 8
        # 416-8-14 = 394 / 80hand = 5cards per hand + 1for burn
        # hand_number = n... (n+1)*5
        # tc = rc / decks_to_go
        # 1 deck_to_go=hand#74-0 = 70   tc4=10*rc(04)/10
        # 2                 64-0 = 60   tc4=10*rc(08)/20
        # 3                 54-1 = 50   tc4=10*rc(12)/30
        # 4                 44-1 = 40   tc4=10*rc(16)/40
        # 5                 34-2 = 30             20
        # 6                 24-2 = 20             24
        # 7                 14-3 = 10             28
        # 8                 04-3 = 0              32
        # dtg(h) = h=0>>8 h=10>>7
        # dtg(h) = 8-(h/10)
        # tc = 10 * rc / (80-h)
        # cut 14

        result = '-'
        true_count = this_hand_count / (8.65 - self.hand_number/10.0)
        next_tc = (self.count) / (8.650 - (self.hand_number + 1.0)/10.0)
        if true_count >= 4.0:
            if (win_diff[0] == 'B') and (banker.value() == 7) and \
               (banker.get_card(2) is not None):
                result = 'WIN'
                self.play_w += 1
            else:
                result = 'LOST'
                self.play_l += 1
        ret = "EZdrag rc(%d)tc(%.1f)next(%.1f)[%s]" % (this_hand_count,
                                                       true_count, next_tc,
                                                       result)
        return ret

    # --------------------------------------------------------------------
    def end_shoe(self):
        '''!
        End of shoe. Show results.
        '''
        print("end_shoe() EZDragon %dW-%dL" % (self.play_w, self.play_l))

    # --------------------------------------------------------------------


class BaccSys(object):
    '''!
    Class that is used to define a Baccarat System.
    Children of this class will be individual class definitions for
    specific Baccarat Systems.
    This parent class will provide the framework for writing your own
    system.

    Normal operation would require a call to the parent class method first,
    then perform any extensions to that method.
    '''
    def __init__(self, system_name="", forced_win=None):
        '''!
        Create a new baccarat system.
        @param system_name String name of the new baccarat system
        '''
        self._reset()
        self.special_forced_win = False
        if forced_win == "JustBoards" and system_name == "JustBoards":
            self.special_forced_win = True
        self.name = system_name

    def new_shoe(self, burn_cards, boards=None, system_data={}):
        '''!
        Start a new shoe.
        @param burn_cards Card[] an array of cards that contain the burn
            cards from a new shoe. An element of None means that card was
            not exposed.
        @param boards Array an array of the display boards
        @param system_data Dict dictionary of data used by the baccarat
            system
        '''
        self._reset()
        self.scoreboards = boards
        self.system_data = system_data
        self.WLseq = [[0,0]]
        return self.special_forced_win

    def _reset(self):
        '''!
        Internal use only.
        Reset the data elements within the baccarat system object.
        '''
        self.hand_number = 0
        self.play_on = None
        self.play_size = 0
        self.won = 0
        self.lost = 0
        self.tied = 0
        self.money = 0.00
        self.scoreboards = None
        self.WLseq = []
        self.last_WLT = ""
        self.quit_shoe = False

    def set_tie_object(self, tie_track):
        '''!
        '''
        self.tie_tracker = tie_track

    def set_bpt_object(self, bpt):
        '''!
        '''
        self.bpt_tracker = bpt

    def hand_pre(self):
        '''!
        Called prior to the play of a Hand.
        A baccarat system should assign any plays in this method.
        The return is a string for display purposes only.
        @return display string
        '''
        self.hand_number = 1
        self.play_on = None
        self.play_size = 0
        return ""

    def result_won(self, amount):
        '''!
        A method called when a hand wins.
        '''
        self.won += 1
        self.money += amount
        seq = self.WLseq
        if seq[-1][1] > 0:
            seq.append( [0,0] )
        seq[-1][0] += 1
        self.WLseq = seq
        self.last_WLT = "W"

    def result_lost(self, amount):
        '''!
        A method called when a hand Losses.
        '''
        self.lost += 1
        seq = self.WLseq
        seq[-1][1] += 1
        self.WLseq = seq
        self.money -= amount
        self.last_WLT = "L"

    def hand_post(self, win_diff, player_hand, banker_hand):
        '''!
        This method is called at the end of a Hand.
        A baccarat system can update their own results.
        @param win_diff String[2] A length 2 string containing the winning
            side ("B" or "P" or "T") and the difference between the winning
            and lossing sides. A 6-6 tie will have "T0". A 6-4 banker win
            will have "B2". A natural will use "n" for the difference.
            An 8-8 tie will have "Tn". A 9-8 banker will would have "Bn".
        @param player_hand Hand a pointer to the Hand object containing the
            cards for the players hand. For read-only purposes.
        @param banker_hand Hand a pointer to the Hand object containing the
            cards for the bankers hand. For read-only purposes.
        '''
        # record results of a play
        if self.play_on is not None and self.play_size > 0:
            if self.play_on == "B":
                if win_diff[0] == "B":
                    self.result_won(0.95 * self.play_size)
                elif win_diff[0] == "T":
                    self.tied += 1
                    self.last_WLT = "T"
                elif win_diff[0] == "P":
                    self.result_lost(self.play_size)
                else:
                    pass#unknown
            elif self.play_on == "P":
                if win_diff[0] == "P":
                    self.result_won(self.play_size)
                elif win_diff[0] == "T":
                    self.tied += 1
                    self.last_WLT = "T"
                elif win_diff[0] == "B":
                    self.result_lost(self.play_size)
                else:
                    pass#unknown?
            elif self.play_on == "T":
                if win_diff[0] == "T":
                    self.result_won(8.0 * self.play_size)
                elif win_diff[0] == "B":
                    self.result_lost(self.play_size)
                elif win_diff[0] == "P":
                    self.result_lost(self.play_size)
                else:
                    pass#unknown?
            else:
                pass#unknown?
        # clear this last play
        self.play_on = None
        self.play_size = 0
        return ""

    def end_shoe(self):
        '''!
        Method called at the end of a shoe, after all hands have been
        played. The return string should give a summary of the baccarat
        system play.
        @return String display system results
        '''
        return "Sys(%s) %d-%d-%d=%+.2f, %s" % (self.name,self.won, \
            self.lost,self.tied,self.money,self.print_WLseq())

    def opposite_side(self, side):
        '''!
        Worker method provided that will return the opposite of "side".
        @param side String "B" or "P".
        @return opposite of "side" or None
        '''
        if side == "P":
            return "B"
        if side == "B":
            return "P"
        return None

    def play(self, side, size=1):
        '''!
        A method called during hand_pre() to assign a play.
        @param side String "B" or "P" or "T"
        @param size integer
        '''
        self.play_on = side
        self.play_size = size
        return side

    def quit_this_shoe(self):
        '''!
        Mark this shoe as no more plays.
        '''
        self.quit_shoe = True

    def print_WLseq(self):
        '''!
        Return a string for display purposes of the Win/Lose sequences.
        '''
        seq = ""
        for i in self.WLseq:
            for j in i:
                seq += "0123456789abcdefghijklmnopqrstuvwxyz"[j]
            seq += " "
        return seq

    def get_keystroke(self):
        '''!
        A method that will get a keystroke and return it as an integer
        value.
        @return integer keystroke value
        '''
        keystroke = 0
        #keystroke = ord(readchar.readkey())
        getch = readchar.readkey()
        for o in getch:
            keystroke = keystroke*256 + ord(o)
        return keystroke

class Interactive(BaccSys):
    '''!
    Play Baccarat with interactive selection of hand plays.
    Press the letter P to play player.
    Press the letter B to play banker.
    Press the enter key to make no play on a hand.
    Press the ESC key to skip to the end of the shoe.
    Press the Ctrl-C for emergency fast exit.
    Press numbers 1 or 2 or 3 or 4 or 5 before the P or B to increase size.
    For instance, press 3 then P will play 3 units on player.
    If no number is pressed it's assumed to be 1.
    '''
    def __init__(self, system_name=""):
        return super(Interactive,self).__init__("interactive")
    def hand_pre(self):
        '''
        We are given a chance to choose a play, prior to dealing cards.
        @return String description of play, such as "P" or "B".
            The returned string is for display purposes only.
            The tracking of the bet made is in the inheritted object
            play_on and play_size.
        '''
        parent_ret = super(Interactive,self).hand_pre()
        my_size = 1
        while not self.quit_shoe:
            keystroke = self.get_keystroke()
            #getch = readchar.readkey()
            #keystroke = 0
            #for o in getch:
            #    keystroke = keystroke*256 + ord(o)
            if chr(keystroke & 223) in ("P","B","T"): #uppercase
                return self.play(chr(keystroke & 223),my_size) #make a play
            elif chr(keystroke) in ("1","2","3","4","5"): #bet size
                my_size = keystroke - ord("0")
            elif keystroke==3:                      # ctrl-C raise exception
                raise ValueError("Ctrl-C request to end game now")
            elif keystroke==27 or keystroke==6939:  # ESC,ESC+ESC quit shoe
                self.quit_this_shoe()
            elif keystroke==13 or keystroke==32:    # enter or space no play
                return ""
            else:
                print("unhandled key(%s)(%d)" % (chr(keystroke),keystroke))
        return ""


class JustBoards(BaccSys):
    def __init__(self, system_name=""):
        return super(JustBoards,self).__init__("JustBoards",
            forced_win="JustBoards")
    def hand_pre(self):
        parent_ret = super(JustBoards,self).hand_pre()
        while not self.quit_shoe:
            #keystroke = self.get_keystroke() #get int keystroke
            #keystroke = ord(readchar.readkey())
            keystroke = self.get_keystroke()
            if chr(keystroke & 223) in ("P","B","T"): #uppercase
                #return self.play(chr(keystroke & 223)) #make a play
                return chr(keystroke & 223)
            elif chr(keystroke & 223) in ("X"):
                return chr(keystroke & 223)
            elif keystroke==3:                      # ctrl-C raise exception
                raise ValueError("Ctrl-C request to end game now")
            elif keystroke==27:                     # ESC quit shoe
                self.quit_this_shoe()
            elif keystroke==13 or keystroke==32:    # enter or space no play
                pass#return ""
            else:
                print("unhandled key(%s)(%d)" % (chr(keystroke),keystroke))
        return ""


class George1(BaccSys):
    '''
    George bacc system 1.
    '''
    def __init__(self, system_name=""):
        parent = super(George1,self).__init__("George1") #call parent
        self.George1_size = 3 #post 5 bet 2, post 6 bet 3
        return parent
    def hand_pre(self):
        '''
        Call out to this method before each hand is played.
        Our system is responsible for making plays prior to
        the play of the hand by calling self.play("B",1).
        Where the "B" or "P" is the side and 1 is the size.
        Before our method is called the default is no play.
        This method returns a string used in the output for
        this hand.
        '''
        parent = super(George1,self).hand_pre() #call parent
        # get the array for board #2 ie: [..., ['C', 5]]
        b2_array = self.scoreboards[2].get_array()
        if len(b2_array) < 2:
            return "" #not on the board yet"
        if b2_array[-1][1] < 5:
            return "" #R2 < 5"
        b0_array = self.scoreboards[0].get_array()
        arrayB = self.scoreboards[0].get_peek_B_array(b0_array)
        peekB2 = self.scoreboards[2].get_cs_mark(arrayB)
        len_R2 = b2_array[-1][1]
        if len_R2 in (5,6):
            long_R2 = b2_array[-1][0]
            # We had 5 long_R2 plays in a row. We now bet opposite.
            # peekB2 is the next play for Banker.
            if peekB2 == long_R2:
                self.play("P",len_R2-self.George1_size)
            else:
                self.play("B",len_R2-self.George1_size)
            self.George1_size = 4
            return ("playG%d"%len_R2)+long_R2+"(%s)"%peekB2
        #elif b2_array[-1][1] == 6:
        #    return "playG6"+b2_array[-1][0]+"(B=%s)"%peekB2
        #return "noplayG7"+b2_array[-1][0]
        return "playG7"

class ValSys(BaccSys):
    def hand_post(self, win_diff, p_hand, b_hand):
        parent_ret = super(ValSys,self).hand_post(win_diff,p_hand,b_hand)
        return " %s" % self.last_WLT
    def hand_pre(self):
        '''!
        ValSystem rules:
        1. if board 2 last entry is in row 1, play chop else play same
        2. overrides rule 1. If 4+ in a row on board 0, play same
        '''
        parent_ret = super(ValSys,self).hand_pre()
        #
        if self.scoreboards is not None:
            b0_array = self.scoreboards[0].get_array()
            if len(b0_array) > 1 and b0_array[-1][1] >= 4:
                rule = 2
                self.play_on = b0_array[-1][0]
                self.play_size = 1
                return "val(%d)=%s" % (rule,self.play_on)
            else:
                b2_array = self.scoreboards[2].get_array()
                if len(b2_array) > 1:
                    rule = 1
                    side = b0_array[-1][0]
                    if b2_array[-1][1] == 1:
                        side = self.opposite_side(side)
                    self.play_on = side
                    self.play_size = 1
                    return "val(%d)=%s" % (rule,self.play_on)
        #
        return ""

    def end_shoe(self):
        seq2 = ""
        for i in self.WLseq:
            for j in i:
                seq2 += "0123456789abcdefghij"[j]
            seq2 += " "
        return "EndSys(%s) %d-%d-%d=%+.2f, %s" % (self.name,self.won, \
            self.lost,self.tied,self.money,seq2)

# END
