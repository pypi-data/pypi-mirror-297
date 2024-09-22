#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  c1219/access/log.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#  This library contains classes to facilitate retreiving complex C1219
#  tables from a target device.  Each parser expects to be passed a
#  connection object.  Right now the connection object is a
#  c1218.connection.Connection instance, but anythin implementing the basic
#  methods should work.

from __future__ import unicode_literals

import struct

from c1219.constants import *
from c1219.data import get_history_entry_record
from c1219.errors import C1219ParseError

class C1219LogAccess(object):  # Corresponds To Decade 7x
	"""
	This class provides generic access to the log data tables that are
	stored in the decade 7x tables.
	"""
	def __init__(self, conn):
		"""
		Initializes a new instance of the class and reads tables from the
		corresponding decades to populate information.

		@type conn: c1218.connection.Connection
		@param conn: The driver to be used for interacting with the
		necessary tables.
		"""
		self.conn = conn
		general_config_table = self.conn.get_table_data(GEN_CONFIG_TBL)
		actual_log_table = self.conn.get_table_data(ACT_LOG_TBL)
		history_log_data_table = self.conn.get_table_data(HISTORY_LOG_DATA_TBL)

		if len(general_config_table) < 19:
			raise C1219ParseError('expected to read more data from GEN_CONFIG_TBL', GEN_CONFIG_TBL)
		if len(actual_log_table) < 9:
			raise C1219ParseError('expected to read more data from ACT_LOG_TBL', ACT_LOG_TBL)
		if len(history_log_data_table) < 11:
			raise C1219ParseError('expected to read more data from HISTORY_LOG_DATA_TBL', HISTORY_LOG_DATA_TBL)

		### Parse GEN_CONFIG_TBL ###
		tm_format = general_config_table[1] & 7
		std_version_no = general_config_table[11]
		std_revision_no = general_config_table[12]

		### Parse ACT_LOG_TBL ###
		log_flags = actual_log_table[0]
		event_number_flag = bool(log_flags & 1)
		hist_date_time_flag = bool(log_flags & 2)
		hist_seq_nbr_flag = bool(log_flags & 4)
		hist_inhibit_ovf_flag = bool(log_flags & 8)
		event_inhibit_ovf_flag = bool(log_flags & 16)
		nbr_std_events = actual_log_table[1]
		nbr_mfg_events = actual_log_table[2]
		hist_data_length = actual_log_table[3]
		event_data_length = actual_log_table[4]
		self.__nbr_history_entries__, self._nbr_event_entries = struct.unpack(self.conn.c1219_endian + 'HH', actual_log_table[5:9])
		if std_version_no > 1:
			ext_log_flags = actual_log_table[9]
			nbr_program_tables = struct.unpack(self.conn.c1219_endian + 'H', actual_log_table[10:12])
		else:
			ext_log_flags = None
			nbr_program_tables = None
		### Parse HISTORY_LOG_DATA_TBL ###
		order_flag = history_log_data_table[0] & 1
		overflow_flag = history_log_data_table[0] & 2
		list_type_flag = history_log_data_table[0] & 4
		inhibit_overflow_flag = history_log_data_table[0] & 8
		nbr_valid_entries, last_entry_element, last_entry_seq_num, nbr_unread_entries = struct.unpack(self.conn.c1219_endian + 'HHIH', history_log_data_table[1:11])

		log_data = history_log_data_table[11:]
		size_of_log_rcd = hist_data_length + 4  # hist_data_length + (SIZEOF(USER_ID) + SIZEOF(TABLE_IDB_BFLD))
		if hist_date_time_flag:
			size_of_log_rcd += LTIME_LENGTH[tm_format]
		if event_number_flag:
			size_of_log_rcd += 2
		if hist_seq_nbr_flag:
			size_of_log_rcd += 2

		if len(log_data) != (size_of_log_rcd * self.nbr_history_entries):
			raise C1219ParseError('log data size does not align with expected record size, possibly corrupt', HISTORY_LOG_DATA_TBL)

		entry_idx = 0
		self._logs = []
		while entry_idx < self.nbr_history_entries:
			self._logs.append(get_history_entry_record(self.conn.c1219_endian, hist_date_time_flag, tm_format, event_number_flag, hist_seq_nbr_flag, log_data[:size_of_log_rcd]))
			log_data = log_data[size_of_log_rcd:]
			entry_idx += 1

	@property
	def nbr_event_entries(self):
		return self._nbr_event_entries

	@property
	def nbr_history_entries(self):
		return self.__nbr_history_entries__

	@property
	def logs(self):
		return self._logs
