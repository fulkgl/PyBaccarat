#!/usr/bin/python

"""!
Unit test for the Ties class.

To execute the unit test from base dir location, enter:
@code
python tests\test_ties.py [-v]
python tests\test_ties.py TestTies.test_basic
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
from pybaccarat.baccarat import Ties


class TestTies(unittest.TestCase):
    '''
    Unit test for the Ties class.
    '''

    @unittest.skip("TBD")
    def test_constructor(self):
        '''
        test card construction
        '''
        pass

    def test_post_tt(self):
        t0 = Ties()
        actual = str(t0)
        self.assertEqual("Ties()", actual, "new shoe(%s)"%actual)
        t0.mark("P")
        actual = str(t0)
        self.assertEqual("Ties()", actual, "P(%s)"%actual)
        t0.mark("T")
        actual = str(t0)
        self.assertEqual("Ties(?)", actual, "PT(%s)"%actual)
        t0.mark("T")
        actual = str(t0)
        self.assertEqual("Ties(T?)", actual, "PTT(%s)"%actual)
        t0.mark("P")
        actual = str(t0)
        self.assertEqual("Ties(Ts)", actual, "PTTP(%s)"%actual)
        
    def test_basics(self):
        '''!
        TBD
        '''
        t0 = Ties()
        actual = str(t0)
        self.assertEqual("Ties()", actual, "new shoe(%s)"%actual)
        t0.mark("P")
        actual = str(t0)
        self.assertEqual("Ties()", actual, "P(%s)"%actual)
        t0.mark("T")
        actual = str(t0)
        self.assertEqual("Ties(?)", actual, "PT(%s)"%actual)
        t0.mark("P")
        actual = str(t0)
        self.assertEqual("Ties(s)", actual, "PTP(%s)"%actual)
        t0.mark("T")
        actual = str(t0)
        self.assertEqual("Ties(s?)", actual, "PTPT(%s)"%actual)
        t0.mark("B")
        actual = str(t0)
        self.assertEqual("Ties(sC)", actual, "PTPTB(%s)"%actual)

    def test_first_tie(self):
        t0 = Ties()
        actual = str(t0)
        self.assertEqual("Ties()", actual, "new(%s)"%actual)
        t0.mark("T")
        actual = str(t0)
        self.assertEqual("Ties(X)", actual, "T(%s)"%actual)
        t0.mark("P")
        actual = str(t0)
        self.assertEqual("Ties(X)", actual, "TP(%s)"%actual)

    def test_triple_tie(self):
        '''!
        TBD
        '''
        # first simple "same"
        t0 = Ties()
        t0.mark("P")
        t0.mark("P")
        t0.mark("P")
        t0.mark("B")
        t0.mark("B")
        actual = str(t0)
        self.assertEqual("Ties()", actual, "3p2b(%s)"%actual)
        t0.mark("T")
        actual = str(t0)
        self.assertEqual("Ties(?)", actual, "3p2bT(%s)"%actual)
        t0.mark("B")
        actual = str(t0)
        self.assertEqual("Ties(s)", actual, "3p2bTb(%s)"%actual)
        t0 = None
        # second simple "chop"
        t1 = Ties()
        t1.mark("P")
        t1.mark("P")
        t1.mark("P")
        t1.mark("B")
        t1.mark("B")
        actual = str(t1)
        self.assertEqual("Ties()", actual, "3p2b(%s)"%actual)
        t1.mark("T")
        actual = str(t1)
        self.assertEqual("Ties(?)", actual, "3p2bT(%s)"%actual)
        t1.mark("P")
        actual = str(t1)
        self.assertEqual("Ties(C)", actual, "3p2bTp(%s)"%actual)
        t1 = None
        # third simple tie follow tie
        t2 = Ties()
        t2.mark("P")
        t2.mark("P")
        t2.mark("P")
        t2.mark("B")
        t2.mark("B")
        actual = str(t2)
        self.assertEqual("Ties()", actual, "3p2b(%s)"%actual)
        t2.mark("T")
        actual = str(t2)
        self.assertEqual("Ties(?)", actual, "3p2bT(%s)"%actual)
        t2.mark("T")
        actual = str(t2)
        self.assertEqual("Ties(T?)", actual, "3p2bTT(%s)"%actual)
        t2 = None
        
    @unittest.skip("TBD")
    def test_basics2(self):
        # 1. empty board
        b0 = Scoreboard(0)
        #b0.set_debug()
        empty_board = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(empty_board, actual, "check empty board")

        # 2. simple P mark
        b0.mark('P')
        board1 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(board1, actual, "basic P\n%s"%actual)

        # 3. simple P mark (total PP)
        b0.mark('P')
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(board2, actual, "basic PP\n%s"%actual)

        # 4. PPB total marks
        b0.mark('B')
        board3 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PB                                                            2\n"+\
          "P                                                             1\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(board3, actual, "basic PP B\n%s"%actual)

        # 5. PPBBBBB total marks (up to the 5th row on B)
        b0.mark('B')
        b0.mark('B')
        b0.mark('B')
        b0.mark('B')
        board4 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PB                                                            2\n"+\
          "PB                                                            2\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(board4, actual, "basic 2P 5B\n%s"%actual)

        # 6. 2P 6B up to the 6th row with B's
        b0.mark('B')
        board46 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PB                                                            2\n"+\
          "PB                                                            2\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"
        actual = b0.print_lines()
        self.assertEqual(board46, actual, "basic 2P 6B\n%s"%actual)
        
        # 7. 2P 7B first slide
        b0.mark('B')
        board5 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PB                                                            2\n"+\
          "PB                                                            2\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " BB                                                           1\n"
        actual = b0.print_lines()
        self.assertEqual(board5, actual, "basic PP BBBBBB B\n%s"%actual)
        
        # 7. 2P 8B second slide
        b0.mark('B')
        board6 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PB                                                            2\n"+\
          "PB                                                            2\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " B                                                            1\n"+\
          " BBB                                                          1\n"
        actual = b0.print_lines()
        self.assertEqual(board6, actual, "basic 2P 8B\n%s"%actual)
        # 
        b0.set_debug(False)
    @unittest.skip("TBD")
    def test_extreme_slide(self):
        '''
        test the condition of slide go too far to the right
        '''
        b0 = Scoreboard(0)
        empty_board = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(empty_board, actual, "check empty board")
        # mark 64 straight Players (slide to pre-max)
        #b0.set_debug(True)
        for i in range(64):
            #print("extreme i=%d" % i)
            b0.mark('P')
        b0.set_debug(False)
        board1 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP   1\n"
        actual64 = b0.print_lines()
        self.assertEqual(board1, actual64, "64P, pre-max\n%s"%actual64)
        # mark the 65th player to reach max condition
        b0.mark('P')
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP  1\n"
        self.assertEqual(board2, b0.print_lines(), "65P max")
        # mark the 66th player to exceed max condition
        b0.mark('P')
        board3 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP> 1\n"
        actual = b0.print_lines()
        self.assertEqual(board3, actual, "66P beyond max\n%s"%actual)
    @unittest.skip("TBD")
    def test_9116_slide(self):
        '''
        test a specific slide condition, 9116
        '''
        b0 = Scoreboard(0)
        #b0.set_debug()
        empty_board = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(empty_board, actual, "check empty board")
        # mark 9115
        for i in range(9):
            b0.mark('P')
        b0.mark('B')
        b0.mark('P')
        for i in range(5):
            b0.mark('B')
        board1 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPB                                                          4\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "PPPP                                                          1\n"
        actual = b0.print_lines()
        self.assertEqual(board1, actual, "pre 9116\n%s\n%s"%(actual,board1))
        # now add that 6th B
        b0.mark('B')
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPB                                                          4\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  BB                                                         2\n"+\
          "PPPP                                                          2\n"
        actual = b0.print_lines()
        self.assertEqual(board2, actual, "after 9116\n%s"%actual)
        b0.set_debug(False)
    @unittest.skip("TBD")
    def test_91176_slide(self):
        '''
        test a specific slide condition, 91176
        '''
        b0 = Scoreboard(0)
        empty_board = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(empty_board, actual, "check empty board")
        # mark 9115
        for i in range(9):
            b0.mark('P')
        b0.mark('B')
        b0.mark('P')
        for i in range(5):
            b0.mark('B')
        board1 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPB                                                          4\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "PPPP                                                          1\n"
        actual = b0.print_lines()
        self.assertEqual(board1, actual, "pre 9116\n%s\n%s"%(actual,board1))
        # now add that 6th B
        b0.mark('B')
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPB                                                          4\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  BB                                                         2\n"+\
          "PPPP                                                          2\n"
        actual = b0.print_lines()
        self.assertEqual(board2, actual, "after 9116\n%s"%actual)
        # now add that 7th B
        #b0.set_debug()
        b0.mark('B')
        #b0.set_debug(False)
        board3 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPB                                                          4\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  B                                                          2\n"+\
          "P  BBB                                                        2\n"+\
          "PPPP                                                          2\n"
        actual = b0.print_lines()
        self.assertEqual(board3, actual, "after 9117\n%s"%actual)
        # 4 Ps
        for i in range(4):
            b0.mark('P')
        board4 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPBP                                                         5\n"+\
          "P  BP                                                         3\n"+\
          "P  BP                                                         3\n"+\
          "P  BP                                                         3\n"+\
          "P  BBB                                                        2\n"+\
          "PPPP                                                          2\n"
        actual = b0.print_lines()
        self.assertEqual(board4, actual, "after 91174\n%s"%actual)
        # 5th P
        #b0.set_debug()
        b0.mark('P')
        board5 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPBP                                                         5\n"+\
          "P  BP                                                         3\n"+\
          "P  BP                                                         3\n"+\
          "P  BPP                                                        3\n"+\
          "P  BBB                                                        3\n"+\
          "PPPP                                                          2\n"
        actual = b0.print_lines()
        self.assertEqual(board5, actual, "after 91175\n%s"%actual)
        # 6th P
        b0.mark('P')
        board6 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPBP                                                         5\n"+\
          "P  BP                                                         3\n"+\
          "P  BP                                                         3\n"+\
          "P  BPPP                                                       3\n"+\
          "P  BBB                                                        3\n"+\
          "PPPP                                                          3\n"
        actual = b0.print_lines()
        self.assertEqual(board6, actual, "after 91176\n%s"%actual)
        # 7th P
        b0.mark('P')
        board7 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBPBP                                                         5\n"+\
          "P  BP                                                         3\n"+\
          "P  BP                                                         3\n"+\
          "P  BPPPP                                                      3\n"+\
          "P  BBB                                                        3\n"+\
          "PPPP                                                          3\n"
        actual = b0.print_lines()
        self.assertEqual(board7, actual, "after 91177\n%s"%actual)
    @unittest.skip("TBD")
    def test_same_long_strings(self):
        '''
        test the condition of 2 same type long strings in parallel and
        a possible collision.
        '''
        b0 = Scoreboard(0)
        empty_board = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"+\
          "                                                              0\n"
        actual = b0.print_lines()
        self.assertEqual(empty_board, actual, "check empty board")
        # mark 6 straight P, check the resulting board
        for i in range(6):
            b0.mark('P')
        board1 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"
        self.assertEqual(board1, b0.print_lines(), "after first 6 players")
        for i in range(3):
            b0.mark('P')
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "P                                                             1\n"+\
          "PPPP                                                          1\n"
        self.assertEqual(board2, b0.print_lines(), "after first 9 players")
        b0.mark('B')
        b0.mark('P')
        b0.mark('P')
        b0.mark('P')
        b0.mark('P')
        # B, then 4 P. Pre-collision condition
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBP                                                           3\n"+\
          "P P                                                           2\n"+\
          "P P                                                           2\n"+\
          "P P                                                           2\n"+\
          "P                                                             1\n"+\
          "PPPP                                                          1\n"
        self.assertEqual(board2, b0.print_lines(), "pre-collision condition")
        # run the collision mark
        b0.mark('P')
        board2 = \
          "....v....1....v....2....v....3....v....4....v....5....v....6 R0\n"+\
          "PBP                                                           3\n"+\
          "P P                                                           2\n"+\
          "P P                                                           2\n"+\
          "P P                                                           2\n"+\
          "P P                                                           2\n"+\
          "PP=P                                                          1\n"
        self.assertEqual(board2, b0.print_lines(), "collision")
    @unittest.skip("TBD")
    def test_getarray(self):
        '''
        test get_rank method
        '''
        pass
    @unittest.skip("TBD")
    def test_getseq(self):
        '''
        test getseq() method
        '''
        pass
    @unittest.skip("TBD")
    def test_mark(self):
        '''
        test mark() method
        '''
        pass
    @unittest.skip("TBD")
    def test_get_cs_mark(self):
        '''
        test get_cs_mark() method
        '''
        pass
    @unittest.skip("TBD")
    def test_get_peek_B_array(self):
        pass
    @unittest.skip("TBD")
    def test_print_lines(self):
        pass
    @unittest.skip("don't test inherit yet")
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
        class_actual = str(c5s.__class__)
        self.assertEqual("<class 'pybaccarat.playingcards.Card'>",
                         class_actual,
                         ".class(%s)" % class_actual)
        module_actual = str(c5s.__module__)
        self.assertEqual("pybaccarat.playingcards", module_actual,
                         ".module(%s)" % module_actual)
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
