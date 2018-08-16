#!/usr/bin/python

"""!
Unit test for the Shoe class.

To execute the unit test from base dir location, enter:
@code
python tests\test_shoe.py [-v]
@endcode

    self.assertIsNone(obj, "msg")
    self.assertIsNotNone(obj, "msg")
    self.assertTrue(boolean, "msg")
    self.assertFalse(boolean, "msg")
    self.assertEqual(expect, actual, "msg")
    self.assertNotEqual(expect, actual, "msg")
    with self.assertRaises(ValueError): causes_exception
    self.fail("msg")

@author <A email="fulkgl@gmail.com">fulkgl@gmail.com</A>
"""

import os,sys,unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))[:-6]) #=dev first
from pybaccarat.playingcards import Shoe
from pybaccarat.playingcards import Card


def delete_file(filespec):
    '''!
    Delete a file if it exists.
    @param filespec file to delete
    '''
    if os.path.exists(filespec):
        os.remove(filespec)


class TestShoe(unittest.TestCase):
    '''
    unit test Shoe class
    '''
    def test_constructor(self):
        '''
        Shoe()
        Shoe(8)
        '''
        # test good construction
        try:
            shoe = Shoe(8)
        except Exception as ex:
            self.fail("ex(%s)" % str(ex))
        self.assertIsNotNone(shoe, "not none Shoe(8)")

        # test bad construction
        expected = "number_decks(8) invalid value(8)"
        try:
            shoe = Shoe("8")
            self.fail("expected a failure because of string param")
        except Exception as ex:
            actual = str(ex)
            self.assertEqual(expected, actual, 'msg Shoe("8")(%s)'%actual)

        # default constructor
        shoe = Shoe()
        self.assertIsNotNone(shoe, "default blank shoe exists")

        # custom shoe
        shoe = Shoe([Card(43), Card(44), Card(45)])
        self.assertIsNotNone(shoe, "small custom 3 card shoe exists")

    def test_reset(self):
        '''
        test method reset()
        '''
        shoe = Shoe(8)
        self.assertTrue(shoe.cut_card_seen(), "new shoe cut card 0")
        shoe.set_cut_card(1)
        self.assertFalse(shoe.cut_card_seen(), "new cut card 1")
        shoe.reset()
        self.assertTrue(shoe.cut_card_seen(), "after reset back to 0")

    def test_shuffle(self):
        '''
        test method shuffle()
        '''
        shoe = Shoe(8)
        self.assertEqual("Ac", str(shoe.deal()), "no shuffle Ace clubs first")
        shoe.reset()
        expected_clubs = "Ac2c3c4c5c6c7c8c9cTcJcQcKc"
        cards = ""
        for _ in range(13):
            cards += str(shoe.deal())
        self.assertEqual(expected_clubs, cards, "pre-shuffle")
        shoe.shuffle()
        cards = ""
        for _ in range(13):
            cards += str(shoe.deal())
        self.assertNotEqual(expected_clubs, cards, "post-shuffle")

    def test_set_cut_card(self):
        '''
        test method set_cut_card(int)
        '''
        # good test
        shoe = Shoe(8)
        shoe.set_cut_card(-14)
        # bad test
        # too big
        expected = "cut card position value too big"
        try:
            shoe.set_cut_card(987)
            self.fail("expected failure set_cut_card(987)")
        except Exception as ex:
            self.assertEqual(expected, str(ex), "too big")
        # too small
        expected = "cut card position value too small"
        try:
            shoe.set_cut_card(-987)
            self.fail("expected failure set_cut_card(-987)")
        except Exception as ex:
            self.assertEqual(expected, str(ex), "too small")

    def test_cut_card_seen(self):
        '''!
        test method cut_card_seen()
        '''
        shoe = Shoe(8)
        self.assertTrue(shoe.cut_card_seen(), "new shoe, yes")
        shoe.set_cut_card(1)
        self.assertFalse(shoe.cut_card_seen(), "position 1 no deal, no")
        card1 = shoe.deal()
        self.assertTrue(shoe.cut_card_seen(), "after 1 dealt, then yes")

    def test_deal(self):
        '''!
        test method deal()
        '''
        shoe = Shoe(8)
        card1 = shoe.deal()
        # no shuffle so Ac should start us out
        self.assertEqual("Ac", str(card1), "no shuffle Ac first card")

        # create a short custom shoe to test running out of cards
        shoe2 = Shoe([Card(43), Card(44), Card(45), ])
        # only 3 cards in this shoe2
        card1 = shoe2.deal()
        self.assertIsNotNone(card1, "first of shoe2")
        card1 = shoe2.deal()
        self.assertIsNotNone(card1, "second of shoe2")
        card1 = shoe2.deal()
        self.assertIsNotNone(card1, "third of shoe2")
        card1 = shoe2.deal()
        self.assertIsNone(card1, "fourth of shoe2 (empty)")

    def test_save_shoe(self):
        '''!
        test method save_shoe()
        '''
        shoe = Shoe() #default single deck
        #no shuffle so we can test a simple single deck in order
        temp_file = os.sep + 'tmp' + os.sep + 'ut1.shoe'
        delete_file(temp_file)
        shoe.save_shoe(temp_file)
        expect = "Ac 2c 3c 4c 5c 6c 7c \n"+\
                 "8c 9c Tc Jc Qc \n"+\
                 "Kc Ad 2d 3d 4d \n"+\
                 "5d 6d 7d 8d 9d \n"+\
                 "Td Jd Qd Kd Ah \n"+\
                 "2h 3h 4h 5h 6h \n"+\
                 "7h 8h 9h Th Jh \n"+\
                 "Qh Kh As 2s 3s \n"+\
                 "4s 5s 6s 7s 8s 9s Ts Js Qs Ks \n"
        with open(temp_file, 'r') as f:
            actual = f.read()
        self.assertEqual(expect, actual, "saved single unshuffled deck")

    def test_load_shoe(self):
        pass


#
# Command line entry point
#
if __name__ == '__main__':
    unittest.main()
