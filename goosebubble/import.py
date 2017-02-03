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

import sys
import os

import consts
import copyutils
import dirutils
import simplelogging
import stats
import media


DEBUG = True

INCOMING = None
SORTED = None
UNSORTED = None


s = stats.Stats()


def process_file(log, directory, filename):
    """Return success or failure"""
    s.total_files += 1

    # Find out if they have meta data, find out the year
    #   from when they were created,
    # If no meta data is present, copy them to UNSORTED
    fullname = os.path.join(directory, filename)
    dest_dir = media.get_year_for_image(fullname)
    if dest_dir is None:
        # File errored in some way
        s.unknown_fail += 1
        return
    elif (dest_dir == media.NO_YEAR):
        dest_dir = UNSORTED
    else:
        dest_dir = os.path.join(SORTED, dest_dir)

    # Ensure there's a directory to put the copy
    dirutils.ensure_dir(dest_dir)

    # Copy them from INCOMING to SORTED/UNSORTED
    copy_result = copyutils.copy_file(filename, directory, dest_dir)

    # Log what we did with them
    # and make sure we close the log files afterwards
    if copy_result == consts.SUCCESS:
        log.append(consts.SUCCESS, "SUCCESS %s to %s" %
                   (fullname, dest_dir))
        if dest_dir == UNSORTED:
            s.unsorted += 1
        else:
            s.success += 1

    elif copy_result == consts.FAIL:
        log.append(consts.FAIL, "FAILURE %s to %s" %
                   (fullname, dest_dir))
        s.copy_fail += 1

    elif copy_result == consts.DUPLICATE:
        log.append(consts.DUPLICATE, "DUPLICATE %s to %s" %
                   (fullname, dest_dir))
        s.duplicate += 1
    else:
        print("*** ERROR processing %s" % fullname)
        s.unknown_fail += 1


def import_files(directory):
    if DEBUG:
        print("Importing from directory %s" % directory)

    log = simplelogging.SimpleLogger()
    log.open_logs()

    try:

        # Iterate over all files in directories under INCOMING
        for subdir, dirs, files in os.walk(INCOMING):
            if DEBUG:
                print("Entering subdirectory %s" % subdir)
            for f in files:
                try:
                    process_file(log, subdir, f)
                except:
                    if DEBUG:
                        raise
                    else:
                        print("Unexpected error processing %s: %s" %
                              (f, sys.exc_info()[0]))
    finally:
        log.close_logs()


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

    print(s.format_stats())
