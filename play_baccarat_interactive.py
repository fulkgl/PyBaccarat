#!/usr/bin/python

import argparse
from pybaccarat.playingcards import Shoe
from pybaccarat.baccarat import Game
from pybaccarat.baccaratsystems import Interactive, JustBoards


def just_boards():
    print("*** JustBoards ***")
    shoe = Shoe(8)
    shoe.shuffle()
    Game(shoe=shoe, system=JustBoards()).play()

def play(shoe=None):
    print("Interactive play a normal single game of baccarat.")
    print("Press the P key for player, B for banker, Ctrl-C for fast exit.")
    print("Press ESC to skip to the end of the shoe. Spacebar for no bet hand.")
    print("Press 1 through 5 then P or B to specify the P or B size.")
    print("")
    Game(shoe=shoe, system=Interactive()).play()

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    # command line entry point

    parser = argparse.ArgumentParser("Play a game of Baccarat interactively")
    parser.add_argument("--create", dest="create_filespec",
        help="instead of playing just create and save a random shoe")
    parser.add_argument("--use", dest="use_filespec",
        help="use a saved shoe instead of random generation")
    parser.add_argument("--just_boards", type=str2bool, nargs='?', const=True,
        default=False,
        help="Just use the program to display board results")
    args = parser.parse_args()

    if args.use_filespec is not None:
        if args.create_filespec is not None:
            raise ValueError("can not use both --create and --use at same time")
        # --use creates an empty shoe, then fill from a saved file
        shoe = Shoe(0)
        shoe.load_shoe(args.use_filespec)
        play(shoe)
    else:
        # generate a new random shoe
        if args.create_filespec is not None:
            shoe = Shoe(8)
            shoe.shuffle()
            # --create saves the new shoe and exists
            shoe.save_shoe(args.create_filespec)
            shoe = None
        else:
            if args.just_boards:
                just_boards()
            else:
                play()

# END #
