import setup
import heapq
import takethree
import consumers

#------------------------------------------------------------------------------
# primary algorithm, used as iterator
#------------------------------------------------------------------------------
def explore_frontier(sig, data_type, metric, max_size, normalizer):
	# closure for binding sig and rules easily
	expand = takethree.generate_expander(sig, normalizer)
	# generate appropriate starting node based on type
	start_node = takethree.e.Un(takethree.parse_type(data_type))
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
	signature, normalizer, module = takethree.generate_resources(setup.SIG_PATH, None)
	*data_types, data, metric = takethree.parse_data(setup.DATA_PATH)

	if setup.VERBOSE_FLAG: print("Data loaded. Creating consumers and producers...")

	# restructure data types a little (for keys and stuff, I think)
	if data_types[2] is None:
		data_types = data_types[:2]
	# construct producers from frontier search above
	producer = lambda t: explore_frontier(signature, t, metric, setup.FRONTIER_SIZE, normalizer)
	# create managers to hold all the producers/consumers
	manager = consumers.ProductionManager(producer)
	# consumers need to be able to execute the programs generated - make a writer
	writer = takethree.CodeWriter(module)
	# create all the consumers!
	manager.create_consumer(consumers.Sketch(data_types, False, False))
	manager.create_consumer(consumers.Sketch(data_types, True, False))
	manager.create_consumer(consumers.Sketch(data_types, False, True))
	manager.create_consumer(consumers.Sketch(data_types, True, True))
	# start churning out those solutions!
	q = manager.start_production()

	if setup.VERBOSE_FLAG: print("Production started. Iterating solutions...")

	# we're iterating through solutions from q until we find one that works
	done = False
	counter = 0
	while not done:
		program = q.get()
		counter += 1

		if setup.VERBOSE_FLAG:
			print("Considering program {}:\n{}".format(counter, repr(program)))

		# let's see if it's consistent on examples
		for ex_input, ex_output in data:
			# we might break while running it, for whatever reason
			try:
				output = program(ex_input, writer)
			except Exception as e:
				if setup.VERBOSE_FLAG: print("\tRejected. Evaluation on examples crashed.")
				break
			# if we're comparing lists, sort first
			if isinstance(output, list) and isinstance(ex_output, list):
				try:
					if sorted(output) != sorted(ex_output):
						if setup.VERBOSE_FLAG: print("\tRejected. Not consistent on examples.")
						break
				except:
					pass
			# otherwise just check for equality
			elif output != ex_output:
				if setup.VERBOSE_FLAG: print("\tRejected. Not consistent on examples.")
				break
			# and that our reducer is a csg
			elif not program.csg_check(ex_input, writer):
				if setup.VERBOSE_FLAG: print("\tRejected. Reducer not a CSG.")
				break
		# if no breaks reached - we've found a solution
		else:
			done = True

			print(repr(program))
