from bs4 import BeautifulSoup
from collections import defaultdict
from functools import partial
from . import kbo
from .termparser import parse_term

# simple exception class for parsing issues
class ParseError(Exception):
    def __init__(self, message):
        self._message = message
    def __repr__(self):
        return repr(self._message)

DEFAULT_METRIC = {"fst": 0.01, "snd": 0.01, "emit": 0.01, "lower": 0.01}

# linear metric on expressions
# maintains a counter, and outputs (m, count) to break ties
# otherwise heapq tries to order the nodes and crashes
class Metric:
    def __init__(self, weights=None, base=None):
        self._weights = defaultdict(lambda: 1)
        self._weights.update(DEFAULT_METRIC)
        if weights is not None:
            self._weights.update(weights)
        self._count = 0
        self._base = base
    def evaluate(self, node):
        w = self._weights
        base = self._base
        total = 0.0
        stack = [node]
        while stack:
            current = stack.pop()
            if current[0] == "un" and base:
                if repr(current[1][1]) in base:
                    total += 1
                else:
                    total += 1
            else:
                total += 1 / w[str(current[1])]
            stack.extend(current[2])
        self._count += 1
        return (total, self._count)
    def __repr__(self):
        return repr(dict(self._weights))
    def __call__(self, n):
        return self.evaluate(n)

# strings from soup are escaped - we convert them to bytestrings and decode
# to unescape them
def unescaped_split(string, splitter):
    new_splitter = splitter.encode('latin1').decode('unicode_escape')
    return [l.strip() for l in string.strip().split(new_splitter)]

# just wraps a dict lookup in a try-catch block to default to newlines
def get_delim(soup_node):
    try:
        return soup_node.attrs['delim']
    except KeyError:
        return "\n"

def parse_data_types(soup):
    input = soup.data.attrs['input']
    output = soup.data.attrs['output']
    try:
        key = soup.data.attrs['key']
    except KeyError:
        key = None
    return input, output, key

def parse_examples(soup):
    data = []
    for n in soup.data.findAll('example'):
        n_input = list(map(eval, unescaped_split(n.input.string, get_delim(n.input))))
        # sometimes get just one instance, other times we've got a list
        try:
            n_output = eval(n.output.attrs['val'])
        except KeyError:
            n_output = list(map(eval, unescaped_split(n.output.string, get_delim(n.output))))
        data.append( (n_input, n_output) )
    return data

def parse_metric(soup):
    weights = {}
    for n in soup.data.findAll('weight'):
        weights[n.attrs['name']] = float(n.attrs['val'])
    return Metric(weights)

def parse_normalizer(soup):
    weights = {}
    precedences = {}
    for n in soup.trs.findAll('weight'):
        weights[n.attrs['name']] = float(n.attrs['val'])
    for n in soup.trs.findAll('precedence'):
        precedences[n.attrs['name']] = float(n.attrs['val'])
    # create whatever order we may have
    W = kbo.Weight(weights)
    P = kbo.Precedence(precedences)
    order = partial(kbo.gt_kbo, W=W, P=P)
    # convert rules into rule objects
    rules = list(map(parse_term, unescaped_split(soup.trs.rules.string, get_delim(soup.trs.rules))))
    rules = list(map(lambda p: kbo.Rule(*p), rules))
    # convert equations into eq objects
#    equations = list(map(parse_term, unescaped_split(soup.trs.eqs.string, get_delim(soup.trs.eqs.output))))
#    equations = list(map(lambda p: kbo.Rule(*p, order), equations))
    equations = []
    # now construct the normalizer
    return kbo.Normalizer(rules, equations)