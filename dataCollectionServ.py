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
	DEVICEID = jData['Device ID']
	operator = jData['Operator']
	HTMLUSRAGTMOD = jData['USER Agent Modified']
	NATPRESENT = jData['NAT Present']
	TCPRSTCLSDPORT = jData['TCP RESET on 8081']
	HTML404MOD = jData['HTTP 404 Modified']
	HTMLCUSTHOST = jData['HTTP custom Host']
	TCPIPFLIP = jData['IP Flipping']
	IPADDR = jData['IP']
        LATITUDE = jData['Latitude']
        LONGITUDE = jData['Longitude']

        c.execute('''insert into operatorsurvey (DeviceID,operator, IP, LONGITUDE, LATITUDE, NAT_PRESENT, TCP_RSTCLSDPORT, HTML_404MOD,HTML_CUSTHOST, TCP_IPFLIP, HTTP_USRAGTMOD) values(?,?,?,?,?,?,?,?,?,?,?)''',(DEVICEID, operator,IPADDR,LONGITUDE, LATITUDE,  NATPRESENT, TCPRSTCLSDPORT, HTML404MOD, HTMLCUSTHOST,TCPIPFLIP, HTMLUSRAGTMOD))
	conn.commit()
	print(jData)
	self.request.sendall("Hello praveen")

if __name__ == "__main__":
    c.execute('''CREATE TABLE if not exists operatorsurvey (DeviceID text,
					      operator text, 
					      IP text,
                                              LONGITUDE real,
                                              LATITUDE real,
                                              NAT_PRESENT boolean,
                                              TCP_RSTCLSDPORT boolean,
                                              HTML_404MOD boolean,
                                              HTML_CUSTHOST boolean,
                                              TCP_IPFLIP boolean,
                                              HTTP_USRAGTMOD boolean)''')
    port = 1234
    dataserver = SocketServer.TCPServer(('',port),dataCollHandler)
    print("Running server")
    dataserver.serve_forever()
