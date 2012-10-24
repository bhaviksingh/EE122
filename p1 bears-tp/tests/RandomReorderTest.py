import random

from BasicTest import *

"""
This tests random packet reordering. We randomly decide to start reordering
packets that go through the forwarder in either direction. In this case,
"true" stands for reordering that of currently inside in_queue and "false" 
stands for otherwise. The packets are instead added to another buffer list,
which when filled to over the set max_capacity, are sent to the out_queue.

Note that to implement this we just needed to override the handle_packet()
method -- this gives you an example of how to extend the basic test case to
create your own.
"""
class RandomReorderTest(BasicTest):
    def __init__(self, forwarder, input_file):
        BasicTest.__init__(self, forwarder, input_file)
        self.max_capacity = 4
        self.buffer_list = []
        self.myname = "RandomReorderTest"

    def handle_packet(self):
        if random.choice([True, False]):
            for p in self.forwarder.in_queue:
                self.buffer_list.append(p)
            if len(self.buffer_list) > self.max_capacity:
                random.shuffle(self.buffer_list)
                #print "REORDER: "+str(self.buffer_list)
                for bp in self.buffer_list:
                    self.forwarder.out_queue.append(bp)
                self.buffer_list = []
        else:
            for p in self.forwarder.in_queue:
                self.forwarder.out_queue.append(p)


        # empty out the in_queue
        self.forwarder.in_queue = []
