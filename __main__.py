import setup
import heapq
import producers
import consumers
from bs4 import BeautifulSoup

#------------------------------------------------------------------------------
# primary algorithm, used as iterator
#------------------------------------------------------------------------------
def explore_frontier(sig, data_type, metric, max_size, normalizer):
	# closure for binding sig and rules easily
	expand = producers.generate_expander(sig, normalizer)
	# generate appropriate starting node based on type
	start_node = producers.e.Un(producers.parse_type(data_type))
	frontier = [(metric(start_node), start_node)]
	# go hog wild
	while len(frontier) < max_size:
		# pull expression off heap, check expansions
		m, expr = heapq.heappop(frontier)
		expansions = expand(expr)
		# if there are expansions, just add them back in
		if expansions:
			for new_expr in expansions:
				heapq.heappush(frontier, (metric(new_expr), new_expr) )
		# if there aren't any expansions and the program is closed, we're done
		elif len(expr._values_from_kind("un")) == 0:
			yield m[0], expr

#------------------------------------------------------------------------------
# now we treat this module as a script - time to execute!
#------------------------------------------------------------------------------
if __name__ == '__main__':
	soup = BeautifulSoup(open(setup.DATA_PATH, 'r'), 'html.parser')
	signature, module = producers.generate_resources(setup.SIG_PATH)
	data_types = producers.parse_data_types(soup)
	data = producers.parse_examples(soup)
	metric = producers.parse_metric(soup)
	if setup.NORM_FLAG:
		normalizer = producers.parse_normalizer(soup)
	else:
		normalizer = None

	if setup.VERBOSE_FLAG: print("Data loaded. Creating consumers and producers...")

	# restructure data types a little (for keys and stuff, I think)
	if data_types[2] is None:
		data_types = data_types[:2]
	# construct producers from frontier search above
	producer = lambda t: explore_frontier(signature, t, metric, setup.FRONTIER_SIZE, normalizer)
	# consumers need to be able to execute the programs generated - make a writer
	writer = producers.CodeWriter(module)
	# create all the consumers!
	sketches = [
		consumers.Sketch(data_types, False, False),
		consumers.Sketch(data_types, False, True),
		consumers.Sketch(data_types, True, False),
		consumers.Sketch(data_types, True, True)
	]

	if setup.VERBOSE_FLAG: print("Production started. Iterating solutions...")

	# we're iterating through solutions from q until we find one that works
	for i, program in enumerate(consumers.generate_search(data_types, producer, sketches)):
		for ex_input, ex_output in data:
			try:
				output = program(ex_input, writer)
			except:
				break
			if isinstance(output, list) and isinstance(ex_output, list):
				try:
					if sorted(output) != sorted(ex_output):
						break
				except:
					pass
			elif output != ex_output:
				break
			elif not program.csg_check(ex_input, writer):
				break
		else:
			print("Found solution after {} steps".format(i))
			print(repr(program))
			break