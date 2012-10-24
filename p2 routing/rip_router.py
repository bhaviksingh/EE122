from sim.api import *
from sim.basics import *

'''
Create your RIP router in this file.
TODO:	break ties with router ID 
		implement implicit withdrawl
		implement poision reverse and split horizon??
'''
class RIPRouter (Entity):
    def __init__(self):
        # Add your code here!
        self.routingTable = {}
        self.minCosts = {}
        self.ports = {}

    def handle_rx (self, packet, port):

        #returns numerical value of the minimum cost to destination dest
        def min_cost(dest):
        	destTable = self.routingTable[dest]
        	return destTable[min(destTable, key=destTable.get)]

        #discovery packet
        if hasattr(packet, 'is_link_up'):
        	print "Discovery packet: ", packet, " at: ", self, " on port ", port
        	if packet.is_link_up:
        		# so i know how to get to my neighbours
        		self.ports[packet.src] = port
        		#there may need to be more error checks for this line
        		self.routingTable[packet.src] = {packet.src : 1}
	    		updatePacket = RoutingUpdate()
	    		updatePacket.add_destination(packet.src, self.routingTable[packet.src][packet.src])
	    		self.send(updatePacket, port, flood=True)
	    		print "Sending updatepacket ", updatePacket.str_routing_table()
        	else:
        		print "Down link"
        		


        #routingupdate packet
        elif hasattr(packet, 'paths'):
        	print "Routingupdate packet: ", packet, " at: ", self, " on port ", port
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
        		print "Sending updatepacket ", updatePacket.str_routing_table()
        
        #if its a data packet, just send it to the router who i know will give me the shortest distance (decrement hops also?)
    	else:
        	print "Data packet: ", packet, " at: ", self, " on port ", port
	        destination = min(self.routingTable[packet.dst], key=self.routingTable[packet.dst].get)
   	    	self.send(packet, self.ports[destination])

        print  self, " TABLE is ", self.routingTable
        print ""
