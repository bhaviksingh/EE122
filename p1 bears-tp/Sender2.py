import sys
import getopt

import Checksum
import BasicSender

'''
VARIABLE SIZE SLIDING WINDOW EXTRA CREDIT
'''

class Sender(BasicSender.BasicSender):

    def __init__(self,dest,port,filename,debug=False):
        super(Sender, self).__init__(dest,port,filename,debug=False)
        self.window_seqno = 0
        # dictionary [ key = seqno. value = (msg_type, packet) tuple ]
        self.packets = {}
        self.msg = None
        self.last_seqno = None
        self.msg_type = None
        self.done = False
        self.window_size = 5
        
    def start(self):
        self.msg = self.infile.read(500)
        while not self.done:
            self.sendpackets()
            lastresponse = None
            while True:
                response = self.receive(.5)
                if not response or response == lastresponse:
                    break
                lastresponse = response
            self.handle_response(lastresponse)
        return
        
    def handle_response(self,response_packet):
        if Checksum.validate_checksum(response_packet):
            if self.debug: print "recv: %s" % response_packet
        else:
            if self.debug: print "recv: %s <--- CHECKSUM FAILED" % response_packet
            return
        pieces = response_packet.split('|')
        cackno = int(pieces[1])
        if (self.last_seqno and cackno > self.last_seqno):
            self.done = True
            if self.debug: print "DONE WITH TRANSFER"
            return
        if cackno > self.window_seqno:
            for j in range(self.window_seqno, cackno):
                del self.packets[j]
            if cackno > (self.window_seqno + self.window_size - 1):
                self.window_size += 1
            self.window_seqno = cackno
        else:
            if self.window_size > 5:
                self.window_size -= 1
            
    
    def sendpackets(self):
        if self.debug: print "window size: ", self.window_size
        for seqno in range(self.window_seqno, self.window_seqno + self.window_size):
            value = self.packets.get(seqno)
            if value:
                hashed_msg_type = value[0]
                hashed_msg = value[1]
                packet = self.make_packet(hashed_msg_type, seqno, hashed_msg)
                self.send(packet)
                if self.debug: print "resent: ", self.strPacketInfo(packet)
                #stop looking when we hit the end
                if hashed_msg_type == 'end':
                    break
            # after we find and hash the end packet, we never enter this block again
            else:
                next_msg = self.infile.read(500)
                self.msg_type = 'data'
                if seqno == 0:
                    self.msg_type = 'start'
                elif next_msg == "":
                    self.msg_type = 'end'
                self.packets[seqno] = self.msg_type, self.msg
                packet = self.make_packet(self.msg_type, seqno, self.msg)
                self.send(packet)
                if self.debug: print "sent: ", self.strPacketInfo(packet)
                self.msg = next_msg
                if self.msg_type == 'end':
                    self.last_seqno = seqno
                    break

    def strPacketInfo(self, packet):
        msg_type, seqno, data, checksum = self.split_packet(packet)
        return "%s|%d||%s" %(msg_type,int(seqno),checksum)



'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    def usage():
        print "BEARS-TP Sender"
        print "-f FILE | --file=FILE The file to transfer; if empty reads from STDIN"
        print "-p PORT | --port=PORT The destination port, defaults to 33122"
        print "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        print "-d | --debug Print debug messages"
        print "-h | --help Print this usage message"

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                               "f:p:a:d", ["file=", "port=", "address=", "debug="])
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False

    for o,a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True

    s = Sender(dest,port,filename,debug)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
