"""
Functions related to highlighting
"""

import re


def highlight(s, token,
			wildcard='%',
			begin='<mark>',
			end='</mark>',
			delim=None):
	"""
	wrap all occurrences of token in
	s with <mark> tags for highlighting
	
	wildcard character is treated as a wildcard operator
	e.g. 'test%' would match 'testing'
	
	Performs a case-insensitive match
	"""
	if token:
		if wildcard:
			token = token.replace(wildcard, '.*')
			
		# make regex
		rgx = '^%s$' % token
		rc = re.compile(rgx, re.IGNORECASE)
		
		if not delim:
			if rc.match(s):
				s = '%s%s%s' % (begin, s, end)
		else:
			pieces = []
			
			for p in s.split(delim):
				if rc.match(p):
					pieces.append('%s%s%s' % (begin, p, end))
				else:
					pieces.append(p)
				
			s = delim.join(pieces)
			
	return s


def highlightContains(s, token,
			begin='<mark>',
			end='</mark>'):
	"""
	highlight wherever the token appears
	in s
	"""
	if s and token:
		s = s.replace(token, "%s%s%s" % (begin, token, end))
	return s


def highlightEMAPA(s, tokens,
				begin='<mark>',
				end='</mark>',
				wildcard='%'):
	"""
	Highlight the search results for EMAPA terms
	
	NOTE: Only highlights first matching token
	"""
	
	sOriginal = s
	
	if tokens:
		for token in tokens:
			if not token:
				continue
			
			# if wildcard search, perform highlightContains
			# contains search
			if token[0] ==wildcard and token[-1] == wildcard:
				token = token[1:-1]
				
				# user only search with wildcard
				if not token:
					s = highlight(s, s, begin=begin, end=end, wildcard=wildcard)
					
					
				s = highlightContains(s, token, begin=begin, end=end)
			
			# begins search
			elif token[-1] == wildcard:
				token = token[:-1]
				
	
				if s.lower().startswith(token.lower()):
					
					matchPoint = len(token)
					s = "%s%s%s" % (begin, s[:matchPoint], end) + s[matchPoint:]
					
			# endswith search
			elif token[0] == wildcard:
				token = token[1:]
				if s.lower().endswith(token.lower()):
					matchPoint = len(s) - len(token)
					
					# case-insensitive replace endswith
					s = s[:matchPoint] + "%s%s%s" % (begin, s[matchPoint:], end)
			
			# else we are matching exact terms or synonyms only
			else:
				s = highlight(s, token, begin=begin, end=end, wildcard=wildcard)
			
			
			# only perform one match to avoid begins/end tag collision
			if s != sOriginal:
				break;
	return s