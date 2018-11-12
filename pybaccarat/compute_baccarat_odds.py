#!/usr/bin/python

'''!
Program to compute the odds for the game of Baccarat.

@author <a href="email:fulkgl@gmail.com">George L Fulk</a>
'''


def bacc_value(num1, num2):
    '''!
    Compute the baccarat value with 2 inputed integer rank values (0..12).
    '''
    if num1 > 9:
        num1 = 0
    if num2 > 9:
        num2 = 0
    num1 += num2
    if num1 > 9:
        num1 -= 10
    return num1


def comma(number):
    '''!
    Convert an integer to comma seperated string.
    '''
    str_int = ""
    sign = ""
    quo = number
    if number < 0:
        sign = '-'
        quo = -number
    while quo > 999:
        rem = quo % 1000
        str_int = ",%03d%s" % (rem, str_int)
        quo = quo // 1000
    return "%s%d%s" % (sign, quo, str_int)


class ComputeBaccaratOdds(object):
    '''!
    Compute the odds for the game of Baccarat.
    '''

    def __init__(self, number_decks=8):
        '''!
        Compute Baccarat odds for the given number of decks of cards.

        The range of valid number of decks is limited to 12. The 12 limit
        is an attempt to prevent attacks or bad coding using up resources.

        @param numberDecks  Number of decks to initialized the odds.
            The range of valid value is 1 at a minimum up to 12.
        @throws java.lang.IllegalArgumentException
            Input arguement numberDecks is not valid.
        '''
        # validate args
        if not isinstance(number_decks, int) or \
           (number_decks < 0) or (number_decks > 12):
            raise ValueError("number_decks(%s) not a legal value" %
                             str(number_decks))

        # create the shoe
        self.saved_shoe = 13 * [4 * number_decks]

        # save the dragon table
        self.dragon_pay_table = 3 * [None]
        self.dragon_natural_win = 10
        self.dragon_natural_tie = 11
        #                              0,  1,  2,  3, 4, 5, 6, 7, 8 , 9,nat,nT
        self.dragon_pay_table[1-1] = [-1, -1, -1, -1, 1, 2, 4, 6, 10, 30, 1, 0]
        self.dragon_pay_table[2-1] = [-1, -1, -1, -1, 1, 3, 4, 7,  8, 20, 1, 0]
        self.dragon_pay_table[3-1] = [-1, -1, -1, -1, 2, 2, 4, 4, 10, 30, 1, 0]
        #                                             ^        ^

        # Number of hand combinations that result in Banker,Player,Tie wins.
        self.count_banker = 0
        self.count_player = 0
        self.count_tie = 0
        self.count_naturals = 0
        self.count_pair = 0
        self.count_nonpair = 0
        self.count_banker_3card7 = 0
        self.count_player_3card8 = 0
        self.count_banker_dragon = [0, 0, 0]
        self.freq_banker_dragon  = [0, 0, 0]
        self.count_player_dragon = [0, 0, 0]
        self.freq_player_dragon  = [0, 0, 0]

        # perform the math computation
        self.recompute(self.saved_shoe)

    def record(self, value_banker, value_player, count,
               is_naturals=True,
               is_banker_3cards=False,
               is_player_3cards=False):
        '''!
        Record the results of a hand combination.
        '''
        diff = value_banker - value_player
        if value_player < value_banker:
            # Banker wins
            self.count_banker += count
            if is_banker_3cards and value_banker == 7:
                self.count_banker_3card7 += count

            if is_naturals:  # and not a tie
                diff = self.dragon_natural_win
            for table_num in range(3):  # various dragon tables
                dragon_pays = self.dragon_pay_table[table_num][diff]
                self.count_banker_dragon[table_num] += count * dragon_pays
                if dragon_pays >= 0:
                    self.freq_banker_dragon[table_num] += count
                self.count_player_dragon[table_num] += -count

        elif value_player > value_banker:
            # Player wins
            self.count_player += count
            if is_player_3cards and value_player == 8:
                self.count_player_3card8 += count

            diff = -diff
            if is_naturals:  # and not a tie
                diff = self.dragon_natural_win
            for table_num in range(3):  # various dragon tables
                dragon_pays = self.dragon_pay_table[table_num][diff]
                self.count_player_dragon[table_num] += count * dragon_pays
                if dragon_pays >= 0:
                    self.freq_player_dragon[table_num] += count
                self.count_banker_dragon[table_num] += -count

        else:
            # Tie wins
            self.count_tie += count

            if is_naturals:
                diff = self.dragon_natural_tie
                # special case, table 3 counts the pushes
                self.freq_banker_dragon[3 - 1] += count
                self.freq_player_dragon[3 - 1] += count
            for table_num in range(3):  # various dragon tables
                dragon_pays = self.dragon_pay_table[table_num][diff]
                self.count_player_dragon[table_num] += count * dragon_pays
                self.count_banker_dragon[table_num] += count * dragon_pays

    def not_naturals(self, value_p, value_b, shoe_size, shoe, count4):
        '''!
        Handle the not a naturals situation. Look for a third player and
        third banker situation.
        '''
        #          = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13]
        draw_table = [3, 4, 4, 5, 5, 6, 6, 2, 3, 3, 3, 3, 3, 3]

        if value_p <= 5:
            # Player hits
            for p3 in range(len(shoe)):
                if shoe[p3] != 0:
                    if value_b <= draw_table[p3]:
                        # Banker hits
                        value_p3 = bacc_value(value_p, 1 + p3)
                        count5 = count4 * shoe[p3]
                        shoe[p3] -= 1
                        for b3 in range(len(shoe)):
                            if shoe[b3] != 0:
                                count6 = count5 * shoe[b3]
                                value_b3 = bacc_value(value_b, 1 + b3)
                                self.record(value_b3, value_p3, count6,
                                            False,   # not natural
                                            True,    # 3 card banker
                                            True)    # 3 card player
                        shoe[p3] += 1
                    else:
                        # Banker stands
                        count6 = count4 * shoe[p3] * (shoe_size - 1)
                        value_p3 = bacc_value(value_p, 1 + p3)
                        self.record(value_b, value_p3, count6,
                                    False,   # not natural
                                    False,   # not 3 card banker
                                    True)    # player 3 cards
        else:
            # Player stands
            if value_b <= 5:
                # Banker hits
                for b3 in range(len(shoe)):
                    if shoe[b3] != 0:
                        value_b3 = bacc_value(value_b, 1 + b3)
                        count6 = count4 * shoe[b3] * (shoe_size - 1)
                        self.record(value_b3, value_p, count6,
                                    False,   # not natural
                                    True,    # 3 card banker
                                    False)   # no 3 card player
            else:
                # Banker stands
                count6 = count4 * shoe_size * (shoe_size - 1)
                self.record(value_b, value_p, count6, False)  # False=!natural

    def recompute(self, shoe):
        '''!
        Recompute the math for the given shoe contents.
        The 13 indexed values will represent the number of each of the 13
        cards in a suit. The shoe[0] is the number of aces, shoe[1] is the
        number of twos, et cetera. Up to shoe[12] is the number of Kings.
        @param shoe integer array of length 13
        '''

        # validate shoe and compute it's size
        if not isinstance(shoe, list) or (len(shoe) != 13):
            raise ValueError("int[13] required")
        shoe_size = 0
        for i in shoe:
            if not isinstance(i, int) or (i < 0) or (i > 50):
                raise ValueError("shoe does not contain valid values")
            shoe_size += i

        # init the counts
        self.count_banker = 0
        self.count_player = 0
        self.count_tie = 0
        self.count_naturals = 0
        self.count_pair = 0
        self.count_nonpair = 0
        self.count_banker_3card7 = 0
        self.count_player_3card8 = 0
        self.count_banker_dragon = [0, 0, 0]
        self.count_player_dragon = [0, 0, 0]
        self.freq_banker_dragon  = [0, 0, 0]
        self.freq_player_dragon  = [0, 0, 0]

        # Loop through all possible card combinations
        for p1 in range(len(shoe)):
            if shoe[p1] > 0:
                count1 = shoe[p1]
                shoe[p1] -= 1
                shoe_size -= 1
                for b1 in range(len(shoe)):
                    if shoe[b1] != 0:
                        count2 = count1 * shoe[b1]
                        shoe[b1] -= 1
                        shoe_size -= 1
                        for p2 in range(len(shoe)):
                            if shoe[p2] != 0:
                                count3 = count2 * shoe[p2]
                                shoe[p2] -= 1
                                shoe_size -= 1
                                for b2 in range(len(shoe)):
                                    if shoe[b2] != 0:
                                        count4 = count3 * shoe[b2]
                                        shoe[b2] -= 1
                                        shoe_size -= 1
                                        # -----
                                        # First 2 cards dealt to each side.
                                        #
                                        # count the pair side bet
                                        if p1 == p2:
                                            self.count_pair += count4
                                        else:
                                            self.count_nonpair += count4
                                        #
                                        value_p = bacc_value(1 + p1, 1 + p2)
                                        value_b = bacc_value(1 + b1, 1 + b2)
                                        if (value_p >= 8) or (value_b >= 8):
                                            count6 = count4 * shoe_size * \
                                                (shoe_size - 1)
                                            self.record(value_b, value_p,
                                                        count6)
                                            self.count_naturals += count6
                                        else:  # not natural
                                            self.not_naturals(value_p, value_b,
                                                              shoe_size, shoe,
                                                              count4)
                                        # -----
                                        shoe_size += 1
                                        shoe[b2] += 1
                                    # if b2
                                # for b2=
                                shoe_size += 1
                                shoe[p2] += 1
                            # if p2
                        # for p2=
                        shoe_size += 1
                        shoe[b1] += 1
                    # if b1
                # for b1=
                shoe_size += 1
                shoe[p1] += 1
            # if p1
        # for p1=

    def __str__(self):
        '''!
        Return the string representation of this object.
        @return String
        '''
        output = []
        total = self.count_banker + self.count_player + self.count_tie

        line = "%5s=%22s%8.4f%%%8.4f%%%+9.4f%%" % (
            'B', comma(self.count_banker),
            self.count_banker * 100.0 / total,
            self.count_banker * 100.0 / (self.count_banker + self.count_player),
            (self.count_banker * 0.95 - self.count_player) * 100.0 / total)
        output.append(line)

        line = "%5s=%22s%8.4f%%%8.4f%%%+9.4f%%" % (
            'P', comma(self.count_player),
            self.count_player * 100.0 / total,
            self.count_player * 100.0 / (self.count_banker + self.count_player),
            (self.count_player - self.count_banker) * 100.0 / total)
        output.append(line)

        line = "%5s=%22s%8.4f%%%8.4fx%+9.4f%%" % (
            'T', comma(self.count_tie),
            self.count_tie * 100.0 / total,
            total * 1.0 / self.count_tie,
            (self.count_tie * 8.0 - self.count_banker - self.count_player) *
            100.0 / total)
        output.append(line)

        line = "total=%22s" % comma(total)
        output.append(line)

        line = " #nat=%22s%8.4f%% T9x%+6.3f%%" % (
            comma(self.count_naturals),
            self.count_naturals * 100.0 / total,
            100.0 * (self.count_tie * (2 + 8.0) - total) / total)
        output.append(line)

        line = "%5s=%22s%8.4f%%%8.4f%%%+9.4f%%" % (
            'EZ-B', comma(self.count_banker - self.count_banker_3card7),
            (self.count_banker - self.count_banker_3card7) * 100.0 / total,
            (self.count_banker - self.count_banker_3card7) * 100.0 /
            (self.count_banker + self.count_player),
            (self.count_banker - self.count_banker_3card7 - self.count_player) *
            100.0 / total)
        output.append(line)

        line = "%5s=%22s%8.4f%%%8.4fx%+9.4f%%" % (
            'B3C7', comma(self.count_banker_3card7),
            self.count_banker_3card7 * 100.0 / total,
            total * 1.0 / self.count_banker_3card7,
            (self.count_banker_3card7 * (1 + 40.0) - total) * 100.0 / total)
        output.append(line)

        line = "%5s=%22s%8.4f%%%8.4fx%+9.4f%%" % (
            'P3C8', comma(self.count_player_3card8),
            self.count_player_3card8 * 100.0 / total,
            total * 1.0 / self.count_player_3card8,
            (self.count_player_3card8 * (1 + 25.0) - total) * 100.0 / total)
        output.append(line)

        for table_num in range(3):  # various dragon tables
            comment = ""
            if table_num == 2:
                comment = "w/T"
            line = "%5s=%22s%8.4f%% %3s     %+9.4f%%" % (
                "DB%d" % (1 + table_num),
                comma(self.count_banker_dragon[table_num]),
                self.freq_banker_dragon[table_num] * 100.0 / total,
                comment,
                self.count_banker_dragon[table_num] * 100.0 / total)
            output.append(line)
        for table_num in range(3):  # various dragon tables
            comment = ""
            if table_num == 2:
                comment = "w/T"
            line = "%5s=%22s%8.4f%% %3s     %+9.4f%%" % (
                "DP%d" % (1 + table_num),
                comma(self.count_player_dragon[table_num]),
                self.freq_player_dragon[table_num] * 100.0 / total,
                comment,
                self.count_player_dragon[table_num] * 100.0 / total)
            output.append(line)

        output.append("%5s=%14s /%15s%8.4fx%+9.4f%%" % (
            'pair', comma(self.count_pair),
            comma(self.count_pair + self.count_nonpair),
            self.count_nonpair * 1.0 / self.count_pair,
            (self.count_pair * 11.0 - self.count_nonpair) * 100.0 /
            (self.count_pair + self.count_nonpair)))

        return "\n".join(output)


if __name__ == "__main__":
    # command line entry point
    ODDS = ComputeBaccaratOdds()
    print(ODDS)
