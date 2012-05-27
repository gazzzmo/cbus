#!/usr/bin/env python
"""
libcbus/common.py - Constants and common functions used in the CBUS protocol.
Copyright 2012 Michael Farrell <micolous+git@gmail.com>

This library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library.  If not, see <http://www.gnu.org/licenses/>.
"""
from base64 import b16encode, b16decode

HEX_CHARS = "0123456789ABCDEF"

END_COMMAND = '\r\n'

# command types
# TODO: improve this with data from s3.4 of serial interface guide p11/12
POINT_TO_MULTIPOINT = 0x05
POINT_TO_POINT = 0x06
# undocumented command type issued for status inquiries by toolkit?
#POINT_TO_46 = '\\46'

# Applications
APP_LIGHTING = 0x38

# Routing buffer
ROUTING_NONE = 0x00

# lighting application commands.
LIGHT_ON = 0x79
LIGHT_OFF = 0x01
LIGHT_TERMINATE_RAMP = 0x09
# note that 0xA0 - 0xA2 are invalid (minimum label length = 3)
# Lighting Application s2.6.5 p11
LIGHT_LABEL = range(0xA0, 0xC0)

# light on
#\0538007964 (GA 100)

# light off
#\0538000164 (GA 100)

# set to level
#\053800rr64FF (GA 100, to level 100%/0xff)

LIGHT_RAMP_RATES = {
	0x02: 0,
	0x0A: 4,
	0x12: 8,
	0x1A: 12,
	0x22: 20,
	0x2A: 30,
	0x32: 40,
	0x3A: 60,
	0x42: 90,
	0x4A: 120,
	0x52: 180,
	0x5A: 300,
	0x62: 420,
	0x6A: 600,
	0x72: 900,
	0x7A: 1020
}


MIN_RAMP_RATE = 0
MAX_RAMP_RATE = 1020

RECALL = 0x1A
IDENTIFY = 0x21

# these are valid confirmation codes used in acknowledge events.
CONFIRMATION_CODES = 'hijklmnopqrstuvwxyzGHIJKLMNOPQRSTUVWXYZ'

MIN_GROUP_ADDR = 0
MAX_GROUP_ADDR = 255

def duration_to_ramp_rate(seconds):
	for k, v in LIGHT_RAMP_RATES.iteritems():
		if seconds <= v:
			return k
	raise ValueError, 'That duration is too long!'

def ramp_rate_to_duration(rate):
	assert len(rate) == 2, "Ramp rate must be two characters."
	rate = rate.upper()	
	return LIGHT_RAMP_RATES[rate]

def cbus_checksum(i, b16=False):
	"""
	Calculates the checksum of a C-Bus command string.
	
	Fun fact: C-Bus toolkit and C-Gate do not use commands with checksums.
	"""
	if b16:
		if i[0] == '\\':
			i = i[1:]
		
		i = b16decode(i)
	
	c = 0
	for x in i:
		c += ord(x)
	
	return ((c % 0x100) ^ 0xff) + 1

def add_cbus_checksum(i):
	c = cbus_checksum(i)
	return i + chr(c)
	
def validate_cbus_checksum(i):
	c = i[-2:]
	d = i[:-2]
	
	cc = cbus_checksum(c, b16=True)
	
	return c == cc

def validate_ga(group_addr):
	"""
	Validates a given group address to verify that it is valid.
	
	:param group_addr: Input group address to validate.
	:type group_addr: int
	
	:returns: True if the given group address is valid, False otherwise.
	:rtype: bool
	
	"""
	return MIN_GROUP_ADDR <= group_addr <= MAX_GROUP_ADDR

def validate_ramp_rate(duration):
	return MIN_RAMP_RATE <= duration <= MAX_RAMP_RATE

