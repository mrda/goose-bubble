#!/usr/bin/env python
#
# stats.py - keep some stats
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


class Stats():

    def __init__(self):
        self.total_files = 0
        self.success = 0
        self.unsorted = 0
        self.copy_fail = 0
        self.duplicate = 0
        self.unknown_fail = 0

    def format_stats(self):
        s = "Total files processed: %d\n" % self.total_files
        s += "Successfully sorted files: %d\n" % self.success
        s += "Files left unsorted: %d\n" % self.unsorted
        s += "Duplicate files found: %d\n" % self.duplicate
        s += "Files where copy failed: %d\n" % self.copy_fail
        s += "Unknown failures: %d\n" % self.unknown_fail
        return s
