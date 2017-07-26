from argparse import ArgumentParser
import os

PATH = "/PATH/TO/THIS/FILE"

parser = ArgumentParser("BigLambda - synthesizing MapReduce programs since 2015")
parser.add_argument("-s", "--signature")
parser.add_argument("-d", "--data")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-fs", "--frontiersize", type=int, default=5000)
parser.add_argument("-p", "--parallel", action="store_true")
parser.add_argument("--dinner", action="store_true")
parser.add_argument("-b", "--benchmark")

args = parser.parse_args()
try:
    SIG_PATH = os.path.join(PATH,  args.signature)
    DATA_PATH = os.path.join(PATH, args.data)
except:
    SIG_PATH = os.path.join(PATH, "../benchmarks/", args.benchmark, "sig.py")
    DATA_PATH = os.path.join(PATH, "../benchmarks/", args.benchmark, "data")
VERBOSE_FLAG = args.verbose
FRONTIER_SIZE = args.frontiersize
PARALLEL_FLAG = args.parallel
DINNER_FLAG = args.dinner
