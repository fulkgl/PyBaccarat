#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
#--
import os,sys,unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))[:-6]) #=dev first
from pybaccarat.baccarat import __version__
#--


def readme(filespec):
    '''Utility to return readme contents for long description'''
    with open(filespec) as f:
        return f.read()

setup(
    name='pybaccarat',
    version=__version__, #'0.14',
    url='https://github.com/fulkgl/PyBaccarat',
    download_url='https://pypi.python.org/packages/source/P/pybaccarat/'+\
        'pybaccarat-%s.tar.gz' % __version__,
    description='Play the card game Baccarat',
    long_description=readme('README.md'),
    author='George L Fulk',
    author_email='fulkgl@gmail.com',
    maintainer='George L Fulk',
    maintainer_email='fulkgl@gmail.com',
    license='MIT',
    packages=['pybaccarat'],
    keywords=['baccarat','game','playing cards','cards','card game',],
    scripts=['bin/play_baccarat_interactive.py'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        #Development Status :: 4 - Beta',
        #Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    #entry_points={'console_scripts':['markdown_py = markdown.__main__:run',],},
)
