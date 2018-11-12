# PyBaccarat
Play the card game Baccarat

To check out a copy of the source:
    git clone https://github.com/fulkgl/PyBaccarat.git

This is an implementation of the card game Baccarat. It includes the code
needed to play a game interactively, replay a historical game, or play a
game with a particular system.

This code has been built and tested with these versions:
    Python 2.7.13
    Python 3.6.4

<h1>Updating this code</h1>
<ol compact>
<li>GIT (source control library). Check out a copy of the code.
<br>To keep the origin and structure of the code obvious, I start
with a $BASE (%BASE%) location. It can be a location of your choosing.
Assign an environment variable to define the starting base location:
in Linux <code>export BASE=/home/george</code> or Windows
<code>set BASE=\users\george</code>. Windows will use <code>%BASE%</code>
instead of <code>$BASE</code> and the back-slash for directory
separator instead of forward slash.
</li><ol compact>
<li>mkdir $BASE/github.com/fulkgl</li>
<li>chdir $BASE/github.com/fulkgl</li>
<li>git clone https://github.com/fulkgl/PyBaccarat.git</li>
</ol>

<br>The command <code>git clone https://github.com/fulkgl/PyBaccarat.git</code>
will make a copy of code from a remote host to local system, 
setting up 3 trees (working directory, index, and head). 
What you normally see is the working directory. The index and head
trees are inside the .git directory. And you don't normally look at them.</li>
<br><code>git status</code><BR>Shows you files missing from git and files
that are changed.
<br><code>git diff README.md</code><br>Git diff will show you
changed files differences.
<br><code>git add README.md</code><br>Use the git add
command to move changes from the working directory to the index.
Files that are new to the repo are initially checked in with
the git add command. Files that have been changed are also 
checked in this way. You often use git add one file at a time since
you specify each file with this command. Use "git reset file"
to reverse the effects of a git add command.
<br><code>git commit -m "description"</code><br>Use the git commit 
command to move changes from the index to the head.
You will do this for all the git added files once.
Use "git checkout" to reverse the effects of a git commit.
The description should contain a reference to the defect or feature
number that is addressing this code change.
<br><code>git push origin master</code><br>Use the git push command to 
move changes from the head to the remote host.
<br>git init is used to create a new repo the first time.
Also a git remote add origin is used the first time to
associate a connection to the remote host.</li>
<br><code>browser https://github.com/fulkgl/PyBaccarat</code>
<br>See that the latest things look correct on the webpage.</li>

<li>Clean up temp files.</li>
<ol compact>
<li>del /s/q build dist pybaccarat.egg-info</li>
<li>rmdir /s/q build dist pybaccarat.egg-info</li>
<li>del /s/q tests\*.pyc pybaccarat\*.pyc</li>
<li>rmdir pybaccarat\__pycache__</li>
</ol>
<li>Build the code</li>
<br>python setup.py build bdist sdist
<li>Run the unit tests</li>
<code><pre>
cd %BASE%\github.com\fulkgl\PyBaccarat
python tests\test_card.py
python tests\test_hand.py
python tests\test_scoreboard.py
python tests\test_shoe.py
python tests\test_ties.py
</pre></code>
<!--
<li>Upload changes to PyPi</li>
<br>twine upload dist/* -r legacy
-->
</ol>

<!--
To check the coding standards and minor quality check:
    cd base-location
    <br>pycodestyle pybaccarat\playingcards.py
    <br>pycodestyle pybaccarat\baccarat.py
    <br>pycodestyle pybaccarat\baccaratsystems.py
    <br>pycodestyle bin\play_baccarat.py
    <br>pylint --rcfile=\usr\local\bin\pylint2.rc pybaccarat\playingcards.py
    <br>pylint --rcfile=\usr\local\bin\pylint2.rc pybaccarat\baccarat.py
    <br>pylint --rcfile=\usr\local\bin\pylint2.rc pybaccarat\baccaratsystems.py
    <br>pylint --rcfile=\usr\local\bin\pylint2.rc bin\play_baccarat.py
-->
