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

MEDIA_TYPES = ['jpg', 'png', 'cr2', 'mov']

INCOMING = None
SORTED = None
UNSORTED = None
BACKUP = None
DUPLICATES = None

DEBUG = False


def import(source_dir, dest_dir, cannot_sort_dir, file_types):
    move_files(source_dir, None, dest_dir, cannot_sort_dir, file_types,
               False)


def move_files(directories, exclude_dirs, dest_dir, cannot_sort_dir, exts,
               files_only):
    """Sort and move files from one place to another
       directories - 
       exclude_dirs -
       dest_dir -
       cannot_sort_dir -
       exts -
       files_only -
    """
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
                            move_single_file(directory + filename, dest_dir,
                                 cannot_sort_dir)


def move_single_file(filename, dest_dir, cannot_sort_dir):
    d = media.get_date_for_image_file(filename)
    if d is None or d is False:
        print("Move file '%s' to unknown" % filename)
        # TODO(mrda): Move file to cannot_sort_dir directory
    else:
        print("Move file '%s' to directory '%s'" % (filename, d))
        # TODO(mrda): Move file to dest_dir directory
        # Well, actually dest_dir/year so ensure_dir(dest_dir + d['year'])


def ensure_dir(path):
    if DEBUG:
        print "Asked to make \"" + path + "\""
    if not os.path.exists(path):
        os.makedirs(path)


def ensure_gb_dirs():
    try:
        root_dir = os.environ.get('GB_MEDIA')
        if root_dir is None:
            root_dir = os.environ['HOME'] + os.sep + 'media'
        # Fix ~'s
        root_dir = os.path.expanduser(root_dir)

        INCOMING = root_dir + os.sep + 'incoming'
        UNSORTED = root_dir + os.sep + 'unsorted'
        SORTED = root_dir + os.sep + 'sorted'
        BACKUP = root_dir + os.sep + 'backup'
        DUPLICATES = root_dir + os.sep + 'duplicates'

        ensure_dir(root_dir)
        ensure_dir(INCOMING)
        ensure_dir(UNSORTED)
        ensure_dir(SORTED)
        ensure_dir(BACKUP)
        ensure_dir(DUPLICATES)
        return True

    except Exception as e:
        print "Unexpected error: ", sys.exc_info()[0]
        return False


if __name__ == '__main__':

    # Note(mrda): This is temporary until integration with shell.py
    move_files(UNSORTED_DIR, YEAR_DIRS, DEFAULT_EXTENSIONS, False, _move_file)
