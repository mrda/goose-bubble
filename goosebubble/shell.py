#
# Copyright (C) 2016 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

"""
Command line goose-bubble interface.
A sample invocation is:
    python shell.py
"""

import os
import sys


PROGNAME='goose-bubble'


def hello():
    print("Well, hello there!")


def help():
    help_str = 'Available commands are:\n'

    # Find the longest verb in the menu item for formatting reasons
    longest_key = 0
    for f in menu_jump_table:
        if len(f) > longest_key:
            longest_key = len(f)
    formatter = '%-' + str(longest_key) + 's'

    for f in sorted(menu_jump_table):
        temp = '  ' + formatter + ' - %s\n'
        help_str += temp % (f, menu_jump_table[f][0])
    print(help_str)


def quit():
    sys.exit(0)


menu_jump_table = {
    'hello': ("say hello", hello),
    'help': ("display this text", help),
    'quit': ("exit", quit),
    'exit': ("exit", quit),
}


def main():
    print("Welcome to %s. Type 'help' for instructions." % PROGNAME)
    while True:
        tokens = raw_input('>> ').split(' ')

        action = tokens[0]

        if action in menu_jump_table:
            menu_jump_table[action][1]()
        else:
            print('Unknown command')


if __name__ == '__main__':
    main()
