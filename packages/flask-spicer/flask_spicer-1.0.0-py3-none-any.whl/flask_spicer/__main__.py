from sys import argv
argc:int = len(argv)

from .cli import run

run(argc,argv)