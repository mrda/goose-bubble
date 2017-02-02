#!/usr/bin/env python
#
# import.py - import image and video files
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

import copyutils
import dirutils
import gblogging
import media
import sys
import os


DEBUG = True

INCOMING = None
SORTED = None
UNSORTED = None


def process_file(directory, filename):
    """Return success or failure"""

    print("Calling process_file for dir=%s, file=%s" % (directory, filename))
    # Find out if they have meta data, find out the year
    #   from when they were created,
    # If no meta data is present, copy them to UNSORTED
    fullpath = os.path.join(directory, filename)
    print "fullpath=%s" % fullpath
    dest_dir = media.get_year_for_image(fullpath)
    print "destdir=%s" % dest_dir
    if (dest_dir == media.NO_YEAR):
        dest_dir = UNSORTED
    else:
        dest_dir = os.path.join(SORTED, dest_dir)

    # Ensure there's a directory to put the copy
    dirutils.ensure_dir(dest_dir)

    # Copy them from INCOMING to SORTED/UNSORTED
    print("We want to copy %s to %s" % (fullpath, dest_dir))
    copy_result = copyutils.copy_file(filename, directory, dest_dir)

    # Log what we did with them
    # and make sure we close the log files afterwards
    if copy_result == copyutils.COPY_STATUS.SUCCEED:
        gblogging.append(gblogging.LOGFILE.SUCCESS, "SUCCESS %s to %s" %
                         (fullname, destdir))
    elif copy_result == copyutils.COPY_STATUS.FAIL:
        gblogging.append(gblogging.LOGFILE.FAIL, "FAILURE %s to %s" %
                         (fullname, destdir))
    elif copy_result == copyutils.COPY_STATUS.DUPLICATE:
        gblogging.append(gblogging.LOGFILE.DUPLICATE, "DUPLICATE %s to %s" %
                         (fullname, destdir))
    else:
        print("*** ERROR processing %s" % fullpath)


def import_files(directory):
    print("Importing from directory %s" % directory)

    gb = gblogging.GbLog()
    gb.open_logs()

    try:

        # Iterate over all files in directories under INCOMING
        for subdir, dirs, files in os.walk(INCOMING):
            print("Entering subdirectory %s" % subdir)
            for f in files:
                try:
                    ret = process_file(gb, subdir, f)
                except:
                    print("Unexpected error processing %s: %s" %
                          (f, sys.exc_info()[0]))
    finally:
        gb.close_logs()


if __name__ == '__main__':

    myname = os.path.basename(sys.argv[0])

    if len(sys.argv) != 2:
        print("%s: [<directory>]" % myname)
        sys.exit(2)

    root_dir = sys.argv[1]

    INCOMING = os.path.join(root_dir, 'incoming')
    UNSORTED = os.path.join(root_dir, 'unsorted')
    SORTED = os.path.join(root_dir, 'sorted')
    DUPLICATES = os.path.join(root_dir, 'duplicates')

    # Ensure there's at least a root and incoming directory already
    if not os.path.isdir(root_dir) or not os.path.isdir(INCOMING):
        sys.exit("%s: Directory %s or %s does not exist. Exiting..." %
                 (myname, root_dir, INCOMING))

    dirutils.ensure_dir(UNSORTED)
    dirutils.ensure_dir(SORTED)

    import_files(root_dir)
