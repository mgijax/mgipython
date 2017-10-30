import string

sdict = {   '' : ('')   }
digits = {  '1' : 1, '2' : 1, '3' : 1, '4' : 1,
      '5' : 1, '6' : 1, '7' : 1, '8' : 1,
      '9' : 1, '0' : 1  }

def splitter (s):
   global sdict
   if sdict.has_key (s):
      return sdict[s]
   last = 0
   items = []
   sl = string.lower (s)
   in_digits = digits.has_key (sl[0])
   for i in range(0, len(sl)):
      if digits.has_key (sl[i]) != in_digits:
         if in_digits:
            items.append (string.atoi(sl[last:i]))
         else:
            items.append (sl[last:i])
         last = i
         in_digits = not in_digits
   if in_digits:
      items.append (string.atoi (sl[last:]))
   else:
      items.append (sl[last:])
   sdict[s] = tuple(items)
   return sdict[s]

def nomenCompare (s1, s2):
   return cmp(splitter(s1), splitter(s2))
