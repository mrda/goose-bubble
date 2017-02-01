#!/usr/bin/env python
#
# media.py - image and video manipulation
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
import exifread
import re
import sys
import os

SPLIT_STR = ':| '


def get_date_for_image(filename, only_year=False):
    """Return the date for an image"""
    fd = open(filename, 'rb')
    try:
        tags = exifread.process_file(fd)
    except UnicodeEncodeError:
        print("** Problem processing file '%s'" % filename)
        return None

    if tags is None:
        print("** File '%s' has no exif data") % filename
        return False

    fd.close()

    # DateTimeOriginal
    try:
        datestr = re.split(SPLIT_STR, str(tags['EXIF DateTimeOriginal']))
        if only_year:
            return datestr[0]
        else:
            return datestr
    except KeyError:
        pass

    # DateTime
    try:
        datestr = re.split(SPLIT_STR, str(tags['Image DateTime']))
        if only_year:
            return datestr[0]
        else:
            return datestr
    except KeyError:
        pass

    # DateTimeDigitized
    try:
        datestr = re.split(SPLIT_STR, str(tags['EXIF DateTimeDigitized']))
        if only_year:
            return datestr[0]
        else:
            return datestr
    except KeyError:
        pass

    if only_year:
        return "no-year"
    else:
        return "no-date"


def get_year_for_image(filename):
    return get_date_for_image(filename, only_year=True)


def test_get_date_for_files(directory, all_files=False, only_year=False):
    for subdir, dirs, files in os.walk(directory):
        count = last_count = 0
        exif = ""
        fullpath = ""
        print("Entering subdirectory %s" % subdir)
        for f in files:
            count += 1
            fullpath = os.path.join(subdir, f)
            exif = get_date_for_image(fullpath)
            if (all_files or (count % 1000 == 0)):
                print("-- Examining %dth file %s, exif = %s" %
                      (count, fullpath, exif))
                last_count = count
        if count != last_count:
            print("-- Processing %dth file %s, exif = %s" %
                  (count, fullpath, exif))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("%s: [<files>][<directories>]" % sys.argv[0])
    for elem in sys.argv[1:]:
        if os.path.isfile(elem):
            print("%s: %s" % (elem, get_date_for_image(elem, only_year=False)))
        elif os.path.isdir(elem):
            test_get_date_for_files(elem, all_files=True, only_year=False)
        else:
            print("*** %s isn't a file or directory" % elem)
