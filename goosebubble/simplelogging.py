#!/usr/bin/env python
#
# logging - naive logging
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

import datetime

import consts


class SimpleLogger():

    def __init__(self):
        self._success_fd = None
        self._fail_fd = None
        self._duplicate_fd = None

    def open_logs(self):
        datestr = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
        if self._success_fd is None:
            self._success_fd = open("gb-success-%s.log" % datestr, 'a+')

        if self._fail_fd is None:
            self._fail_fd = open("gb-fail-%s.log" % datestr, 'a+')

        if self._duplicate_fd is None:
            self._duplicate_fd = open("gb-duplicate-%s.log" % datestr, 'a+')

    def append(self, logfile, text):
        if logfile == consts.SUCCESS:
            self._success_fd.write(text + "\n")
        elif logfile == consts.FAIL:
            self._fail_fd.write(text + "\n")
        elif logfile == consts.DUPLICATE:
            self._duplicate_fd.write(text + "\n")

    def close_logs(self):
        self._success_fd.close()
        self._fail_fd.close()
        self._duplicate_fd.close()
