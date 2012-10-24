from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
'''
class RIPRouter (Entity):
    def __init__(self):
        # Add your code here!
        self.routingTable = {}
        self.ports = {}

    def handle_rx (self, packet, port):

        #returns numerical value of the minimum cost to destination dest
        def min_cost(dest):
        	destTable = self.routingTable[dest]
        	return destTable[min(destTable, key=destTable.get)]

        #discovery packet
        if hasattr(packet, 'is_link_up'):
        	print "Discovery packet: ", packet
        	if packet.is_link_up:
        		# so i know how to get to my neighbours
        		self.ports[packet.src] = port

        		# initialize neighbour information, a lot of this code should be cleaned up! (error checks)
        		if self.routingTable.has_key(packet.src):
        			print "if this statement prints wtf is happening " , packet, self.routingTable
        			self.routingTable[packet.src][packet.src] = 1
        		else:
        			self.routingTable[packet.src] = {packet.src : 1}

	    		if self.routingTable[packet.src][packet.src] != 1:
	    			print "this shouldnt be happening either" , packet, self.routingTable

	    		updatePacket = RoutingUpdate()
	    		updatePacket.add_destination(packet.src, self.routingTable[packet.src][packet.src])
	    		self.send(updatePacket, port, flood=True)
        	return

        #routingupdate packet
        if hasattr(packet, 'paths'):
        	print "Routingupdate packet: ", packet
        	destinations = packet.all_dests();
        	updatePacket = RoutingUpdate()
        	for dest in destinations:
        		throughSrc = min_cost(packet.src) + packet.get_distance(dest)
        		#if i dont have any info on how to get to dest, add info for it, going through packet.src
        		if not self.routingTable.has_key(dest):
        			self.routingTable[dest] = { packet.src : throughSrc}
        			updatePacket.add_destination(dest, throughSrc)
        		#if i have info on how to get to it, only update things if the path through packet.src is shorter
        		elif  throughSrc < min_cost(dest):
        			self.routingTable[dest][packet.src] =  throughSrc
	        		updatePacket.add_destination(dest, throughSrc)
	        #send out an update packet if something is changed
	        if (len(updatePacket.all_dests()) >0):
        		self.send(updatePacket, port, flood = True)
        	return
        
        #if its a data packet, just send it to the router who i know will give me the shortest distance (decrement hops also?)
        destination = min(self.routingTable[packet.dst], key=self.routingTable[packet.dst].get)
        self.send(packet, self.ports[destination])
