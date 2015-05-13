__author__ = 'praveenkumaralam'
import SocketServer
import json
import sqlite3
conn = sqlite3.connect('middlebox.db')
c = conn.cursor()
class dataCollHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print("Praveen")
        data = self.request.recv(4096).strip()
	startCurly = data.find('{')
        jsonString = data[startCurly:]
	print jsonString
        jData = json.loads(jsonString)
	AndroidId = jData['AndroidId']
	operator = jData['operator']
	if jData['HeaderModified'] == 'yes':
		headerMod = True
	else:
		headerMod = False
	if jData['NATProxy'] == 'yes':
		natProxy = True
	else: 
		natProxy = False
	if jData['IpFlipping'] == 'yes':
		ipFlipping = True
	else:
		ipFlipping = False
	if jData['TCP_RST'] == 'yes':
		tcpRst = True
	else:
		tcpRst = False
	if jData['Http404'] == 'yes':
		http404 = True
	else:
		http404 = False
	if jData['HeaderHost'] =='yes':
		headerHost = True
	else:
		headerHost = False
		
	
        c.execute('''insert into operatorsurvey (androidid,operator, nat_proxy, tcp_rst, hdr_mod,hdr_host, ip_flip, http_404_mod) values(?,?,?,?,?,?,?,?)''',(AndroidId, operator, natProxy, tcpRst, headerMod, headerHost,ipFlipping, http404))
	conn.commit()
        print(jData)
        self.request.sendall("Hello praveen")

if __name__ == "__main__":
    c.execute('''CREATE TABLE if not exists operatorsurvey (androidid text,
					      operator text, 
                                              nat_proxy text,
                                              tcp_rst boolean,
                                              hdr_mod boolean,
                                              hdr_host boolean,
                                              ip_flip boolean,
                                              http_404_mod boolean)''')
    port = 1234
    dataserver = SocketServer.TCPServer(('',port),dataCollHandler)
    print("Running server")
    dataserver.serve_forever()
