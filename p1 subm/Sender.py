import sys
import getopt

import Checksum
import BasicSender

'''
This is a skeleton sender class. Create a fantastic transport protocol here.
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
    
    def start(self):
        self.msg = self.infile.read(1400)
        while not self.done:
            self.sendpackets()
            response = self.receive(.5)
            self.handle_response(response)
        return

        
    def handle_response(self,response_packet):
        if Checksum.validate_checksum(response_packet):
            if self.debug: print "recv: %s" % response_packet
        else:
            if self.debug: print "recv: %s <--- CHECKSUM FAILED" % response_packet
            return
        pieces = response_packet.split('|')
        cackno = int(pieces[1])
        if self.debug: print "CACK: ", cackno
        if (self.last_seqno and cackno > self.last_seqno):
            self.done = True
            return
        if cackno > self.window_seqno:
            for j in range(self.window_seqno, cackno):
                del self.packets[j]
            self.window_seqno = cackno
    
    def sendpackets(self):
        for seqno in range(self.window_seqno, self.window_seqno + 5):
            value = self.packets.get(seqno)
            if value: 
                hashed_msg_type = value[0]
                hashed_msg = value[1]
                packet = self.make_packet(hashed_msg_type, seqno, hashed_msg)
                self.send(packet)
                if self.debug: print "resent: ", self.strPacketInfo(packet)
                #stop looking when we hit the end
                if self.msg_type == 'end':
                    break
            # after we find and hash the end packet, we never enter this block again
            else:
                next_msg = self.infile.read(1300)
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
