#!/usr/bin/python2.5
# Mublin <mublin@dealloc.org> Tue Mar 25 17:54:53 CET 2008
# This script is in the public domain, see README.html.
import sys
header = '''\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html 
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="author" content="mublin" />
  <meta name="description" content="Russian source words for Lojban gismu" />
  <meta name="keywords" content="Russian, etymology, Lojban, gismu" />
  <meta name="date" content="2008-03-25" />
  <link rel="copyright" href="README.html" title="Public domain" />
  <link rev="made" href="mailto:mublin@dealloc.org" title="Feedback" />
  <style type="text/css">
/*<![CDATA[*/

body { font-family: monospace; font-size: large; }
h1, h2 { font-family: serif; }
h1, h3 { background-color: white; color: blue; text-align: center; }
h2 { background-color: white; color: green }
dt { margin-top: 1em; }

#version { font-size: medium; }
.index { text-align: center; }
.gismu { font-weight: bold; }
.russian { font-weight: bold; color: red; }
.translation, .comment { 
  font-family: monospace;
  font-style: italic;
  font-size: smaller; 
}
/*]]>*/
  </style>

  <title>Russian etymology of Lojban</title>
</head>

<body>
<h1>Russian etymology of Lojban<br/><span id="version">Version 1.4, April 2008</span></h1>

<hr/>
<div class="index">
  <a href="#b">B</a>
  <a href="#c">C</a>
  <a href="#d">D</a>
  <a href="#f">F</a>
  <a href="#g">G</a>
  <a href="#j">J</a>
  <a href="#k">K</a>
  <a href="#l">L</a>
  <a href="#m">M</a>
  <a href="#n">N</a>
  <a href="#p">P</a>
  <a href="#r">R</a>
  <a href="#s">S</a>
  <a href="#t">T</a>
  <a href="#v">V</a>
  <a href="#x">X</a>
  <a href="#z">Z</a>
  <a href="README.html">README</a>
</div>

<dl>'''

footer = '''\
</dl>
</body>
</html>'''

section = '''\
<hr/><h2 id="%s">%s</h2>'''

entry = '''\
<dt>
  %s
  %s
  %s
</dt>
<dd class="sourceword">
  %s
  %s
  %s
</dd>'''

extra = '''\
<dd class="extra">
  %s
</dd>'''

field = '''\
<span xml:lang="%s" lang="%s" class="%s">%s</span>'''

def span(lang, klass, content):
    if not content:
        return ""
    return field % (lang, lang, klass, content)

def wrap(sandwich, content):
    if not content:
        return ""
    return content.join(sandwich)

print header

initial = ""

for line in sys.stdin:
    #sys.stderr.write(line)
    gismu, keyword, lojbanisation, \
           russian, \
           iso9, \
           translation, \
           comment = line.split('\t')

    if gismu and gismu[0] != initial:
        initial = gismu[0]
        print section % (
            initial, initial.upper())

    if comment:
        comment = comment.replace("``", "&ldquo;")
        comment = comment.replace("''", "&rdquo;")

    gismu         = span("jbo", "gismu", gismu)
    keyword       = span("en", "keyword", keyword)
    lojbanisation = span("jbo", "lojbanisation", lojbanisation)
    russian       = span("ru", "russian", russian)
    iso9          = span("ru", "iso9", iso9)
    translation   = span("en", "translation", translation)
    comment       = span("en", "comment", comment)

    lojbanisation = wrap("[]", lojbanisation)
    iso9          = wrap("[]", iso9)
    translation   = wrap("&ldquo; &rdquo;".split(), translation)

    print entry % (
        gismu, keyword, lojbanisation, 
        russian, iso9, translation)

    if comment:
        print extra % comment

print footer
