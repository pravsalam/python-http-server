import urlparse
import BaseHTTPServer
import json
import os
import random
#This program works only on python version below 3, not on new version above 3
 #this program extends BaseHTTPRequestHandler and overrides the do_get command

class middleboxHttphandler(BaseHTTPServer.BaseHTTPRequestHandler):
    #@overide do_get
    def do_GET(self):
        HttpProxy = False
        NatProxy = False
        responseDict ={}
        testType = None
        print(self.headers)
        reqHeaders = self.headers
	parsed_data = urlparse.urlparse(self.path)
        (client_ip, client_port)=self.client_address
        cdata_dict = urlparse.parse_qs(parsed_data.query)
        androidId = cdata_dict['unique_id'][0]
        #cellularOperator = cdata_dict['network_operator'][0]
        clientLocalIp = cdata_dict['local_ip'][0]

        if "test-type" in reqHeaders.keys():
            testType = reqHeaders['Test-Type']
        #if there was a middlebox HTTP standard suggest to include via header field
        if testType == "HeaderTest":
            HttpProxy = self.checkHeaderManipulation(reqHeaders)
            self.send_response(200)
            self.end_headers()
            if not HttpProxy:
                #Headers were not manipulated

                self.wfile.write("HTTP_HEADER_OK")
            else:
                #Headers were manipulated
                self.wfile.write("HTTP_HEADER_MANIPULATED")
        elif testType == "Http404":
                self.send_response(404)
                self.end_headers()
                self.wfile.write("HTTP_404")
        elif testType == "NatTest":
	    responseDict['NatProxy'] = {}	
	    print clientLocalIp, client_ip
            if clientLocalIp != client_ip:
                print("Nat Proxy present")
		#responseDict['NatProxy'] = {}
                responseDict['NatProxy']['NatPresent']='Yes'
                responseDict['NatProxy']['clientIp']=client_ip
                responseDict['NatProxy']['clientPort'] = client_port
            else:
                print("Nat Proxy not present")
                responseDict['NatProxy']['NatPresent']='No'
            self.send_response(200)
            self.end_headers()
            json_string = json.dumps(responseDict)
            self.wfile.write(json_string)
	elif testType == "HeaderHostTest":
	    self.send_response(200)
            self.end_headers()
	    self.wfile.write("MIDDLEBOX_SERVER")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("HTTP_404")


    def checkHeaderManipulation(self,headers):
        knownUserAgents =['TEST']
        if 'via' in headers.keys():
			return True
	#check the user agent string, if it is not TEST, then it is modified by http proxy
        for uagent in knownUserAgents:
            if uagent not in headers['User-Agent']:
                return True
        return False

class httpstandardserver(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		print "Test HTTP standard server"
		self.send_response(200)
		self.end_headers()
		self.wfile.write("Http 80 reached")
	
from BaseHTTPServer import HTTPServer
server = HTTPServer(('',8080),middleboxHttphandler)
print(" Starting middlebox server")
server.serve_forever()

