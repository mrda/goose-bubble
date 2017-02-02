#!/usr/bin/env python
#
# copyutils.py - copying utils
#
# Copyright (C) 2017 Michael Davies <michael@the-davies.net>
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

import enum
import hashutils
import shutil
import sys
import os


class COPY_STATUS():
    SUCCEED = 1
    FAIL = 2
    DUPLICATE = 3

    def __init__(self, Type):
        self.value = Type

    def __str__(self):
        if self.value == COPY_STATUS.SUCCEED:
            return 'SUCCEED'
        if self.value == COPY_STATUS.FAIL:
            return 'FAIL'
        if self.value == COPY_STATUS.DUPLICATE:
            return 'DUPLICATE'

    def __eq__(self, y):
        return self.value == y.value


def generate_unique_filename(filename, destdir):
    # Assuming filename already exists in destdir
    # but we'll handle it if it isn't
    fullpath = os.path.join(destdir, filename)
    if not os.path.exists(fullpath):
        return filename

    filename, file_extension = os.path.splitext(filename)
    return filename+'-dup'+file_extension


def copy_file(filename, sourcedir, destdir, debug=False):
    # Does filename exist in destdir?
    sourcefullpath = os.path.join(sourcedir, filename)
    destfullpath = os.path.join(destdir, filename)
    if os.path.exists(destfullpath):
        # Are the files the same?
        if hashutils.is_identical(sourcefullpath, destfullpath):
            return COPY_STATUS(COPY_STATUS.DUPLICATE)
        else:
            # Not duplicate, so fail for now
            # TODO(mrda): copy in the file with a different name if the
            # file contents isn't the same
            return COPY_STATUS(COPY_STATUS.FAIL)
    else:
        # Doesn't exist, so copy
        try:
            if debug:
                print("Copying %s to %s" % (sourcefullpath, destfullpath))
            shutil.copy2(sourcefullpath, destfullpath)
        except IOError, e:
            if debug:
                print "Unable to copy file. %s" % e
            return COPY_STATUS(COPY_STATUS.FAIL)
    return COPY_STATUS(COPY_STATUS.SUCCEED)


if __name__ == '__main__':
    print("Return status is %s" %
          str(copy_file(sys.argv[1], sys.argv[2], sys.argv[3])))
