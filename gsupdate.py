#!/usr/bin/env python
# encoding=utf8

import sys
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
		if elem.custom['name'].text is None:
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


''' Main '''
# auth
client = gdata.spreadsheet.service.SpreadsheetsService()
client.debug = settings.debug
client.ClientLogin(settings.credentials[0], settings.credentials[1])

# spreadsheet selection
spreadsheet_key = settings.spreadsheet_key
worksheet_id = settings.worksheet_id

# data to add
line = settings.line

# get worksheet feed
list_feed = client.GetListFeed(key=spreadsheet_key, wksht_id=worksheet_id) 

count = len(list_feed.entry)
if count == 0:
	insertRow()
	sys.exit(0)

# try to update a row
updated = updateRow(list_feed, True)

# append new line
if not updated:
	insertRow()

sys.exit(0)
