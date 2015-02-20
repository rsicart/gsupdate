#!/usr/bin/env python
# encoding=utf8

from datetime import datetime

date_time = datetime.now()

debug = False

credentials = 'username@gmail.com', 'appPassword'

spreadsheet_key = 'spreadsheet_key_here'

worksheet_id = 'od6' # default value

line = {
	'name': 'Doge',
	'email': 'doge@example.com',
	'creationdate': date_time.strftime('%Y-%m-%d'),
}
