# Copyright (C) 2018 Philipp Hörist <philipp AT hoerist.com>
#
# This file is part of nbxmpp.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

import logging
import re
import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from datetime import tzinfo

log = logging.getLogger('nbxmpp.m.date_and_time')

PATTERN_DATETIME = re.compile(r'''
    ([0-9]{4}-[0-9]{2}-[0-9]{2})    # Date
    T                               # Separator
    ([0-9]{2}:[0-9]{2}:[0-9]{2})    # Time
    (?P<frac>\.[0-9]{0,6})?         # Fractual Seconds
    [0-9]*                          # lose everything > 6
    (Z|[-+][0-9]{2}:[0-9]{2})       # UTC Offset
    $                               # End of String
''', re.VERBOSE)

ZERO = timedelta(0)
HOUR = timedelta(hours=1)
SECOND = timedelta(seconds=1)

STDOFFSET = timedelta(seconds=-time.timezone)
if time.daylight:
    DSTOFFSET = timedelta(seconds=-time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET


class LocalTimezone(tzinfo):
    '''
    A class capturing the platform's idea of local time.
    May result in wrong values on historical times in
    timezones where UTC offset and/or the DST rules had
    changed in the past.
    '''
    def fromutc(self, dt):
        assert dt.tzinfo is self
        stamp = (dt - datetime(1970, 1, 1, tzinfo=self)) // SECOND
        args = time.localtime(stamp)[:6]
        dst_diff = DSTDIFF // SECOND
        # Detect fold
        fold = (args == time.localtime(stamp - dst_diff))
        return datetime(*args, microsecond=dt.microsecond,
                        tzinfo=self, fold=fold)

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        return ZERO

    def tzname(self, dt):
        return 'local'

    @staticmethod
    def _isdst(dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = time.mktime(tt)
        tt = time.localtime(stamp)
        return tt.tm_isdst > 0


def create_tzinfo(hours=0, minutes=0, tz_string=None):
    if tz_string is None:
        return timezone(timedelta(hours=hours, minutes=minutes))

    if tz_string.lower() == 'z':
        return timezone.utc

    try:
        hours, minutes = map(int, tz_string.split(':'))
    except Exception:
        log.warning('Wrong tz string: %s', tz_string)
        return None

    if hours not in range(-24, 24):
        log.warning('Wrong tz string: %s', tz_string)
        return None

    if minutes not in range(59):
        log.warning('Wrong tz string: %s', tz_string)
        return None

    if hours in (24, -24) and minutes != 0:
        log.warning('Wrong tz string: %s', tz_string)
        return None
    return timezone(timedelta(hours=hours, minutes=minutes))


def parse_datetime(
    timestring: str | None,
    check_utc: bool = False,
    convert: str | None = 'utc',
    epoch: bool = False
) -> datetime | float | None:
    '''
    Parse a XEP-0082 DateTime Profile String

    :param timestring: a XEP-0082 DateTime profile formated string

    :param check_utc:  if True, returns None if timestring is not
                       a timestring expressing UTC

    :param convert:    convert the given timestring to utc or local time

    :param epoch:      if True, returns the time in epoch

    Examples:
    '2017-11-05T01:41:20Z'
    '2017-11-05T01:41:20.123Z'
    '2017-11-05T01:41:20.123+05:00'

    return a datetime or epoch
    '''
    if timestring is None:
        return None
    if convert not in (None, 'utc', 'local'):
        raise TypeError('"%s" is not a valid value for convert')

    match = PATTERN_DATETIME.match(timestring)
    if match is None:
        return None

    timestring = ''.join(match.groups(''))
    strformat = '%Y-%m-%d%H:%M:%S%z'
    if match.group('frac'):
        # Fractional second addendum to Time
        strformat = '%Y-%m-%d%H:%M:%S.%f%z'

    try:
        date_time = datetime.strptime(timestring, strformat)
    except ValueError:
        return None

    if not 1 < date_time.year < 9999:
        # Raise/Reduce MIN/MAX year so converting to different
        # timezones cannot get out of range
        return None

    if check_utc:
        if convert != 'utc':
            raise ValueError(
                'check_utc can only be used with convert="utc"')

        if date_time.tzinfo != timezone.utc:
            return None

        if epoch:
            return date_time.timestamp()
        return date_time

    if convert == 'utc':
        date_time = date_time.astimezone(timezone.utc)
        if epoch:
            return date_time.timestamp()
        return date_time

    if epoch:
        # epoch is always UTC, use convert='utc' or check_utc=True
        raise ValueError(
            'epoch not available while converting to local')

    if convert == 'local':
        date_time = date_time.astimezone(LocalTimezone())
        return date_time

    # convert=None
    return date_time


def get_local_time():
    formated_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    isdst = time.localtime().tm_isdst
    zone = -(time.timezone, time.altzone)[isdst] / 60.0
    zone = (zone / 60, abs(zone % 60))
    tzo = '%+03d:%02d' % zone
    return formated_time, tzo
