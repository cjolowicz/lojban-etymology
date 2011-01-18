#!/usr/bin/python2.5
# 
# TODO:
# - markup: directionality, language

import sys
from datetime import datetime
import score
from gismudict import gismudict
from itertools import izip, count

DEBUG = False
VERSION = '1.0'
indentlevel = 0
indentwidth = 2
now = datetime.now()

def indent():
    global indentlevel
    assert(indentlevel >= 0)
    indentlevel += indentwidth

def unindent():
    global indentlevel
    indentlevel -= indentwidth
    assert(indentlevel >= 0)

def output(s='', newline=True):
    if type(s) == unicode:
        s = s.encode('utf-8')
    if newline:
        s += '\n'
    sys.stdout.write(' ' * indentlevel + s)

def message(s='', newline=False):
    if newline:
        s += '\n'
    sys.stderr.write(s)

def htmlquote(s):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    return s

def parsefile(langcode):
    from collections import defaultdict
    result = defaultdict(list)
    for line in open('lojban-source-words_%s.txt' % langcode):
        line = line.decode('utf-8')
        if line and line[-1]=='\n':
            line = line[:-1]
        if not line:
            continue
        line = htmlquote(line)
        line = line.split('\t')
        result[line[0]].append(line[1:])
    return result

def markup_sumti(definition):
    for x in ('x1', 'x2', 'x3', 'x4', 'x5'):
        definition = definition.replace(x, '<span class="sumti">%s</span>' % x)
    return definition

def parse_remark(comment):
    comment = htmlquote(comment)
    comment = markup_sumti(comment)

    # find gismu refs
    remark, words = [], comment.split()
    for word, i in izip(words, count()):
        before = after = ''
        if word and word[0] not in 'abcdefgijklmnoprstuvxyz':
            before, word = word[0], word[1:]
        if word and word[-1] not in 'abcdefgijklmnoprstuvxyz':
            word, after = word[:-1], word[-1]
        if len(word) == 5 and word in gismudict and not (
                word == 'cmavo' and i+1 < len(words) and words[i+1] == 'list'):
            word = '<a class="gismuref" href="#%s">%s</a>' % (2 * (word,))
        remark.append(word.join((before, after)))
    remark = ' '.join(remark)

    # split reference from remark
    i = remark.find('(cf. ')
    if i == 0:
        remark, references = '', remark[1:-1]
    elif i > 0:
        remark, references = remark[:i], remark[i+1:-1]
    else:
        references = ''

    remark = remark.strip()
    references = references.strip()

    # clean up remark
    if remark and remark[-1] == ';':
        remark = remark[:-1]
    if remark and remark[0] == '[' and remark[-1] == ']':
        remark = remark[1:-1]
    remark = remark.replace(']; [', '; ')

    # clean up references
    if references:
        references = u'\u2192' + references[3:]

    return remark, references

def output_index():
    output('<div class="index">')
    indent()
    for initial in 'abcdefgijklmnoprstuvxyz':
        output('<a href="#%s" accesskey="%s">%s</a>' % (3 * (initial,)))
    unindent()
    output('</div>')

#languages = dict(zh='C.',en='E.',hi='H.',es='S.',ru='R.',ar='A.')
languages = dict(zh='Chinese',en='English',hi='Hindi',es='Spanish',ru='Russian',ar='Arabic')
            
zh = parsefile('zh')
en = parsefile('en')
hi = parsefile('hi')
es = parsefile('es')
ru = parsefile('ru')
ar = parsefile('ar')

etymology = dict.fromkeys(set(zh) | set(en) | set(hi) | set(es) | set(ru) | set(ar))

output('''\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html 
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="author" content="mublin" />
  <meta name="description" content="Source words for Lojban gismu" />
  <meta name="keywords" content="etymology, Lojban, gismu" />
  <meta name="date" content="%s" />
  <link rel="copyright" href="README.html" title="Public domain" />
  <link rev="made" href="mailto:mublin@dealloc.org" title="Feedback" />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <style type="text/css">
/*<![CDATA[*/
/*]]>*/
  </style>

  <title>Etymology of Lojban</title>
</head>''' % str(now.date()))

output()
output('<body>')
output()
output('<div class="content">')
indent()
output('<h1>Etymology of Lojban<br/><span id="version">Version %s, %s</span></h1>' % (
    VERSION, now.strftime('%B %Y')))
output()
output_index()
output()
output('<div class="main">')
indent()
initial = ''
for gismu, gismudef in sorted(gismudict.iteritems()):
    if len(gismu) != 5:
        continue # skip cmavo

    if initial != gismu[0]:
        initial = gismu[0]
        if DEBUG and initial > 'b':
            break
        message(initial)
        output()
        output('<h3 class="initial" id="%s">%s</h3>' % (2 * (initial,)))

    remark, references = parse_remark(gismudef.comment)
    output()
    output('<div class="entry">')
    indent()
    output('<span class="gismu" id="%s">%s</span>' % (2 * (gismu,)))
    output('<span class="rafsilist">')
    indent()
    for rafsi in gismudef.rafsi:
        output('<span class="rafsi">[%s]</span>' % rafsi)
    unindent()
    output('</span>')
    output('<span class="gismudef">&ldquo;%s&rdquo;</span>' % markup_sumti(gismudef.definition))
    output('<span class="keywords">')
    indent()
    for i, keywords in sorted(gismudef.keywords.items()):
        output('<span class="keywordentry">')
        indent()
        output('<span class="place">x%d</span>' % i)
        output('<span class="keyword">%s</span>' % '; '.join(keywords))
        unindent()
        output('</span>')
    unindent()
    output('</span>')

    if gismu in etymology:
        output('<span class="etymology">')
        indent()
        for langcode, lang in (('en',en), ('zh',zh), ('hi',hi), ('es',es), ('ru',ru), ('ar',ar)):
            entries = []
            done = {}
            for entry in lang[gismu]:
                if lang == ar:
                    entry += [u''] * (6 - len(entry))
                keyword, transcription, entry = entry[0], entry[1], entry[2:]
                value = score.score(gismu, transcription)
                if value:
                    if entry[0] in done:
                        continue
                    done[entry[0]] = True
                    entries.append((keyword, transcription, entry))
            if entries:
                output('<span class="langetymology">')
                indent()
                output('<span class="lang">%s</span>' % languages[langcode])
                output('<span class="sourcewordentries">')
                indent()
                for entry, i in izip(entries, count(1)):
                    keyword, transcription, entry = entry
                    output('<span class="sourcewordentry">')
                    indent()
                    if len(entries) > 1:
                        output('<span class="sourcewordnumber">%d</span>' % i)
                    if not entry[0]:
                        output('<span class="sourceword transcription">*%s</span>' % transcription)
                        continue

                    if lang == en:
                        output('<span class="sourceword">%s</span>' % entry[0])
                    elif lang == es:
                        output(u'<span class="sourceword" xml:lang="es" lang="es">%s</span>' % entry[0])
                        output(u'<span class="translation">%s</span>' % entry[1])
                    elif lang in (hi, ru):
                        output(u'<span class="sourceword" xml:lang="%s" lang="%s">%s</span>' % (langcode, langcode, entry[0]))
                        output(u'<span class="transliteration">[%s]</span>' % entry[1])
                        output(u'<span class="translation">%s</span>' % entry[2])
                    elif lang == ar:
                        output(u'<span class="sourceword" xml:lang="ar" lang="ar" dir="rtl">%s</span>' % entry[0])
                        output(u'<span class="transliteration">[%s]</span>' % entry[1])
                        output(u'<span class="translation">%s</span>' % entry[2])
                    elif lang == zh:
                        if entry[1]:
                            output(u'<span class="sourceword" xml:lang="zh" lang="zh">%s</span>' % entry[0])
                            output(u'<span class="sourceword simplified">(%s)</span>' % entry[1])
                            output(u'<span class="transliteration">[%s]</span>' % entry[2])
                            output(u'<span class="translation">%s</span>' % entry[3])
                        else:
                            output(u'<span class="sourceword" xml:lang="zh" lang="zh">%s</span>' % entry[0])
                            output(u'<span class="transliteration">[%s]</span>' % entry[2])
                            output(u'<span class="translation">%s</span>' % entry[3])

                    comment = entry[-1]
                    if 'dubious' in comment or 'FIXIT' in comment:
                        output('<span class="comment">(?)</span>')

                    unindent()
                    output('</span>') # class="langetymology"
                unindent()
                output('</span>') # class="sourcewordentries"
                unindent()            
                output('</span>') # class="sourcewordentry"
        unindent()            
        output('</span>') # class="etymology"

    if references:
        output('<span class="references">%s</span>' % references)

    if remark:
        output('<span class="remark">%s</span>' % remark)

    unindent()            
    output('</div>') # class="entry"
unindent()
output('</div>') # class="main"
output()
output_index()
output()
unindent()
output('</div>') # class="content"
output('</body>')
output('</html>')
message(newline=True)
