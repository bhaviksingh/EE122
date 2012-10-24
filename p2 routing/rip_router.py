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
        self.routingTable = {} #routingTable = { 'a' : {'a':1 , 'b': 2}, 'b': {'b':1 , 'c':2}}
        self.minCosts = {}
        self.ports = {}

    def handle_rx (self, packet, port):

		def update_min_costs():
			"""This function generates destDict from routingTable (basically the same as routingTable but ordered by destination)
			it is current HIGHLY inefficient, costing O(n^2) time. fix it maybe? """
			preChange = self.minCosts.copy()
			#print "premin = ", preChange
			destDict = {}
			for row in self.routingTable: #each row is the neighbour
			    for dest in self.routingTable[row]: #the dictionary has a whole bunch of "dest, cost" values
			        cost = self.routingTable[row][dest]
			        if destDict.has_key(dest):
			            lst = destDict[dest]
			            lst.append((row,cost))
			            destDict[dest] = lst # through row, costing cost
			        else:
			            destDict[dest] = [(row,cost)]

			for dest in destDict: #destdict is each destination and the cost to get through it, and who its through
				self.minCosts[dest] = min(destDict[dest], key=lambda x:x[1])
			#print " mincosts is ", self.minCosts,  "changed  = ", preChange != self.minCosts
			return preChange != self.minCosts

		def gen_update(to):
			""" Takes minCosts and generates a routingUpdate from it, specific to the "to" destination"""
			updatePacket = RoutingUpdate()
			for dest in self.minCosts: #for each dest
				if dest != to: # if its not where im sending
					updatePacket.add_destination(dest, self.minCosts[dest][1])
			return updatePacket

    	
		#main body	
		print self, " got ", packet, " at ", port

		if hasattr(packet, 'is_link_up'): #delivery

			self.ports[packet.src] = port #how to get to my neighbours
			if packet.is_link_up:
				self.routingTable[packet.src] =  {packet.src: 1}
			else:
				if not self.routingTable.has_key(packet.src): #todo: remove
					print "OMGWTFF"
				self.routingTable.pop(packet.src) 

		elif hasattr(packet, 'paths'): #update packets
			print "Routing update is ", packet.str_routing_table();
			for dest in packet.all_dests():
				throughSrc = self.minCosts[packet.src][1] + packet.get_distance(dest)
				if not self.routingTable[packet.src].has_key(dest): #no info for dest through src
					self.routingTable[packet.src] = {dest: throughSrc}
				elif throughSrc < self.routingTable[packet.src][dest]: #cost to dest through src has changed
					self.routingTable[packet.src][dest] = throughSrc

		else: 
			if self.minCosts.has_key(packet.dst):
				print "Trying to send to ", packet.dst, " through ", self.minCosts[packet.dst]
				self.send(packet, self.ports[self.minCosts[packet.dst][0]]) # data packet, send it through the least cost port


		if update_min_costs(): #regenerate the mincost table, returns true if its changed
			for outport in self.ports: #each of my neighbours
				updatePacket = gen_update(outport)
				#print "sending ,", updatePacket.str_routing_table(), " to ", self.ports[outport]
				if len(updatePacket.all_dests()) > 0:
					self.send(updatePacket, self.ports[outport]) #send an update
		
		print "routing table is ", self.routingTable
		print "mincost table is ", self.minCosts
		print ""
