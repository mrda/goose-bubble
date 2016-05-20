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


MEDIA_EXTENSIONS = ['jpeg', 'jpg', 'png', 'cr2', 'mov']


def get_date_for_image_file(filename):
    """Return the date for an image"""
    fd = open(filename, 'rb')
    try:
        tags = exifread.process_file(fd)
    except UnicodeEncodeError:
        print("*** Problem processing file '%s'" % filename)
        return None

    if tags is None:
        print("*** File '%s' has no exif data") % filename
        return False

    fd.close()

    # DateTimeOriginal
    try:
        return str(tags['EXIF DateTimeOriginal']).split(':')[0]
    except KeyError:
        pass

    # DateTime
    try:
        return str(tags['Image DateTime']).split(':')[0]
    except KeyError:
        pass

    # DateTimeDigitized
    try:
        return str(tags['EXIF DateTimeDigitized']).split(':')[0]
    except KeyError:
        pass

    return False


if __name__ == '__main__':
    # TODO(mrda): Provide some standalone parsing here
    pass
