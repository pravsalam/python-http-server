import httplib
import urllib
import ast
# this program takes the file name, checks on the server if the file present or not
#if the file is present, the user is allowed to either delete or modify the file
#if the file is not present, user can create the file, update and delete options are hidden
while True:
    fname = raw_input("Enter filename:")
    url = 'http://localhost:8080/?filename=%s' %fname
    url = url+'&command=fetch'
    conn = httplib.HTTPConnection("localhost:8080")
    #check if file is present on server
    conn.request("GET","/?filename=%s&command=fetch" %fname)
    res = conn.getresponse()
    if res.status == 200:
        #file is present on server, offer user contextual menu
        data = res.read()
        servdata = ast.literal_eval(data)
        print("File present on server")
        cmd = raw_input("please type [update|delete]:")
        newdict = {}
        if cmd == 'update':
            print(" Press enter to take default values")
            for key in servdata:
                if(key!='filename' and key !='command'):
                    newvalue = raw_input("New value for %s [%s]:" %(key, servdata[key]))
                    if newvalue!='':
                        newdict[key]=newvalue
            #create a get url to send command to server
            url=""
            url=url+"/?filename=%s&command=update"%fname
            for key in newdict:
                url= url+"&%s=%s"%(key, newdict[key])
            conn.request("GET",url)
            updateres = conn.getresponse()
            if updateres.status == 200:
                #update on server was successful
                print ("File modified successfully")
                newdata = updateres.read()
                updateddata = ast.literal_eval(newdata)
                print("%s Contents:"%fname)
                for key in updateddata:
                    if( key != 'filename' and key !='command'):
                        print("%s: %s"%(key,updateddata[key][0]))
            else:
                print(" Internal error, Unable to modify the file")
        if cmd == 'delete':
            #create delete command url
            url=""
            url=url+"/?filename=%s&command=delete"%fname
            conn.request("GET",url)
            delres = conn.getresponse()
            if delres.status == 200:
                print("File deleted successfully")
            else:
                print("File could not be deleted")
    else:
        #file is not present on server, take custom fields and create a new file on server
        userdata={}
        print("New file will be created on server")
        data = raw_input("field1: ")
        userdata['field1']=data
        data = raw_input("field2: ")
        userdata['field2']=data
        data = raw_input("field3: ")
        userdata['field3'] = data
        #creating a GET url
        url=""
        url = url+"/?filename=%s&command=create"%fname
        for key in userdata:
            url=url+"&%s=%s"%(key,userdata[key])
        conn.request("GET",url)

        createres = conn.getresponse()
        if createres.status == 200:
            print(" File was successfully created on server")
        createddata = createres.read()
        createdict = ast.literal_eval(createddata)
        print("%s Contents:"%fname)
        for key in createdict:
            if(key!= 'filename' and key!='command'):
                print("%s: %s"%(key,createdict[key][0]))
