#!/usr/bin/env python
# encoding=utf8

import sys, getopt, re
import settings
import gdata.spreadsheet.service

def printElem(elem):
	''' For debugging purposes '''
	print 'Author: %s' % elem.author
	print 'Category: %s' % elem.category
	print 'Content: %s' % elem.content
	print 'Contrib: %s' % elem.contributor
	print 'id: %s' % elem.id
	print 'Link: %s' % elem.link
	print 'Published: %s' % elem.published
	print 'Rights: %s' % elem.rights
	print 'Source: %s' % elem.source
	print 'Summary: %s' % elem.summary
	print 'Control: %s' % elem.control
	print 'Title: %s' % elem.title
	print 'Updated: %s' % elem.updated
	print 'Custom: %s' % elem.custom
	print 'text: %s' % elem.text

def getRowId(row):
	''' Returns a row id
		@param string row is an URL with the last part of the path being the row id
	'''
	results = row.split('/')
	return results[-1] # last element

def isUpdateable(custom):
    updateable = True
    for field in settings.mandatory:
        if custom[field].text is None or custom[field].text == '':
            updateable = updateable and True
        else:
            updateable = updateable and False
    return updateable


def insertRow():
	''' Appends a line to the document
	'''
	entry = client.InsertRow(line, spreadsheet_key, worksheet_id)
	if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
		print "Insert row succeeded."
		sys.exit(0)
	else:
		print "Insert row failed."
		sys.exit(1)

def updateRow(listFeed, reverse=False):
	''' Updates a row from the document
		@param listFeed worksheet feed of type SpreadsheetsListFeed
		@param reverse if True, updates the last empty line available (otherwise the first)
		@returns boolean
	'''
	count = len(listFeed.entry)-1
	if reverse:
		iterable = range(count, 0, -1)
	else:
		iterable = range(0, count)

	#find an empty row to update (in case that document contains empty rows in the middle or end)
	row = None
	for i in iterable:
		elem = listFeed.entry[i]
		if isUpdateable(elem.custom):
			row = getRowId(listFeed.entry[i].id.text)
			listFeed = client.GetListFeed(key=spreadsheet_key, wksht_id=worksheet_id, row_id=row)
			entry = client.UpdateRow(listFeed, line)
			if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
				print "Update row succeeded."
				sys.exit(0)
			else:
				print "Update row failed."		
				sys.exit(1)

	return False

def checkTime(time):
    return time if re.match('[0-9]{2}:[0-9]{2}', time) is not None else None


def usage():
    print "python gsupdate.py -r [-t hh:mm]"
    print "Options:"
    print " -r: run"
    print " -t: time in format hh:mm"



if __name__ == '__main__':

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'rt:')
    except getopt.GetoptError as err:
        usage()
        sys.exit(1)

    options = {
        'run': False,
        'time': None
    }

    for opt, value in optlist:
        if opt == '-r':
            options['run'] = True
        elif opt == '-t':
            options['time'] = checkTime(value)

    if 'run' not in options.keys() or options['run'] is False:
        print "Argument -r (for run) is mandatory!"
        usage()
        sys.exit(1)



    ''' Main '''
    # auth
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.debug = settings.debug
    client.ClientLogin(settings.credentials[0], settings.credentials[1])

    # spreadsheet selection
    spreadsheet_key = settings.spreadsheet_key
    worksheet_id = settings.worksheet_id

    # default data to add
    line = settings.line

    # data overwrite
    for k, v in options.items():
        if k in settings.mapping:
            line[settings.mapping[k]] = v

    # get worksheet feed
    list_feed = client.GetListFeed(key=spreadsheet_key, wksht_id=worksheet_id)

    count = len(list_feed.entry)
    if count == 0:
            insertRow()
            sys.exit(0)

    # try to update a row
    updated = updateRow(list_feed, settings.append_end)

    # append new line
    if not updated:
            insertRow()

    sys.exit(0)
