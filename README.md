# PyBaccarat
Play the card game Baccarat

To check out a copy of the source:
    cd base-location
    git clone https://github.com/fulkgl/PyBaccarat.git

Run each of the following with:
    Python 2.7.13

Run unit tests:
    cd base-location
    python tests\unittest_card.py
    python tests\unittest_shoe.py
    python tests\unittest_hand.py

To check the coding standards and minor quality check:
    cd base-location
    pycodestyle pybaccarat\playingcards.py
    pycodestyle pybaccarat\baccarat.py
    pycodestyle pybaccarat\baccaratsystems.py
    pycodestyle bin\play_baccarat.py
    pylint --rcfile=\usr\local\bin\pylint2.rc pybaccarat\playingcards.py
    pylint --rcfile=\usr\local\bin\pylint2.rc pybaccarat\baccarat.py
    pylint --rcfile=\usr\local\bin\pylint2.rc pybaccarat\baccaratsystems.py
    pylint --rcfile=\usr\local\bin\pylint2.rc bin\play_baccarat.py

To run the build and make distribution packages:
    cd base-location
    python setup.py sdist bdist_egg
    rem dist/* contains source and binary distribution packages

x