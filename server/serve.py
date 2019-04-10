import socketserver
import os
import subprocess
import tempfile
import json

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def testResults(self, tmpdir):
        expected = []
        exp_file = open('./expected.json')
        for line in exp_file:
            expected.append(json.loads(line))

        actual = []
        act_file = open(tmpdir + '/eve.json')
        for line in act_file:
            l = json.loads(line)
            if l["event_type"] == "alert":
                actual.append(json.loads(line))

        actual_c = actual.copy()

        for act in actual:
            for exp in expected:
                count = 0
                for key in exp:
                    if act[key] == exp[key]:
                        count += 1
                if count == len(exp) and act in actual_c:
                    expected.remove(exp)
                    actual_c.remove(act)
       
        if len(actual_c) == 0 and len(expected) == 0:
            return True, None

        if len(actual_c) > 0:
            return False, "Too many alerts"

        return False, "Not enough alerts"

    def handle(self):
        self.request.sendall("Enter Rule(s):\n".encode())
        rules = self.request.recv(1024).strip().decode()

        tmpdir = tempfile.mkdtemp()
        tmp_rules = tmpdir + '/my.rules'
        open(tmp_rules, 'w').write(rules + '\n')

        pcap_folder = './pcaps'
        result = ""
        for pcap in os.listdir(pcap_folder):
            if os.path.isfile(os.path.join(pcap_folder, pcap)):
                pcap_f = os.path.join(pcap_folder, pcap)
                r = subprocess.run(['suricata', '-r', pcap_f, '-S', tmp_rules, '-l', tmpdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if r.stderr:
                    result += r.stderr.decode()

#        result += open(tmpdir + '/fast.log').read()

        pcap_test,result_resp = self.testResults(tmpdir)        
        if pcap_test:
            result += open('./flag.txt').read()
        else:
            result += result_resp + "\n"       

        self.request.sendall(result.encode())

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
