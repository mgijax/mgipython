#!/usr/bin/env python

import argparse
import os

def parseInput():
	"""
	Parse the command line input
	returns input files
	"""
	parser = argparse.ArgumentParser(
		description='Input data file(s) to MGD'
	)
	parser.add_argument('files', type=file, nargs='+',
		help='data input files')

	args = parser.parse_args()
	return args



def processFiles(inputFiles, 
				deferConstraints=False):
	"""
	validate, process, and load the input files
	
		deferConstraints -- defers all table constraint checking until end of transaction
			Useful for updating tables with circular foreign keys
	"""
	

	from handler import getHandler	
	from mgipython.modelconfig import db
	
	print db
	
	print inputFiles
	
	# start transaction
	con = db.session.connection()
	
	if deferConstraints:
		con.execute('set constraints all deferred')
	
	# TODO(kstone): This may be memory inefficient.
	#	Refactor candidate (maybe store key map in a file)
	relativeKeyMap = {}
		
	for inputFile in inputFiles:
		config = _readConfig(inputFile)
		print config
		
		
		# get the handler
		handler = getHandler(config['dataType'], filePointer = inputFile,
								columnDelim = config['columnDelim'],
								columnOrder = config['columnOrder'],
								defaultParams = config['defaultParams'],
								opType = config['opType'],
								relativeKeyMap = relativeKeyMap)
		
		print "\nProcessing file with %s handler" % handler.DATA_TYPE
		
		
		handler.validate()
		
		print "validated %s file %s" % (handler.DATA_TYPE, handler.filePointer.name)
		
		print "Calculating inserts and updates"
		
		handler.unify()
		
		print "Calculated inserts and updates"
		
		print handler.ops
		
		print "loading data file"
		
		handler.load()
		
	db.session.commit()

def _readConfig(inputFile):
	"""
	Reads the config header of input file	
	returns {opType, dataType, columnOrder, columnDelim}
	"""
	head = [next(inputFile) for x in xrange(3)]
	opType = head[0].strip()
	dataType = head[1].strip()
	columnOrder = head[2].strip()
	
	defaultParams = {}
	
	# parse any default data params
	if '(' in dataType and dataType[-1] == ')':
		parenStart = dataType.find('(')
		
		paramString = dataType[ (parenStart + 1) : -1].strip().replace('"','')
		paramStrings = paramString.split(',')
		
		dataType = dataType[:parenStart]
		
		for paramString in paramStrings:
			items = paramString.split('=')
			if len(items) > 1:
				key = items[0].strip()
				value = items[1].strip()
				if key and value:
					defaultParams[key] = value

	columnDelim = '\t'
	if ',' in columnOrder:
		columnDelim = ','
	
	columnOrder = columnOrder.split(columnDelim)
	return {"opType": opType, "dataType": dataType, "columnOrder": columnOrder,
		"columnDelim": columnDelim, "defaultParams": defaultParams}


def writeDataFile(fileName, dataRows,
				modelName,
				columns,
				operation="Update",
				defaultParams={},
				columnDelim='\t'):
	"""
	Creates an input file suitable for processFiles()
		Writes the appropriate file headers from
			operations, modelName, columns, and defaultParams
			
		fileName points to created file
	"""
	fp = open(fileName, 'w')
	
	modelLine = modelName
	if defaultParams:
		modelLine += "(%s)" % ",".join(["%s=%s" % (k, str(v)) for k,v in defaultParams.items()])
	
	try:
		# write header
		fp.write("%s\n" % operation)
		fp.write("%s\n" % modelLine)
		fp.write("%s\n" % columnDelim.join(columns))
		
		# write dataRows
		for r in dataRows:
			fp.write("%s\n" % columnDelim.join([str(c) for c in r]))
			
	finally:
		fp.close()


if __name__ == "__main__":

	args = parseInput()
	inputFiles = args.files
	
	# initialize DB model for testing
	server=os.environ['MGD_DBSERVER']
	database=os.environ['MGD_DBNAME']
	user=os.environ['MGD_DBUSER']
	passwordFile=os.environ['MGD_DBPASSWORDFILE']
	password=''
	with open(passwordFile, 'r') as f:
		password = f.readline()

	
	from mgipython import modelconfig
	modelconfig.createDatabaseEngine(
		server=server,
		database=database,
		user=user,
		password=password,
		trace=False
	)

	try:
		processFiles(inputFiles)
	finally:
		for f in inputFiles:
			f.close()

	print "successfully loaded %s" % [f.name for f in inputFiles]
