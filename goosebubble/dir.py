#!/usr/bin/env python
#
# dir.py - directory operations for goose-bubble
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

import media

import exifread
import fnmatch
import os
import sys


UNSORTED_DIR = ['unsorted/']

YEAR_DIRS = [ str(1970+i) for i in range(75) ]


def move_files(directories, exclude_dirs, exts, files_only, func):
    matches = []
    extensions = []
    for ex in exts:
        extensions.append(ex)
        extensions.append(ex.upper())

    for directory in directories:
        for root, dirnames, filenames in os.walk(directory, topdown=True):
            # TODO(mrda): Debugging issue here
            if 'firefox32.png' in filenames:
                print "***** firefox32.png"
                print root
                print filenames
                print dirnames
            prune = False
            for excl_dir in exclude_dirs:
                if excl_dir in dirnames:
                    dirnames.remove(excl_dir)
                    prune = True
            if not prune:
                for extension in extensions:
                    for filename in filenames:
                        if fnmatch.fnmatchcase(filename, '*.'+extension):
                            if files_only:
                                result = filename
                            else:
                                result = (root, filename)
                            func(directory + filename)


def _move_file(filename):
    d = media.get_date_for_image_file(filename)
    if d is None or d is False:
        print("Move file '%s' to unknown" % filename)
    else:
        print("Move file '%s' to directory '%s'" % (filename, d))


if __name__ == '__main__':

    # Note(mrda): This is temporary until integration with shell.py
    move_files(UNSORTED_DIR, YEAR_DIRS, DEFAULT_EXTENSIONS, False, _move_file)
