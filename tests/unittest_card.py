#!/usr/bin/python

"""!
Unit test for the Card class.

To execute the unit test from base dir location, enter:
@code
cd pybaccarat_base
python tests\unittest_card.py [-v]
@endcode
@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
"""
import unittest

from playingcards import Card


class TestCard(unittest.TestCase):
    '''
    Unit test for the Card class.
    '''
    def test_constructor(self):
        '''
        test card construction
        '''

        # simple good value test
        c5s = Card(5, 's')
        self.assertIsNotNone(c5s, "normal 5s")

        # bad rank value
        with self.assertRaises(ValueError):
            cbad = Card(0, 's')  # rank 0
        with self.assertRaises(ValueError):
            cbad = Card(0, 'S')  # upper suit
        with self.assertRaises(ValueError):
            cbad = Card('s', 5)  # swap suit,rank
        with self.assertRaises(ValueError):
            cbad = Card(5, 5)   # 2 ranks
        with self.assertRaises(ValueError):
            cbad = Card('s', 's')  # 2 suits
        with self.assertRaises(ValueError):
            cbad = Card(5, '')  # suit length 0
        with self.assertRaises(ValueError):
            cbad = Card(None, None)  # Null
        cbad = None

        try:
            cbad = Card('s', 5)
            self.fail("s5 should have thrown a ValueError but did not")
        except ValueError as ex:
            self.assertEqual("new_ordinal(s) not an integer", str(ex),
                             "check msg")

        # bad suit value
        with self.assertRaises(ValueError):
            cbad = Card(5, 'Clubs')

        # interate through all legal 52 cards
        count = 0
        for suit in "cdhs":
            for rank in range(1, 14):
                count += 1
                card = Card(rank, suit)
                self.assertIsNotNone(card, "52 legeal cards")
                card = None
        self.assertEqual(52, count, "make sure we did all 52")

        # try some illegal ranks
        illegal = [-1, 0, 14]
        suit = 's'
        for rank in illegal:
            expected = "new_ordinal(%d) not in rank range 1..13" % rank
            try:
                cbad = Card(rank, suit)
                self.fail("bad should have thrown a ValueError but did not")
            except ValueError as ex:
                self.assertEqual(expected, str(ex), "check msg")

    def test_getrank(self):
        '''
        test get_rank method
        '''
        rank = 5
        c5s = Card(rank, 's')
        self.assertEqual(rank, c5s.get_rank(), "rank 5 from card5s")

    def test_getsuit(self):
        '''
        test get_suit method
        '''
        suit = 'h'
        c5h = Card(5, suit)
        self.assertEqual(suit, c5h.get_suit(), "rank h from card5h")

    def test_ordinal(self):
        '''
        test ordinal method
        '''
        c5s = Card(5, 's')
        # spades are 4th suit (3*13) = +39
        # five rank is 5-1 within spades range
        self.assertEqual((39 + 5 - 1), c5s.get_ordinal(), "card5s ordinal")
        # Ac = 0
        # 2c = 1
        # ...
        # Kc = 12
        # Ad = 13
        # ...
        # Ah = 26
        # ...
        # As = 39
        # ...
        # Ks = 51

    def test_tostring(self):
        '''
        test __str__ method
        '''
        c5s = Card(5, 's')
        self.assertEqual('5s', str(c5s), "card5s toString")

    def test_eq(self):
        '''
        test __eq__ method
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        card3 = Card(5, 's')
        class CardChild1(Card):
            pass
        card4 = CardChild1(5, 's')
        card5 = CardChild1(7, 'h')
        card6 = Card(5, 's')

        # test 3 fundamental tests of same class EQ
        self.assertTrue(card1 == card1, "reflexive")
        self.assertTrue(card1 is card1, "same instance")

        self.assertFalse(card1 == card2, "false A==B")
        self.assertFalse(card2 == card1, "false B==A")
        self.assertFalse(card1 is card2, "not same instance 1")
        self.assertFalse(card2 is card1, "not same instance 2")

        self.assertTrue(card1 == card3, "2 diff but same value")
        self.assertTrue(card3 == card1, "opposite of 1==3")
        self.assertTrue(card1 == card6, "transative test1")
        self.assertTrue(card6 == card1, "T test2")
        self.assertTrue(card3 == card6, "T test3")
        self.assertTrue(card6 == card3, "T test4")
        self.assertFalse(card1 is card3, "not same 3")
        self.assertFalse(card1 is card6, "not same 6")
        # basic same class tests done

        # test Card class against a Card subclass
        self.assertTrue(card1 == card4, "child class same value")
        self.assertTrue(card4 == card1, "opp child class same")
        self.assertFalse(card1 == card5, "child class diff value")
        self.assertFalse(card5 == card1, "opp child class diff")
        self.assertFalse(card1 is card4, "not same 4")
        self.assertFalse(card1 is card5, "not same 5")

        # set tests
        set_test = set([card1, card3])
        actual = len(set_test)
        self.assertEqual(1, actual, "card1 and 3 EQ actual(%d)" % actual)
        set_test2 = set([card1, card3, card6])  # card6 is from child class
        actual = len(set_test2)
        self.assertEqual(1, actual, "card1,3,6 actual(%d)" % actual)
        set_test3 = set([card1, card3, card6, card5])
        actual = len(set_test3)
        self.assertEqual(2, actual, "card5 is unique")

    def test_ne(self):
        '''!
        test __ne__ method
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        card3 = Card(5, 's')
        class CardChild1(Card):
            pass
        card4 = CardChild1(5, 's')
        card5 = CardChild1(7, 'h')
        card6 = Card(5, 's')

        # test 3 fundamental tests of same class EQ
        self.assertFalse(card1 != card1, "reflexive")
        self.assertTrue(card1 is card1, "same instance")

        self.assertTrue(card1 != card2, "false A==B")
        self.assertTrue(card2 != card1, "false B==A")
        self.assertFalse(card1 is card2, "not same instance 1")
        self.assertFalse(card2 is card1, "not same instance 2")

        self.assertFalse(card1 != card3, "2 diff but same value")
        self.assertFalse(card3 != card1, "opposite of 1==3")
        self.assertFalse(card1 != card6, "transative test1")
        self.assertFalse(card6 != card1, "T test2")
        self.assertFalse(card3 != card6, "T test3")
        self.assertFalse(card6 != card3, "T test4")
        self.assertFalse(card1 is card3, "not same 3")
        self.assertFalse(card1 is card6, "not same 6")
        # basic same class tests done

        # test Card class against a Card subclass
        self.assertFalse(card1 != card4, "child class same value")
        self.assertFalse(card4 != card1, "opp child class same")
        self.assertTrue(card1 != card5, "child class diff value")
        self.assertTrue(card5 != card1, "opp child class diff")
        self.assertFalse(card1 is card4, "not same 4")
        self.assertFalse(card1 is card5, "not same 5")

    def test_lt(self):
        '''
        __lt__
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        try:
            result = card1 < card2
            self.fail("should not continue")
        except NotImplementedError as ex:
            self.assertEqual("LT does not have meaning, so not permitted",
                             str(ex))

    def test_le(self):
        '''
        __le__
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        try:
            result = card1 <= card2
            self.fail("should not continue")
        except NotImplementedError as ex:
            self.assertEqual("LE does not have meaning, so not permitted",
                             str(ex))

    def test_gt(self):
        '''
        __gt__
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        try:
            result = card1 > card2
            self.fail("should not continue")
        except NotImplementedError as ex:
            self.assertEqual("GT does not have meaning, so not permitted",
                             str(ex))

    def test_ge(self):
        '''
        __ge__
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        try:
            result = card1 >= card2
            self.fail("should not continue")
        except NotImplementedError as ex:
            self.assertEqual("GE does not have meaning, so not permitted",
                             str(ex))

    def test_hash(self):
        '''
        __hash__
        '''
        card1 = Card(5, 's')
        card2 = Card(7, 'h')
        card3 = Card(5, 's')
        h1 = card1.__hash__()
        # print("h1(%s)" % str(h1))
        self.assertTrue(h1 == card3.__hash__(), "card 1 and 3 same value")
        self.assertFalse(h1 == card2.__hash__(), "card 1 and 2 diff")

    def test_inherit(self):
        '''
        inheritted things from object:

        c = playingcards.Card(5,'s')
        dir(c)
        ['__delattr__', '__getattribute__', '__setattr__', '__new__',
        '__dict__', '__dir__', '__format__', '__init_subclass__',
        '__subclasshook__', '__reduce__', '__reduce_ex__', '__weakref__']

        @todo inherit tests
        '''
        # check namespace values
        c5s = Card(5, 's')
        self.assertEqual("<class 'playingcards.Card'>", str(c5s.__class__),
                         "class")
        self.assertEqual("playingcards", c5s.__module__, "module")
        docstring = c5s.__doc__
        self.assertTrue(isinstance(docstring, str), "docstring is string")
        self.assertTrue(0 < len(docstring), "some string of >0 exists")

        # __repr__  (<method-wrapper '__repr__' of Card object at 0x0336FD50>)
        # __sizeof__(<built-in method __sizeof__ of Card object at 0x02A08F70>)

    # @todo usage examples


#
# Command line entry point
#
if __name__ == '__main__':
    unittest.main()
