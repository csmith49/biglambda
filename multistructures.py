import os
import multiprocessing
from collections import defaultdict
import heapq
import time

class PrioritySet(object):
    def __init__(self):
        self._heap = []
        self._set = set()
    def push(self, priority, obj):
        if obj not in self._set:
            heapq.heappush(self._heap, (priority, obj))
            self._set.add(obj)
    def pop(self):
        priority, obj = heapq.heappop(self._heap)
        self._set.remove(obj)
        return obj

class PipeCombiner(object):
    def __init__(self, conns):
        self._conns = conns
        self._lists = [[] for i in range(len(conns))]
        self._frontier = PrioritySet()
        self._frontier.push(0, (0, ) * len(self._lists))
    def __iter__(self):
        return self
    def __next__(self):
        try:
            index = self._frontier.pop()
        except IndexError:
            raise StopIteration
        for child in self.children(index):
            self._frontier.push(self.lookup_metric(child), child)
        return self.lookup_value(index)
    @staticmethod
    def children(index):
        for i in range(len(index)):
            copy = tuple([index[j] if j != i else index[j]+1 for j in range(len(index))])
            yield copy
    def lookup(self, index):
        val = []
        for li, ind in enumerate(index):
            while len(self._lists[li]) <= ind:
                v = self._conns[li].recv()
                self._lists[li].append(v)
            val.append(self._lists[li][ind])
        return tuple(val)
    def lookup_value(self, index):
        v = self.lookup(index)
        return tuple([p[1] for p in v])
    def lookup_metric(self, index):
        v = self.lookup(index)
        return sum([p[0] for p in v])

def lift_to_conns(conns, gen, msg = None):
    for item in gen:
        for i in conns:
            i.send(item)

def lift_to_queue(queue, gen, msg = None):
    for item in gen:
        queue.put(item)
    print("terminating")

class Producer(object):
    def __init__(self, conns, gen):
        self._conns = conns
        self._gen = gen
    def add_conn(self, conn):
        self._conns.append(conn)
    def start(self, msg = None):
        proc = multiprocessing.Process(target=lift_to_conns, args=(self._conns, self._gen, msg))
        proc.daemon = True
        proc.start()

class Consumer(object):
    def __init__(self, conned_gen):
        self._gen = conned_gen
    def __iter__(self):
        return self._gen
    def output_to_queue(self, queue):
        proc = multiprocessing.Process(target=lift_to_queue, args=(queue, self))
        proc.daemon = True
        proc.start()

class ProductionManager(object):
    def __init__(self, producer_gen):
        # producer_gen : requirement -> generator
        self._producers = {}
        self._prod_gen = producer_gen
        self._consumers = []
    def create_consumer(self, cons):
        conns = []
        for req in cons.reqs:
            try:
                prod = self._producers[req]
            except:
                prod = Producer([], self._prod_gen(req))
                self._producers[req] = prod
            i_pipe, o_pipe = multiprocessing.Pipe()
            prod.add_conn(i_pipe)
            conns.append(o_pipe)
        self._consumers.append(Consumer(cons.consume(PipeCombiner(conns))))
    def start_production(self):
        for req, prod in self._producers.items():
            prod.start(req)
        output_queue = multiprocessing.Queue()
        for cons in self._consumers:
            cons.output_to_queue(output_queue)
        return output_queue

if __name__ == "__main__":
    def producer(out_p):
        for i in range(10000):
            time.sleep(.2)
            v = (i ** 2, i)
            print("sending", v)
            out_p.send( (i ** 2, i) )

    in_1, out_1 = multiprocessing.Pipe()
    in_2, out_2 = multiprocessing.Pipe()

    combiner = PipeCombiner([out_1, out_2])
    prod1 = multiprocessing.Process(target=producer, args=(in_1,))
    prod1.start()
    prod2 = multiprocessing.Process(target=producer, args=(in_2,))
    prod2.start()
    for i in combiner:
        print("combining",i)

