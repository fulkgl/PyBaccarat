#!/usr/bin/python

import pybaccarat.baccarat
import pybaccarat.baccaratsystems

print("Interactive play a normal single game of baccarat.")
print("press the P key for player, B for banker, Ctrl-C for fast exit")
print("press ESC to skip to the end of the shoe, spacebar for no bet a hand")
print("press 1 through 5 then P or B to specify the P or B size.")
print("")

pybaccarat.baccarat.Game(system=pybaccarat.baccaratsystems.interactive()).play()
