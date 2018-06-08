#!/usr/bin/python

#import sys
#from msvcrt import getch
import msvcrt
import pybaccarat.playingcards
import pybaccarat.baccarat
import pybaccarat.baccaratsystems

print("interactive play a normal single game of baccarat")
shoe = pybaccarat.playingcards.Shoe(8)
player = pybaccarat.baccarat.Hand()
banker = pybaccarat.baccarat.Hand()
systemplay = pybaccarat.baccaratsystems.interactive()
game = pybaccarat.baccarat.Game(shoe, player, banker, systemplay)
game.play(interactive=False)
