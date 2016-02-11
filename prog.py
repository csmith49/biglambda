# OUTLINE:
# step 1: read where the sig/data files are
# step 2: load the data, get the types and starting nodes
# step 3: run program until success is found

# imports
import argparse
import heapq
import os
import takethree

#algorithm definition, to be used as an iterator
def explore_frontier(signature, data_types, metric, max_size, normalizer):
    # closure for binding sig and rules easily
    expand = takethree.generate_expander(signature, normalizer)
    # use takethree to gen appropriate templates
    start_nodes = takethree.create_start(*data_types)
    frontier = []
    for s in start_nodes:
        frontier += [(metric(e), e) for e in expand(s)]
    heapq.heapify(frontier)
    # now generate frontier exploration
    while len(frontier) < max_size:
        m, expr = heapq.heappop(frontier)
        expansions = expand(expr)
        if expansions:
            for new_expr in expansions:
                heapq.heappush(frontier, (metric(new_expr), new_expr) )
        elif len(expr._values_from_kind("un")) == 0:
            yield expr

# STEP 1
# set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("signature")
parser.add_argument("data")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-fs", "--frontiersize", type=int, default=5000)
parser.add_argument("-n", "--normalize", action="store_true")

# STEP 2
# now parse the args, and convert to the appropriate data
args = parser.parse_args()
# first by filepaths
sig_path = os.path.join(os.getcwd(), args.signature)
data_path = os.path.join(os.getcwd(), args.data)
# now by using takethree's resource generators
sig, norm, module = takethree.generate_resources(sig_path, None)
*data_types, data, metric = takethree.parse_data(data_path)
# Need to generate new normalizer, will do so here
# DO IT NOW
if args.normalize:
    tags = takethree.parse_tags(data_path)
    norm = takethree.EasyNormalizer(tags)
else:
    norm = None

# apply the algorithm, letting us iterate over possible results
results = explore_frontier(sig, data_types, metric, args.frontiersize, norm)
writer = takethree.CodeWriter(module)

# STEP 3
# here we go

final = None

if args.verbose: print("Starting iteration...")
for i, expr in enumerate(results):
    if args.verbose: print("Visiting " + repr(expr))
    if args.verbose: print("    Count: " + str(i))
    try:
        func = writer(expr)
        for input, output in data:
            expr_output = func(input)
            if args.verbose:
                print("   > Function Output: " + repr(expr_output))
                print("   >     File Output: " + repr(output))
            if isinstance(expr_output, list) and isinstance(output, list):
                if sorted(expr_output) != sorted(output):
                    break
            elif expr_output != output:
                break
        else:
            print("Success: " + repr(expr))
            final = expr
            break
    except Exception as err:
        if args.verbose: print("Execution failed: " + repr(err))
