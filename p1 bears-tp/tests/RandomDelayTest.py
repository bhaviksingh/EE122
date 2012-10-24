import random
import time

from BasicTest import *

"""
This tests random packet delays. We randomly decide to delay about half of the
packets that go through the forwarder in either direction. The delay time ranges
from 0 to 1 second (1000ms).

Note that to implement this we just needed to override the handle_packet()
method -- this gives you an example of how to extend the basic test case to
create your own.
"""
class RandomDelayTest(BasicTest):
    def __init__(self, forwarder, input_file):
        BasicTest.__init__(self, forwarder, input_file)
        self.myname = "RandomDelayTest"

    def handle_packet(self):
        for p in self.forwarder.in_queue:
            if random.choice([True, False]):
                random_delaytime = random.randrange(1000)/1000.0
                #print "Packet delayed: "+str(random_delaytime)
                time.sleep(random_delaytime)
            self.forwarder.out_queue.append(p)

        # empty out the in_queue
        self.forwarder.in_queue = []
