#import autolog
def orderedsubsets(xs):
    return _orderedsubsets(list(xs))
def _orderedsubsets(xs):
    if not xs:
        yield []
    while xs:
        x = xs.pop()
        for ys in _orderedsubsets(xs):
            yield ys + [x]
            yield ys
def orderedsubstrings(xs):
    for ys in orderedsubsets(xs):
        yield ''.join(ys)
def orderedoccurs(haystack, needle):
    i = -1
    for c in needle:
        i = haystack.find(c, i + 1)
        if i == -1:
            return False
    return True
#@autolog.logged
def basic_score(gismu, word):
    max = 0
    for sub in orderedsubstrings(word):
        if orderedoccurs(gismu, sub):
            l = len(sub)
            if l > max:
                max = l
    return max
def twoletters(word):
    for i in xrange(len(word)):
        if i + 1 >= len(word):
            break
        yield word[i] + word[i+1]
        if i + 2 >= len(word):
            break
        yield word[i] + word[i+2]
def findall(s, c):
    i = -1
    while True:
        i = s.find(c, i + 1)
        if i == -1:
            break
        yield i
#@autolog.logged
def twoletter_score(gismu, word):
    for c, d in twoletters(word):
        for i in findall(gismu, c):
            if i <= 3 and d == gismu[i+1]:
                return True
            if i <= 2 and d == gismu[i+2]:
                return True
    return False
#@autolog.logged
def score(gismu, word):
    matches = basic_score(gismu, word)
    if matches >= 3:
        return matches
    if twoletter_score(gismu, word):
        return 2
    return 0
def readsourcewords(fd):
    for line in sys.stdin:
        if not line:
            continue
        if '\n' == line[-1]:
            line = line[:-1]
        jbo, zh, en, hi, es, ru, ar = line.split('\t')
        yield (jbo, zh, en, hi, es, ru, ar)
def scoresourcewords(fd):
    for jbo, zh, en, hi, es, ru, ar in readsourcewords(fd):
        scores = ['']
        for word in (zh, en, hi, es, ru, ar):
            scores.append(str(score(jbo, word)))
        sys.stdout.write('\t'.join(line) + '\n')
        sys.stdout.write('\t'.join(scores) + '\n')
def getcontributions(fd):
    from collections import defaultdict
    contributions = defaultdict(int)
    gismu = {}
    for jbo, zh, en, hi, es, ru, ar in readsourcewords(fd):
        if jbo in gismu:
            continue
        if score(jbo, zh): contributions['zh'] += 1
        if score(jbo, en): contributions['en'] += 1
        if score(jbo, hi): contributions['hi'] += 1
        if score(jbo, es): contributions['es'] += 1
        if score(jbo, ru): contributions['ru'] += 1
        if score(jbo, ar): contributions['ar'] += 1
        gismu[jbo] = True
    n = len(gismu)
    for k, v in contributions.iteritems():
        sys.stdout.write('%s = %r%%\n' % (k, (100*v/n)))

def getavgscore(fd):
    scores = {
        'zh': 0.0, 'en': 0.0, 'hi': 0.0, 'es': 0.0, 'ru': 0.0, 'ar': 0.0,
        }
    n = 0
    for jbo, zh, en, hi, es, ru, ar in readsourcewords(fd):
        scores['zh'] += score(jbo, zh)
        scores['en'] += score(jbo, en)
        scores['hi'] += score(jbo, hi)
        scores['es'] += score(jbo, es)
        scores['ru'] += score(jbo, ru)
        scores['ar'] += score(jbo, ar)
        n += 1
    for k, v in scores.iteritems():
        sys.stdout.write('%s = %r\n' % (k,v/n))

if __name__ == '__main__':
    import sys
    getcontributions(sys.stdin)
