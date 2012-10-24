EE 122 Fall 2012
Project 1

Partners:
=======================
Eugene Huang (ee122-en)
Bhavik Singh (ee122-js)

Sender.py challenges
=====================

Implementation of the Sender class was relatively straightforward, but we ran into a few issues.

1. The first was how to resend packets. In our implementation packets are being read in from a stream. Once we read in one packet of data from the stream and sent it, if the sending failed and we needed to resend there was no way to re-access the stream to get the data. Thus we began hashing (or storing) packets that we were sending, and if a packet had to be resent, its data would be read from the hash. We also delete all elements from the hash that are not required, ie: all items in the hash for whom we've received an ack for.

2. The second was dealing with packets near the end of the data stream. Once we've sent the last packet, we need to make sure we received an ack for it. If we didn't receive an ack, we move the window up to the last packet whose ack was received, send it and send 5 packets after it. However you run into an issue if your ack was within the last 5 packets (eg: the second last packet) and this needs to be dealt with carefully.


Extra credit
=============

1. Dynamic sliding window: Sender2.py
The size of the sliding window was a static 5. We made it so this size can be decreased and increased dynamically based on the network condition. Our judge of network condition was how many packets go through. If all the packets in the current window go through, this means the network condition is good, so increase the window size by 1. If some packets were dropped, then we decrease the window size, lower bounded by 5. We noticed that the window sizes increases up to 9 for BasicTest, but for other tests where drops were more often, it only increased up to 6 or 7.

2. Variable round-trip time: Sender3.py
The time we wait for a receive to timeout was a static .5 seconds (500ms). For the extra credit, we made it so that this value can be changed based on the actual time taken to send a packet and receive a response. Thus the timeout value = average(timeoutvalue + roundtriptime). We saw that this timeout correctly gets reduced for BasicTest, but for cases such as randomTest, this timeout becomes longer. This is because the round-trip-time in the latter case is higher due to dropped/corrupted packets.

