# PyBaccarat
Play the card game Baccarat

To check out a copy of the source:
    cd base-location
    git clone https://github.com/fulkgl/PyBaccarat.git

Run each of the following with:
    Python 2.7.13

Run unit tests:
    cd base-location
    <br>python tests\unittest_card.py
    <br>python tests\unittest_shoe.py
    <br>python tests\unittest_hand.py
    <br>python tests\unittest_scoreboard.py

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

To run the build and make distribution packages:
    cd base-location
    <br>python setup.py sdist bdist_egg
    <br>rem dist/* contains source and binary distribution packages

<h2>Updating this code</h2>
<ol compact>
<li>Clean up temp files.</li>
<ol compact>
<li>del /s/q build dist pybaccarat.egg-info</li>
<li>rmdir /s/q build dist pybaccarat.egg-info</li>
<li>del /s/q tests\*.pyc pybaccarat\*.pyc</li>
</ol>
<li>Check for updates to git.</li>
<ol compact>
<li>GIT education</li>
<li><B>git clone username@host:/path/to/repository</B>
<BR>This will make a copy of code from a remote host to local, 
setting up 3 trees (working directory, index, and head). 
What you normally see is the working directory. The index and head
trees are in the .git directory.</li>
<li><b>git status</b><BR>Shows you files missing from git and files
that are changed.</li>
<li><b>git diff README.md</B><br>Git diff will show you
changed files differences.
<li><b>git add README.md</b><br>Use the git add
command to move changes from the working directory to the index.
Files that are new from the repo are initially checked in with
the git add command. Files that have been changed are also 
check in this way. You often use git add one file at a time since
you specify each file with this command.</li>
<li><b>git commit -m "description"</b><br>Use the git commit 
command to move changes from the index to the head.
You will do this for all the git added files once.</li>
<li><b>git push ?</b><br>Use the git push command to 
move changes from the head to
the remote host.</li>
<li>git init is used to create a new repo the first time</li>
</ol>
<ol compact>
<li>git status</li>
<li>git add bin\interactive.py and other missing files</li>
<li>git diff README.md to check changes</li>
<li>git add README.md to check in changes</li>
</ol>
<li>check in code to git. git add done above.</li>
<li>update PiPy</li>
<li>build, test, install</li>
@rem python setup.py build bdist sdist upload
</ol>
