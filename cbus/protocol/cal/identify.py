#!/usr/bin/env python
# cbus/protocol/cal/identify.py - Identify unit
# Copyright 2013 Michael Farrell <micolous+git@gmail.com>
# 
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

from cbus.common import *
from struct import unpack, pack
import warnings

__all__ = [
	'IdentifyCAL',
]



class IdentifyCAL(object):
	"""
	Identify cal
	"""
	
	def __init__(self, packet, attribute):
		self.packet = packet
		self.attribute = attribute
	
	@classmethod
	def decode_cal(cls, data, packet):
		"""
		Decodes identify SAL.
		"""
		
		cal = IdentifyCAL(packet, ord(data[1]))
		
		data = data[2:]
		return data, cal
	
	def encode(self):
		assert (0 <= self.attribute <= 255), 'attribute must be in range 0..255'
		return [CAL_REQ_IDENTIFY, self.attribute]
		
	def __repr__(self): # pragma: no cover
		return '<%s object: attribute=%r>' % (
			self.__class__.__name__,
			self.attribute
		)




