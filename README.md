# biglambda
Source code for the BigLambda data-parallel synthesis project. Based 
on the PLDI 2016 paper **MapReduce Program Synthesis** by 
[Calvin Smith](http://pages.cs.wisc.edu/~cjsmith/) and 
[Aws Albarghouthi](http://pages.cs.wisc.edu/~aws/).

## Dependencies
The tool depends on the most recent versions of `BeautifulSoup`,
`lxml`, and `ply`, neither of which are included.

## Usage
First edit `PATH` in `biglambda/setup.py`.
```
usage: BigLambda - synthesizing MapReduce programs since 2015
       [-h] [-s SIGNATURE] [-d DATA] [-v] [-fs FRONTIERSIZE] [-p] [--dinner]
       [-b BENCHMARK]

optional arguments:
  -h, --help            show this help message and exit
  -s SIGNATURE, --signature SIGNATURE
  -d DATA, --data DATA
  -v, --verbose
  -fs FRONTIERSIZE, --frontiersize FRONTIERSIZE
  -p, --parallel
  --dinner
  -b BENCHMARK, --benchmark BENCHMARK
```
`biglambda/producers/parser.out` and `biglambda/producers/typetab.py` 
will be generated after the computation.
