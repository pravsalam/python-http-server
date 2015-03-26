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
		knownUserAgents =['TEST']
		print(self.headers)
		reqHeaders = self.headers
		#if there was a middlebox HTTP standard suggest to include via header field
		if 'Via' in reqHeaders.keys():
			HttpProxy = True
		#check the user agent string, if it is not TEST, then it is modified by http proxy
		for uagent in knownUserAgents:
			if uagent not in reqHeaders['User-Agent']:
				HttpProxy = True
				
		(client_ip, client_port)=self.client_address
		print(client_ip)
		print(self.path)
		parsed_data = urlparse.urlparse(self.path)
		print(parsed_data.query)
        	#get the query data and parse them into a dictionary
		cdata_dict = urlparse.parse_qs(parsed_data.query)
		androidId = cdata_dict['unique_id'][0]
		cellularOperator = cdata_dict['network_operator'][0]
		clientLocalIp = cdata_dict['local_ip'][0]
		#prepare response dictionary to return as json
		if clientLocalIp != client_ip:
			NatProxy = True
		if HttpProxy:
			print("Http Proxy Found")
			responseDict['HttpProxy'] ='yes'
		else:
			responseDict['HttpProxy'] = 'no'
		responseDict['NatProxy'] = {}
		if NatProxy:
			print("Nat Proxy present")
			responseDict['NatProxy']['NatPresent']='yes'
			responseDict['NatProxy']['clientIp']=client_ip
			responseDict['NatProxy']['clientPort'] = client_port
			
		else:
			responseDict['NatProxy']['NatPresent']='no' 
		print(responseDict)
		json_string = json.dumps(responseDict)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(json_string)


from BaseHTTPServer import HTTPServer
server = HTTPServer(('',8080),middleboxHttphandler)
print(" Starting middlebox server")
server.serve_forever()
