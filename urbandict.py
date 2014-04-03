#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import urllib
import argparse
from httplib2 import Http
from colorama import Fore, Back, Style

# API
##############################################################################
# This tools uses the API http://api.urbandictionary.com/v0/define?term=$TERM

class urbandict(object):
	"""
	Class that allows the API interaction with the one and only famous urbandictionary.
	"""

	def __init__(self):
		""" 
		Constructor
		"""
		self.CHARSET = "utf-8"
		self.SERVER_RESPONSES = {
			200: 'ok', 
			304: 'not modified', 
			400: 'bad request', 
			403: 'forbidden',  
			404: 'not found', 
			406: 'not acceptable', 
			500: 'internal server error', 
			502: 'bad gateway', 
			503: 'service unavailable', 
			504: 'gateway timeout'
		}

	def getServerResponse(self, number):
		"""
		Converts a server response into a human readable format.
		"""
	    
		for key, value in self.SERVER_RESPONSES.iteritems():
			if key == int(number):
				return value

		raise ValueError("The server response with ID %i is unknown." % int(number))

	def findDefinition(self, definition_search_key):
		"""
		Searches a given string on the legendary urbandictionary. Returns the JSON raw result of the query. If something goes wrong this method raises an RuntimeError.
		"""
		h = Http()
    		resp, content = h.request("http://api.urbandictionary.com/v0/define?term=%s" % urllib.quote_plus(definition_search_key), "GET")

		try:
			if self.getServerResponse(resp['status']) != self.SERVER_RESPONSES[200]:
				raise RuntimeError("""The server did not answer the query in the correct way. The answer ID given by the server is: %i (%s).\n Try again or create a bug report if you think this is an error of this program.""" % (int(resp['status']), self.getServerResponse(resp['status'])))
		except ValueError as e:
			message = e.args
			raise RuntimeError("The program has stopped because the server responded with a unknown status. %s" % message[0])

		return content

	def printResult(self, contentRaw, details=False):
		"""
		Prints the results.
		"""
		content = json.loads(contentRaw)
		for item in content['list'][0:1]:
			definition = item['definition']
			permalink = item['permalink']
			word = item['word']
			example = item['example']
            
			print word + ": " + definition
			if details is True:
				print ""
				print "Example: " + self.stripEmptyLines(example)
				print "Link: " + permalink
				#print Fore.YELLOW + "Details:"
				#print Fore.RESET + author + " - " + unicode(defId) + " - " + unicode(thumbsUp) + "/" + unicode(thumbsDown)

	def stripEmptyLines(self, string):
		"""
		Removes empty lines from a given string.
		"""
		newString = ""
		oldString = string
		for line in oldString.split('\n'):
			if line.strip():
				newString += line + '\n'	
		return newString

def main(argv):
	ud = urbandict()

	parser = argparse.ArgumentParser(description='Uses the legendary urbandictionary to find awesome definitions. You will love it!')
	parser.add_argument('--definition', '-d',  help='finds and prints all defintions')
	parser.add_argument('--details', action="store_true", help='prints also examples and details')

	args = parser.parse_args()

	if len(argv) == 1:
		parser.print_help()
		sys.exit()

	if args.definition is not None:
		ud.printResult(ud.findDefinition(args.definition),args.details)

if __name__ == "__main__":
	main(sys.argv)
