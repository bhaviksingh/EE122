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

    	def update_min_costs():
    		#this function is HIGHLY inefficient, costing O(n^2) time. fix it maybe?
    		preChange = self.minCosts
    		destDict = {}
    		for row in routingTable: #each row is the neighbour
    			for dest, cost in row: #the dictionary has a whole bunch of "dest, cost" values
    				if destDict.has_key(dest):
    					destDict[dest] = destDict.append((row,cost)) # through row, costing cost
    				else:
    					destDict[dest] = [(row,cost)]

    	    for dest in destDict: #destdict is each destination and the cost to get through it, and who its through
    	    	minCost[dest] = min(destDict[dest], key=lambda x:x[1])

    		return preChange == self.minCosts

    	def gen_update(to):
    		updatePacket = RoutingUpdate()
    		for dest, throughcost in minCosts: #for each dest
    			if dest != to: # if its not where im sending
    				updatePacket.add_destination(dest, throughcost[1])
    		return updatePacket

    	
    	#main body	
    	print self, " got ", packet, " at ", port

    	if has_attr(packet, 'is_link_up'): #delivery
    		self.ports[packet.src] = port #how to get to my neighbours
    		if packet.is_link_up:
    			routingTable[packet.src] =  {packet.src: 1}
    		else:
    			if not routingTable.has_key(packet.src): #todo: remove
    				print "OMGWTFF"
    			routingTable.pop(packet.src) 
       
    	elif has_attr(packet, 'paths'): #update packets
    		for dest in packet.all_dests():
    			throughSrc = minCosts[packet.src][1] + packet.get_distance(dest)
    			if not self.routingTable[packet.src].has_key(dest): #no info for dest through src
    				self.routingTable[packet.src] = {dest: throughSrc}
    			elif throughSrc < routingTable[packet.src][dest]: #cost to dest through src has changed
    				self.routingTable[packet.src][dest] = throughSrc

    	else: 
    		send(packet, self.ports[minCosts[packet.dst][0]]) # data packet, send it through the least cost port

    	if update_min_costs(): #regenerate the mincost table, returns true if its changed
    		for neighbour,port in self.ports: #each of my neighbours
    			updatePacket = gen_update(neighbour)
    			if len(updatePacket) > 0
    				send(updatePacket, port) #send an update
