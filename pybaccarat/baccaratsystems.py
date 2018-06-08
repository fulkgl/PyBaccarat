#!/usr/bin/python

'''!
@package pybaccarat.baccaratsystems
This module is collection of classes used with
systems for playing the game <B>Baccarat</B>.
@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
@version 0.01
'''

from msvcrt import getch


class Dragon(object):
    '''!
    TBD
    '''

    # -------------------------------------------------------------------------
    def __init__(self):
        '''!
        TBD
        '''
        self.dragon_play = "    "
        self.dragon_count = 0
        self.dragon_dict = {}
        self.hand_number = 0

    # -------------------------------------------------------------------------
    def update_count(self, rank):
        '''!
        Add these ranks to the count.
        @param rank <em>int</em> card rank's to add to system count
        '''
        if (rank == 1) or (rank == 2) or (rank == 3):
            self.dragon_count += 1
        if (rank == 8) or (rank == 9):
            self.dragon_count -= 1

    # -------------------------------------------------------------------------
    def new_shoe(self, burn_card):
        '''!
        Begin a new shoe.
        @param burn_card <em>Card</em>
        '''
        ##!< dragon_count used to count my system
        self.dragon_count = 0
        self.update_count(burn_card.get_rank())
        ##!< dragon_play is used for display out
        self.dragon_play = "    "
        ##!< dragon_dict tracks the side bet difference results
        self.dragon_dict = {
            'B9': 0, 'B8': 0, 'B7': 0, 'B6': 0, 'B5': 0, 'B4': 0, 'B3': 0,
            'B2': 0, 'B1': 0, 'P9': 0, 'P8': 0, 'P7': 0, 'P6': 0, 'P5': 0,
            'P4': 0, 'P3': 0, 'P2': 0, 'P1': 0, 'Bn': 0, 'Pn': 0, 'Tn': 0,
            'T0': 0}

    # -------------------------------------------------------------------------
    def hand_pre(self, hand_num):
        self.hand_number = hand_num
        return ""

    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
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
    # -------------------------------------------------------------------------


class EZDragon(object):
    '''!
    Card count system for EZ-Baccarat Dragon side bet. EZ-Baccarat is the
    shuffle master commission free game. The Dragon side bet pays 40 to 1
    for a banker win of 3 card totalling 7.
    '''

    # -------------------------------------------------------------------------
    def __init__(self):
        '''!
        TBD
        '''
        self.play_w = 0
        self.play_l = 0
        self.count = 0
        self.hand_number = 0

    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    def new_shoe(self, burn_card):
        '''!
        Start of a new shoe. Start the new count. The burn card is exposed so
        we can record that as an initial value.
        @param <em>burn_rank</em> is the rank of the burn card. Add it to
            the count.
        '''
        self.count = 0
        self.add_count(burn_card.get_rank())
        self.play_w = 0
        self.play_l = 0

    # -------------------------------------------------------------------------
    def hand_pre(self, hand_num):
        self.hand_number = hand_num
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

    # -------------------------------------------------------------------------
    def end_shoe(self):
        '''!
        End of shoe. Show results.
        '''
        print("end_shoe() EZDragon %dW-%dL" % (self.play_w, self.play_l))

    # -------------------------------------------------------------------------


class BaccSys(object):
    def __init__(self, sys_name=""):
        self.name = sys_name
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
    def new_shoe(self, burn_card, boards=None):
        self.hand_number = 0
        self.play_on = None
        self.play_size = 0
        self.won = 0
        self.lost = 0
        self.tied = 0
        self.money = 0.00
        self.scoreboards = boards
        self.WLseq = [[0,0]]
        self.last_WLT = ""
    def set_tie_object(self, tie_track):
        self.tie_tracker = tie_track
    def set_bpt_object(self, bpt):
        self.bpt_tracker = bpt
    def hand_pre(self, hand_num):
        self.hand_number = hand_num
        self.play_on = None
        self.play_size = 0
        return ""
    def result_won(self, amount):
        self.won += 1
        self.money += amount
        seq = self.WLseq
        #if len(seq) < 1:
        #    seq = [[1,0]]
        if seq[-1][1] > 0:
            seq.append( [0,0] )
        seq[-1][0] += 1
        self.WLseq = seq
        self.last_WLT = "W"
    def result_lost(self, amount):
        self.lost += 1
        seq = self.WLseq
        #if len(seq) < 1:
        #    seq = [[0,0]]
        #else:
        seq[-1][1] += 1
        self.WLseq = seq
        self.money -= amount
        self.last_WLT = "L"
    def hand_post(self, win_diff, player_hand, banker_hand):
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
                    pass#unknown?
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
        return ""
    def opposite_side(self, side):
        if side == "P":
            return "B"
        if side == "B":
            return "P"
        return None
    def play(self, side, size=1):
        self.play_on = side
        self.play_size = size
    def quit_this_shoe(self):
        self.quit_shoe = True

class interactive(BaccSys):
    def __init__(self, sys_name=""):
        # first, call parent
        parent_ret = super(interactive,self).__init__("interactive")
    def hand_pre(self, hand_num):
        '''
        We are given a chance to choose a play, prior to dealing cards.
        @param hand_num int hand number
        @return String description of play, such as "P" or "B".
            The returned string is for display purposes only.
            The tracking of the bet made is in the inheritted object
            play_on and play_size.
        '''
        # first, call parent
        parent_ret = super(interactive,self).hand_pre(hand_num)
        if not self.quit_shoe:
            my_size = 1
            keystroke = ord(getch())
            uckey = chr(keystroke & 223) #uppercase letter and 1101 1111
            if keystroke==ord("2") or keystroke==ord("3") or \
               keystroke==ord("4") or keystroke==ord("5") or \
               keystroke==ord("1"):
                my_size = keystroke-ord("0")
                keystroke = ord(getch())
                uckey = chr(keystroke & 223)
            if uckey == "P" or uckey == "B":
                self.play(uckey,my_size)
                return uckey
            elif keystroke==3:      #ctrl-C
                raise ValueError("Ctrl-C request to end game")
            elif keystroke==27:     #ESC
                self.quit_this_shoe()
        return " "
    #def hand_post(self, win_diff, p_hand, b_hand):
    #    parent_ret = super(interactive,self).hand_post(win_diff,p_hand,b_hand)
    #    if self.play_size == 0:
    #        return ""
    #    return " %s" % self.last_WLT
    def end_shoe(self):
        seq2 = ""
        for i in self.WLseq:
            for j in i:
                seq2 += "0123456789abcdefghij"[j]
            seq2 += " "
        return "Sys(%s) %d-%d-%d=%+.2f, %s" % (self.name,self.won, \
            self.lost,self.tied,self.money,seq2)

class ValSys(BaccSys):
    def hand_post(self, win_diff, p_hand, b_hand):
        parent_ret = super(ValSys,self).hand_post(win_diff,p_hand,b_hand)
        return " %s" % self.last_WLT
    def hand_pre(self, hand_num):
        '''!
        ValSystem rules:
        1. if board 2 last entry is in row 1, play chop else play same
        2. overrides rule 1. If 4+ in a row on board 0, play same
        '''
        parent_ret = super(ValSys,self).hand_pre(hand_num)
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
