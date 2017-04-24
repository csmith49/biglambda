import heapq

class LazyList(object):
	def __init__(self, generator):
		self._generator = generator
		self._history = []
	def __getitem__(self, key):
		print(len(self._history))
		while key >= len(self._history):
			self._history.append(next(self._generator))
		return self._history[key]

class LazyFrontier(object):
	def __init__(self, generators, combiner=None):
		self._generators = generators
		if combiner is None:
			self._combiner = lambda x: x
		else:
			self._combiner = combiner
		self._frontier = [(0, (0,) * len(self._generators))]
		self._seen = set()
	def __iter__(self):
		return self
	def __next__(self):
		h, cur = heapq.heappop(self._frontier)
		for child in self._children(cur):
			h_child = self._heuristic(child)
			heapq.heappush(self._frontier, (h_child, child) )
		return h, self._combiner(*self._item(cur))
	def _heuristic(self, index):
		return sum(self._generators[i][j][0] for i, j in enumerate(index))
	def _item(self, index):
		return [self._generators[i][j][1] for i, j in enumerate(index)]
	def _children(self, index):
		for i in range(len(index)):
			new_index = index[:i] + (index[i] + 1, ) + index[i+1:]
			if not new_index in self._seen:
				self._seen.add(new_index)
				yield new_index

class LazyProduct(object):
	def __init__(self, generators):
		self._generators = generators
		self._frontier = []
		for i, gen in enumerate(self._generators):
			h, cur = next(gen)
			heapq.heappush(self._frontier, ( (h, (i, cur)) ))
	def __iter__(self):
		return self
	def __next__(self):
		h, (i, cur) = heapq.heappop(self._frontier)
		h_p, cur_p = next(self._generators[i])
		heapq.heappush(self._frontier, (h_p, (i, cur_p)))
		return cur

def generate_search(prod_gen, sketches):
	producers = {}
	consumers = []
	for sketch in sketches:
		reqs = []
		for req in sketch.reqs:
			try:
				prod = producers[req]
			except:
				prod = LazyList(prod_gen(req))
				producers[req] = prod
			reqs.append(prod)
		consumers.append(LazyFrontier(reqs, sketch))
	return LazyProduct(consumers)
