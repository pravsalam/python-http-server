import urlparse
import BaseHTTPServer
import json
import os
import random
import sqlite3
import gviz_api
#from collections import OrderedDict
content= open('index3.html').read()

class httpstandardserver(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
		print(self.headers)
		(client_ip, client_port)=self.client_address
                #self.send_response(200)
                #self.end_headers()
                #self.wfile.write(self.path)
                if self.path == '/' or self.path == '/index.html':
                    self.send_response(200)
                    self.end_headers()
                    print "What am i waiting for \n"
                    self.wfile.write(content)
                    print "I have sent content to client\n"
                elif self.path == '/getdata':
                    print "getdata called\n"
                    self.send_response(200)
                    self.end_headers()
                    #self.wfile.write("file not found")
                    self.wfile.write(getJsonObject())
                    print "sent content to client\n"
                elif self.path == '/getgeodata':
                    print "getgeodata called\n"
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(getgeodata())
                    print "sent content to client\n"
                elif self.path == '/getOperatorStats':
                    print "get operators stats called\n"
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(getOperatorStats())
                    print "sent content to client\n"
                elif self.path == '/getUserTestStats':
                    print "get user test stats"
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(getUserTestStats())
                    print "sent content to client\n"
                elif self.path == '/getTestsHistogram':
                    print "get test histogram"
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(getTestsHistogram())
                    print "sent content to client\n"
                else:
                    print "unknown path"
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write("File Not found")
                    print "sent content to client\n"
def getJsonObject():
    conn = sqlite3.connect('middlebox.db')
    DataTable ={}
    DataTable['cols'] =[]
    #columns_list =[]
    #column_info = OrderedDict()
    column_info={}
    column_info['id']=""
    column_info['label'] = "Nat Present"
    column_info['type'] ="string"
    #columns_list.append(column_info)
    #print column_info
    DataTable['cols'].append(column_info)
    column_info = {}
    column_info['id'] = ""
    column_info['label'] = "count"
    column_info['type'] = "number"
    #print column_info
    #columns_list.append(column_info)
    DataTable['cols'].append(column_info)
    
    #print columns_list
    cursor = conn.execute("select NAT_PRESENT,count(*) as count  from operatorsurvey group by NAT_PRESENT ")
    #DataTable['cols'] = columns_list
    DataTable['rows'] = []
    #row_info={}
    for row in cursor:
        print row[0], row[1]
        row_info={}
        row_info['c'] = []
        column_info ={}
        if row[0] == 0:
            #column_info = {}
            column_info['v']='NAT not Present'
            row_info['c'].append(column_info)
            column_info ={}
            column_info['v'] = str(row[1])
            row_info['c'].append(column_info)
        elif row[0] == 1:
            #column_info = {}
            column_info['v']='NAT Present'
            row_info['c'].append(column_info)
            column_info ={}
            column_info['v'] = str(row[1])
            row_info['c'].append(column_info)
        DataTable['rows'].append(row_info)
    print DataTable
    return json.dumps(DataTable,ensure_ascii = False)
    #return json.dumps(['foo', {'bar': ['baz', None, 1.0, 2]}])
def getgeodata():
    conn = sqlite3.connect('middlebox.db')
    cursor = conn.execute("select LONGITUDE as long, LATITUDE as lat, operator from operatorsurvey")
    DataTable ={}
    DataTable['cols'] =[]

    column_info={}
    column_info['id']=""
    column_info['label'] = "Lat`"
    column_info['type'] ="number"
    #columns_list.append(column_info)
    #print column_info
    DataTable['cols'].append(column_info)
    column_info = {}
    column_info['id'] = ""
    column_info['label'] = "Long"
    column_info['type'] = "number"
    #print column_info
    #columns_list.append(column_info)
    DataTable['cols'].append(column_info)
    column_info = {}
    column_info['id'] = ""
    column_info['label'] = "operator"
    column_info['type'] = "string"
    #print column_info
    #columns_list.append(column_info)
    DataTable['cols'].append(column_info)

    DataTable['rows'] = []
    #row_info={}
    for row in cursor:
        print row[0], row[1]
        row_info={}
        row_info['c'] = []
        column_info ={}
        #column_info = {}
        column_info['v']=row[1]
        row_info['c'].append(column_info)
        column_info ={}
        column_info['v'] = row[0]
        row_info['c'].append(column_info)
        column_info ={}
        column_info['v'] = row[2]
        row_info['c'].append(column_info)

        DataTable['rows'].append(row_info)
    print DataTable
    return json.dumps(DataTable,ensure_ascii = False)
def getOperatorStats():
    conn = sqlite3.connect('middlebox.db')
    DataTable ={}
    DataTable['cols'] =[]
    #columns_list =[]
    #column_info = OrderedDict()
    column_info={}
    column_info['id']=""
    column_info['label'] = "Network"
    column_info['type'] ="string"
    #columns_list.append(column_info)
    #print column_info
    DataTable['cols'].append(column_info)
    column_info = {}
    column_info['id'] = ""
    column_info['label'] = "Tests Performed"
    column_info['type'] = "number"
    #print column_info
    #columns_list.append(column_info)
    DataTable['cols'].append(column_info)
    
    #print columns_list
    cursor = conn.execute("select operator,count(*) as count  from operatorsurvey group by operator ")
    #DataTable['cols'] = columns_list
    DataTable['rows'] = []
    #row_info={}
    for row in cursor:
        print row[0], row[1]
        row_info={}
        row_info['c'] = []
        column_info ={}
        #column_info = {}
        column_info['v']=row[0]
        row_info['c'].append(column_info)
        column_info ={}
        column_info['v'] =row[1]
        row_info['c'].append(column_info)
        DataTable['rows'].append(row_info)
    print DataTable
    return json.dumps(DataTable,ensure_ascii = False)
def getUserTestStats():
    conn = sqlite3.connect('middlebox.db')
    DataTable ={}
    DataTable['cols'] =[]
    #columns_list =[]
    #column_info = OrderedDict()
    column_info={}
    column_info['id']=""
    column_info['label'] = "Unique users"
    column_info['type'] ="number"
    #columns_list.append(column_info)
    #print column_info
    DataTable['cols'].append(column_info)
    column_info = {}
    column_info['id'] = ""
    column_info['label'] = "total tests"
    column_info['type'] = "number"
    #print column_info
    #columns_list.append(column_info)
    DataTable['cols'].append(column_info)
    
    #print columns_list
    cursor = conn.execute("select count(DeviceID),count(DISTINCT DeviceID) as count  from operatorsurvey")
    #DataTable['cols'] = columns_list
    DataTable['rows'] = []
    #row_info={}
    for row in cursor:
        print row[0], row[1]
        row_info={}
        row_info['c'] = []
        column_info ={}
        #column_info = {}
        column_info['v']=row[1]
        row_info['c'].append(column_info)
        column_info ={}
        column_info['v'] = row[0]
        row_info['c'].append(column_info)
        DataTable['rows'].append(row_info)
    print DataTable
    return json.dumps(DataTable,ensure_ascii = False)
def getTestsHistogram():
    conn = sqlite3.connect('middlebox.db')
    DataTable ={}
    DataTable['cols'] =[]
    #columns_list =[]
    #column_info = OrderedDict()
    natpresent = 0
    tcpreset = 0
    http404 =0
    customhost = 0
    tcpipflip = 0
    httpusragent = 0
    column_info={}
    column_info['id']=""
    column_info['label'] = "Test"
    column_info['type'] ="string"
    DataTable['cols'].append(column_info)
    column_info = {}
    column_info['id'] = ""
    column_info['label'] = "middlebox detected"
    column_info['type'] = "number"
    #print column_info
    #columns_list.append(column_info)
    DataTable['cols'].append(column_info)
    
    cursor = conn.execute("select count(NAT_PRESENT)from operatorsurvey where NAT_PRESENT = 1")
    for row in cursor:
        natpresent = row[0]
        print natpresent
    cursor = conn.execute("select count(TCP_RSTCLSDPORT)from operatorsurvey where  TCP_RSTCLSDPORT= 1")
    for row in cursor:
        tcpreset= row[0]
    cursor = conn.execute("select count(HTML_404MOD)from operatorsurvey where  HTML_404MOD=1")
    for row in cursor:
        http404 = row[0]
    cursor = conn.execute("select count(HTML_CUSTHOST)from operatorsurvey where  HTML_CUSTHOST=1")
    for row in cursor:
        customhost = row[0]
    cursor = conn.execute("select count(TCP_IPFLIP)from operatorsurvey where  TCP_IPFLIP=1")
    for row in cursor:
        tcpipflip = row[0]
    cursor = conn.execute("select count(HTTP_USRAGTMOD)from operatorsurvey where  HTTP_USRAGTMOD=1")
    for row in cursor:
        tcpuseragent = row[0]
    DataTable['rows']=[]
    row_info={}
    row_info['c'] =[]
    column_info={}
    column_info['v'] = 'NAT Present'
    row_info['c'].append(column_info)
    column_info={}
    column_info['v'] = natpresent
    row_info['c'].append(column_info)
    DataTable['rows'].append(row_info)

    row_info={}
    row_info['c'] =[]
    column_info={}
    column_info['v'] = 'TCP Reset'
    row_info['c'].append(column_info)
    column_info={}
    column_info['v'] = tcpreset
    row_info['c'].append(column_info)
    DataTable['rows'].append(row_info)

    row_info={}
    row_info['c'] =[]
    column_info={}
    column_info['v'] = 'HTTP 404 Mod'
    row_info['c'].append(column_info)
    column_info={}
    column_info['v'] = http404
    row_info['c'].append(column_info)
    DataTable['rows'].append(row_info)

    row_info={}
    row_info['c'] =[]
    column_info={}
    column_info['v'] = 'Custom Host'
    row_info['c'].append(column_info)
    column_info={}
    column_info['v'] = customhost
    row_info['c'].append(column_info)
    DataTable['rows'].append(row_info)

    row_info={}
    row_info['c'] =[]
    column_info={}
    column_info['v'] = 'TCP IP Flip'
    row_info['c'].append(column_info)
    column_info={}
    column_info['v'] = tcpipflip
    row_info['c'].append(column_info)
    DataTable['rows'].append(row_info)

    row_info={}
    row_info['c'] =[]
    column_info={}
    column_info['v'] = 'user agent'
    row_info['c'].append(column_info)
    column_info={}
    column_info['v'] = tcpuseragent
    row_info['c'].append(column_info)

    DataTable['rows'].append(row_info)

    print DataTable
    return json.dumps(DataTable,ensure_ascii = False)
    

from BaseHTTPServer import HTTPServer
server = HTTPServer(('',80),httpstandardserver)
print(" Starting http server")
try:
        server.serve_forever()
except KeyboardInterrupt:
        pass
server.server_close()

