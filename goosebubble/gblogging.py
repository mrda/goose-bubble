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


class LOGFILE():
    SUCCESS = 1
    FAIL = 2
    DUPLICATE = 3

    def __init__(self, Type):
        self.value = Type

    def __str__(self):
        if self.value == COPY_STATUS.SUCCEES:
            return 'SUCCESS'
        if self.value == COPY_STATUS.FAIL:
            return 'FAIL'
        if self.value == COPY_STATUS.DUPLICATE:
            return 'DUPLICATE'

    def __eq__(self, y):
        return self.value == y.value


class GbLog():

    def __init__(self):
        self._success_fd = None
        self._fail_fd = None
        self._duplicate_fd = None

    def open_logs(self):
        datestr = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
        if self._success_fd is None:
            self._success_fd = open("gb-success-log-%s" % datestr, 'a+')

        if self._fail_fd is None:
            self._fail_fd = open("gb-fail-log-%s" % datestr, 'a+')

        if self._duplicate_fd is None:
            self._duplicate_fd = open("gb-duplicate-log-%s" % datestr, 'a+')

    def append(self, logfile, text):
        if logfile == LOGFILE.SUCCESS:
            self._success_fd.write(text)
        elif logfile == LOGFILE.FAIL:
            self._fail_fd.write(text)
        elif logfile == LOGFILE.DUPLICATE:
            self._duplicate_fd.write(text)

    def close_logs(self):
        self._success_fd.close()
        self._fail_fd.close()
        self._duplicate_fd.close()

