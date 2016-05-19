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

def main():
    while True:
        tokens = raw_input('>> ').split(' ')

        if tokens[0] == 'hello':
            print("Well, hello there!")

        elif tokens[0] == 'help':
            progname = os.path.basename(__file__)
            sys.exit('Usage: %s <command>, where <command> is one of:\n'
                     '  hello     - say hello\n'
                     '  help      - display this text\n'
                     '  quit|exit - exit\n'
                     % progname)

        elif tokens[0] in ['quit', 'exit']:
            sys.exit(0)

        else:
            print('Unknown command')


if __name__ == '__main__':
    main()
