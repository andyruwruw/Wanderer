from __future__ import with_statement, print_function, unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import input
from builtins import str
from builtins import range
from builtins import object
import sys
import collections
import os.path
import logging
import re
import imp
import argparse
try:
    imp.find_module('simplejson')
    import simplejson as json
except ImportError:
    import json as json
from location import Location
from wand_gamelogic import GameDirector
import pygame_frontend as frontend

sys.py3kwarning = True  #Turn on Python 3 warnings

class WandererGame(object):
    def __init__(self, 
                 startlevel=1,
                 startscreen=None,
                 solution_file=None,
                 size='m'):
        self.gameLogic = GameDirector()
        if not startscreen:
            self.gameLogic.read_new_level_num(
                startlevel)
        else:
            self.gameLogic.read_new_level(
                filename=startscreen,
                solution_file=solution_file)
        self.gameLogic.read_new_level(
            startlevel=startlevel,
            startscreen=startscreen,
            solution_file=solution_file)
        self.frontEnd = frontend.GetFrontEnd(size=size)
        #TODO need to have a loop here where I gather input,
        # feed it to the game logic, call the frontend to update,
    def new_game(self):
        pass



def main(startlevel=1, startscreen=None, debugflag=False):
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--filename", action='store',
                       help="starting screen filename")
    group.add_argument("-l", "--level", type=int, action='store',
                       help="starting screen number", default=1)
    parser.add_argument("-s", "--solution_file", action='store',
                        help="filename for optional external solution entry",
                        default=None)
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Start in debug mode",
                        default=False)
    parser.add_argument("-z", "--size", action='store', 
                        choices=['s', 'm', 'l'],
                        help="Specify size of window",
                        default='m')
    args = parser.parse_args()
    solution_filename = None
    size = 'm'
    if args.filename:
        startscreen = args.filename
    if args.level:
        startlevel = args.level
    if args.solution_file:
        solution_filename = args.solution_file
    if args.size:
        size = args.size
    debugflag = args.debug

    # Set up logging
    # define Handler to write INFO messages or higher to
    # the sys.stderr
    logging.basicConfig(
        level=logging.DEBUG,
        format = '%(module)-7s l:%(lineno)4s %(message)s',
        filename='logfile.txt',
        filemode='w') #'w' mode will overwrite
    logging.basicConfig(level=logging.INFO)
    console = logging.StreamHandler()
    #console.setLevel(logging.INFO)
    console.setLevel(logging.INFO) #Set this back to INFO after done debugging
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger(None).addHandler(console)
    logging.info('Logging turned on')

    if debugflag:
        import doctest
        doctest.testmod()
    else:
        logging.disable(logging.DEBUG)

    try:
        WandererGame(startlevel=startlevel,
                     startscreen=startscreen,
                     solution_file=solution_filename,
                     size=size)
    except:
        logging.error("Error caught at top level", exc_info=sys.exc_info())
    finally:
        err_info = None  #allow garbage collection on the traceback info
        #answer = input("\n\nPress return to exit")


if __name__ == "__main__":
    main()

