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
                    self.wfile.write(content)
                elif self.path == '/getdata':
                    self.send_response(200)
                    self.end_headers()
                    #self.wfile.write("file not found")
                    self.wfile.write(getJsonObject())
                elif self.path == '/getgeodata':
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(getgeodata())
                elif self.path == '/getOperatorStats':
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(getOperatorStats())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write("File Not found")
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
    

from BaseHTTPServer import HTTPServer
server = HTTPServer(('',80),httpstandardserver)
print(" Starting http server")
try:
        server.serve_forever()
except KeyboardInterrupt:
        pass
server.server_close()

