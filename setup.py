#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme(filespec):
    '''Utility to return readme contents for long description'''
    with open(filespec) as f:
        return f.read()

setup(
    name='pybaccarat',
    version='0.01',
    packages=['pybaccarat'],
    description='Play the card game Baccarat',
    long_description=readme('README.md'),
    keywords='playing cards game Baccarat',
    author='George L Fulk',
    author_email='fulkgl@gmail.com',
    url='https://github.com/fulkgl/PyBaccarat',
    scripts=[],
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
