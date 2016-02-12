####################################
# IMPORTS
###################################

# imports for threaded data structures
import multiprocessing
import multistructures
# imports for algorithm stuff
import argparse
import os
import takethree
import heapq
import hos
import itertools

from pprint import pprint

#######################################
# Argument parsing
#######################################
def get_args():
    # construct parser and add args
    parser = argparse.ArgumentParser()
    parser.add_argument("signature")
    parser.add_argument("data")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-fs", "--frontiersize", type=int, default=5000)
    parser.add_argument("-n", "--normalize", action="store_true")

    # extract relevant arguments
    args = parser.parse_args()
    sig_path = os.path.join(os.getcwd(), args.signature)
    data_path = os.path.join(os.getcwd(), args.data)
    # get relevant data structures
    sig, norm, module = takethree.generate_resources(sig_path, None)
    *data_types, data, metric = takethree.parse_data(data_path)
    if args.normalize:
        norm = takethree.EasyNormalizer(takethree.parse_tags(data_path))
    return sig, norm, module, data_types, data, metric, args.frontiersize, args.verbose

#######################################
# Actual algorithm
#######################################
def explore_frontier(signature, data_type, metric, max_size, normalizer):
    # closure for binding sig and norm easily
    expand = takethree.generate_expander(signature, normalizer)
    # create starting node and go frontier
    start_node = takethree.e.Un(takethree.parse_type(data_type))
    frontier = [(metric(start_node), start_node)]
    # go hog wild
    while len(frontier) < max_size:
        m, expr = heapq.heappop(frontier)
        expansions = expand(expr)
        if expansions:
            for new_expr in expansions:
                heapq.heappush(frontier, (metric(new_expr), new_expr) )
        elif len(expr._values_from_kind("un")) == 0:
            yield m[0], expr

def explore_frontier_hist(signature, data_type, metric, max_size, normalizer):
    expand = takethree.generate_expander(signature, normalizer)
    start_node = takethree.e.Un(takethree.parse_type(data_type))
    frontier = [(metric(start_node), start_node, [start_node])]
    while len(frontier) < max_size:
        m, expr, history = heapq.heappop(frontier)
        expansions = expand(expr)
        if expansions:
            for new_expr in expansions:
                heapq.heappush(frontier, (metric(new_expr), new_expr, history + [new_expr]))
        elif len(expr._values_from_kind("un")) == 0:
            pprint(history)
            yield m[0], expr


#######################################
# Main loop (testing for now)
#######################################

if __name__ == "__main__":
    sig, norm, module, data_types, data, metric, fs, verbose = get_args()
    # adjust data type spec
    if data_types[2] is None:
        data_types = data_types[0], data_types[1]
    # define what our producers look like
    producer = lambda t: explore_frontier(sig, t, metric, fs, norm)
    # create a manager to hold it all
    manager = multistructures.ProductionManager(producer)
    # create writer for consumers
    writer = takethree.CodeWriter(module)
    # now create consumers and add them
    manager.create_consumer(hos.Sketch(data_types, False, False))
    manager.create_consumer(hos.Sketch(data_types, True, False))
    manager.create_consumer(hos.Sketch(data_types, False, True))
    manager.create_consumer(hos.Sketch(data_types, True, True))
    # start production
    q = manager.start_production()

    done = False
    counter = 0
    while not done:
        prog = q.get()
        if verbose: print(prog)
        counter += 1
        for i, o in data:
            try:
                val = prog(i, writer)
                if verbose: print(val, o)
            except Exception as e:
                if verbose: print(e)
                break
            if isinstance(val, list) and isinstance(o, list):
                try:
                    if sorted(val) != sorted(o):
                        break
                except:
                    if verbose: print("failure to compare")
            elif val != o:
                break
            elif not prog.csg_check(i, writer):
                break
        else:
            done = True
            print("DINNER_STAT sol {}".format(repr(prog)))
            print("DINNER_STAT size {}".format(prog.size()))
