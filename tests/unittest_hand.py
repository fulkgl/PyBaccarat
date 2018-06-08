#!/usr/bin/python

'''
Unit test for the baccarat.Hand class.
'''
import unittest

from pybaccarat.baccarat import Hand
from pybaccarat.playingcards import Card,Shoe


class TestHand(unittest.TestCase):
    '''
    Unit test for the baccarat.Hand class.
    '''
    def test_constructor(self):
        '''
        test hand construction
        '''

        # good value
        player = Hand()
        self.assertIsNotNone(player, "normal")

        # bad
        # anything to test?

    def test_empty(self):
        '''
        test empty method
        '''
        player = Hand()
        player.empty()

    def test_add(self):
        '''
        add(card)
        '''
        player = Hand()
        card6s = Card(6, 's')
        self.assertEqual(0, player.value(), "no cards value 0")
        self.assertEqual("[]", str(player), "no cards")

        player.add(card6s)
        self.assertEqual(6, player.value(), "1 six = 6 value")
        self.assertEqual("[6s]", str(player), "add 6s")

        player.add(card6s)
        self.assertEqual(2, player.value(), "2 sixes = 2 value")
        self.assertEqual("[6s,6s]", str(player), "2 cards")

        player.add(card6s)
        self.assertEqual(8, player.value(), "3 sixes = 8 value")
        self.assertEqual("[6s,6s,6s]", str(player), "3 cards")

        # add an illegal 4th card
        expected = "too many cards in hand, can not add more"
        try:
            player.add(card6s)
            self.fail("should have failed adding 4th card")
        except ValueError as ex:
            self.assertEqual(expected, str(ex), "adding 4th card")

    def test_value(self):
        pass

    def test_need_hit(self):
        '''
        need_hit()
        need_hit(player)
        '''
        player = Hand()
        banker = Hand()
        card6s = Card(6, 's')
        card7h = Card(7, 'h')
        cardAd = Card(1, 'd')

        # normal player hit uses other=None
        player.add(card6s)
        player.add(card7h)
        self.assertTrue(player.need_hit(None), 'player 6+7 needs a hit')

        player.empty()
        player.add(card6s)
        player.add(cardAd)
        self.assertFalse(player.need_hit(None), 'player 6+A no hit')

        # normal banker must pass other=player
        player.empty()
        banker.empty()
        player.add(card6s)
        player.add(cardAd)
        banker.add(card6s)
        banker.add(card6s)
        self.assertTrue(banker.need_hit(player),
                        'banker 6+6 v player 6+A; hit')

        player.empty()
        banker.empty()
        player.add(card6s)
        player.add(card7h)
        player.add(cardAd)
        banker.add(card7h)
        banker.add(card7h)
        self.assertFalse(banker.need_hit(player), 'banker 4 v. P6+7+1; no hit')

        player.empty()
        banker.empty()
        player.add(card6s)
        player.add(card7h)
        player.add(cardAd)
        banker.add(card7h)
        banker.add(card6s)
        self.assertTrue(banker.need_hit(player), 'banker 3 v. P6+7+1; hit')

    def test_get_card(self):
        '''
        get_card(int)
        '''
        player = Hand()

        self.assertIsNone(player.get_card(0), 'empty hand')
        card6s = Card(6, 's')
        card7h = Card(7, 'h')
        cardAd = Card(1, 'd')
        player.add(card6s)
        player.add(card7h)
        player.add(cardAd)
        returned_card = player.get_card(2)
        self.assertEqual(1, returned_card.get_rank(), 'get back Ad')

    def test_str(self):
        pass


#
# Command line entry point
#
if __name__ == '__main__':
    unittest.main()
