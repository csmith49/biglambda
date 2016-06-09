from argparse import ArgumentParser
import os

parser = ArgumentParser("BigLambda - synthesizing MapReduce programs since 2015")
parser.add_argument("signature")
parser.add_argument("data")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-fs", "--frontiersize", type=int, default=5000)
parser.add_argument("-n", "--normalize", action="store_true")
parser.add_argument("-p", "--parallel", action="store_true")
parser.add_argument("-d", "--dinner", action="store_true")

args = parser.parse_args()
SIG_PATH = os.path.join(os.getcwd(), args.signature)
DATA_PATH = os.path.join(os.getcwd(), args.data)
VERBOSE_FLAG = args.verbose
FRONTIER_SIZE = args.frontiersize
NORM_FLAG = args.normalize
PARALLEL_FLAG = args.parallel
DINNER_FLAG = args.dinner