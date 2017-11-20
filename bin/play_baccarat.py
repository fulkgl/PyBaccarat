#!/usr/bin/python

import playingcards
import baccarat

print("play a normal single game of baccarat")
shoe = playingcards.Shoe(8)
player = baccarat.Hand()
banker = baccarat.Hand()
game = baccarat.Game(shoe, player, banker)
game.play()
