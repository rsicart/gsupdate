#!/usr/bin/env python
# encoding=utf8

from datetime import datetime

date_time = datetime.now()

debug = False

credentials = 'username@gmail.com', 'appPassword'

spreadsheet_key = 'spreadsheet_key_here'

worksheet_id = 'od6' # default value

# appends line at first updateable line beggining from last line
# @see gsupdate.updateRow()
append_end = False

# line: dict of column names and values
# !important rules!:
# * in spreadsheet:
# > ** first row (#1) shoud be 'column names' row
# > ** p.e:    A    | B    | C        | D
# > **      1  Jour | Mois | Arrivé à | Départ à
# * in data dict keys:
# > ** no whitespaces
# > ** lowercase
line = {
	u'name': 'Doge',
	u'email': 'doge@example.com',
	u'creationdate': date_time.strftime('%Y-%m-%d'),
}

# used to decide if a row is updatable
mandatory = [u'name', u'email']
