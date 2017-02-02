#!/usr/bin/env python
#
# hashutils.py - hashing utils
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


import hashlib
import sys


def md5_for_file(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_identical(sourcefile, destfile):
    """Return whether two files are identical"""
    hash_sourcefile = md5_for_file(sourcefile)
    hash_destfile = md5_for_file(destfile)
    return hash_sourcefile == hash_destfile


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print("%s: %s" % (filename, md5_for_file(filename)))
