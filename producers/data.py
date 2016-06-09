from bs4 import BeautifulSoup
from collections import defaultdict

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

def parse_data(filename):
    # parse the file as 'pseudo-html'
    soup = BeautifulSoup(open(filename, 'r'), 'html.parser')
    # pull out the input, output, and key
    try:
        input = soup.data.attrs['input']
        output = soup.data.attrs['output']
    except AttributeError:
        raise ParseError("can't find input/output type")
    try:
        key = soup.data.attrs['key']
    except KeyError:
        key = None
    # pull out weights and construct a metric
    weight_dict = {}
    for n in soup.findAll('weight'):
        weight_dict[n.attrs['name']] = float(n.attrs['val'])

    if key:
        base_tup = (input, output, key)
    else:
        base_tup = (input, output)
    metric = Metric(weight_dict, base_tup)
    # pull out the data instances
    data = []
    for n in soup.findAll('example'):
        n_input = list(map(eval, unescaped_split(n.input.string, get_delim(n.input))))
        # sometimes we get single instances, other times we have lists of outputs
        try:
            n_output = eval(n.output.attrs['val'])
        except KeyError:
            n_output = list(map(eval, unescaped_split(n.output.string, get_delim(n.output))))
        data.append( (n_input, n_output) )
    # return a really big tuple
    return input, output, key, data, metric

def parse_tags(filename):
    # parse as pseudoxml
    soup = BeautifulSoup(open(filename, 'r'), 'html.parser')

    tags = []

    for t in soup.findAll('norm'):
        tags.append( (t.attrs['tag'], t.attrs['name']) )

    return tags
