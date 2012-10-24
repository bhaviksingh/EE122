import random

from BasicTest import *

"""
This tests random packet corruption. We randomly decide to corrupt about half 
of the packets that go through the forwarder in either direction. The "true" 
case here is for the corruption, as opposed to the other "false" case for 
dropping packets in RandomDropTest. The amount of corruption is uniformly 
distributed across the packet's data contents, and the corruption symbol is 
from the same body of the packet's data contents. In the case of the sequence 
number, a random number from 0 to 99 replaces it.

Note that to implement this we just needed to override the handle_packet()
method -- this gives you an example of how to extend the basic test case to
create your own.
"""
class RandomCorruptTest(BasicTest):
    def __init__(self, forwarder, input_file):
        BasicTest.__init__(self, forwarder, input_file)
        self.myname = "RandomCorruptTest"

    def handle_packet(self):
        for p in self.forwarder.in_queue:
            if random.choice([True,False]):
                #choose a random number n from 0 to 9 and apply this n times
                num_times = random.randrange(10)
                #corrupt the data)
                if len(p.data) > 0:
                    for i in range( num_times ):
                        rand_index = random.randrange(len(p.data))
                        corrupt_index = random.randrange(len(p.data))
                        p.data = p.data.replace( p.data[rand_index], p.data[corrupt_index] )
                #corrupt the message type
                if len(p.msg_type) > 0:
                    for i in range( num_times ):
                        rand_index = random.randrange(len(p.msg_type))
                        corrupt_index = random.randrange(len(p.msg_type))
                        p.msg_type = p.msg_type.replace( p.msg_type[rand_index], p.msg_type[corrupt_index] )
                #corrupt the sequence number
                for i in range( num_times ):
                    p.seqno = random.randrange(100)

            self.forwarder.out_queue.append(p)

        # empty out the in_queue
        self.forwarder.in_queue = []
