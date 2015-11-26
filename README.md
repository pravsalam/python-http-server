Running server: There are three python scripts developed for the purpose of testing and capturing the results. These scripts are tested with python 2.7. All the three scripts should be running to successfully perform all tests in the Android application.

server.py: This is the main script that reads most of the incoming HTTP requests. This script does not need root permission and can be run as “ python server.py”. 

httpserver.py: this script opens port 80, so it requires root privelages to run. It can be run as “ sudo python httpserver.py”

dataCollectionServ.py: This scripts logs all the results and listens on port 1234. It does not require root privileges and can be run as “python dataCollectionServ.py”
