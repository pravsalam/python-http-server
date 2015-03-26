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
        if "Test-Type" in reqHeaders.keys():
            testType = reqHeaders['Test-Type']
        #if there was a middlebox HTTP standard suggest to include via header field
        if testType == "HeaderTest":
            HttpProxy = checkHeaderManipulation(reqHeaders)
            self.send_response(200)
            self.end_headers()
            if not HttpProxy:
                #Headers were not manipulated

                self.wfile.write("HTTP_HEADER_OK")
            else:
                #Headers were manipulated
                self.wfile.write("HTTP_HEADER_MANIPULATED")


    def checkHeaderManipulation(self,headers):
        knownUserAgents =['TEST']
        if 'Via' in reqHeaders.keys():
			return True
		#check the user agent string, if it is not TEST, then it is modified by http proxy
        for uagent in knownUserAgents:
            if uagent not in reqHeaders['User-Agent']:
                return True
        return False


from BaseHTTPServer import HTTPServer
server = HTTPServer(('',8080),middleboxHttphandler)
print(" Starting middlebox server")
server.serve_forever()
