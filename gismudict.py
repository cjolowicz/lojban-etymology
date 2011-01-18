#!/usr/bin/python

class gismudef(object):
    def __init__(self, line):
        _, self.gismu, self.cvc, self.ccv, self.cvv, self.keyword, self.hintword, self.definition, self.textbook, self.frequency, self.comment = \
           [s.strip() for s in splitfields(line, (1, 7, 11, 15, 20, 41, 62, 159, 161, 169))]
        self.rafsi = [rafsi for rafsi in (self.cvc, self.ccv, self.cvv) if rafsi]
        self.keywords = keywords[self.gismu]

#         i = self.comment.rfind('(cf. ')
#         if i != -1:
#             self.references = [x.strip() for x in self.comment[i+5:-1].split(',')]
#             self.comment = self.comment[:i]
#         else:
#             self.references = []

def splitfields(line, args):
    result, i = [], 0
    for arg in args:
        result.append(line[i:arg])
        i = arg
    result.append(line[i:])
    return result

from collections import defaultdict
keywords = defaultdict(dict)
fd = open('oblique_keywords.txt')
for line in fd:
    line = line.rstrip()
    if not line:
        continue
    gismu, ks = line.split(';', 1)
    gismu, place = gismu[:-1], int(gismu[-1])
    ks = [k.strip() for k in ks.split(';')]
    keywords[gismu][place] = ks

gismudict = {}
fd = open('gismu.txt')
fd.readline()
for line in fd:
    line = line.rstrip()
    if not line:
        continue
    gismu = gismudef(line)
    gismudict[gismu.gismu] = gismu
