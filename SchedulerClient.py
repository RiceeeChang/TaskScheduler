# --------------------------------------------------
# python version: 3.4.2
# a http client 
# send json file in request to server
# 
# --------------------------------------------------

import http.client # http module for python3
import json

class SchedulerClient(object):

    def __init__(self, ip, port):
        self.ip   = ip
        self.port = port


    # ------------------------------------
    # project is a dictionary.
    #
    #
    # ------------------------------------

    def sendProjectToScheduler(self, project): 

        connection = http.client.HTTPConnection(self.ip, self.port)
        headers = {'Content-type' : 'application/json'} 
        json_project = json.dumps(project)

        try:
            connection.request('POST', '', json_project, headers)
            response = connection.getresponse()
            print(response.read().decode())
            connection.close()
        except http.client.BadStatusLine:
            print ("Server something wrong probably")
        return

if __name__ == '__main__':
    client = SchedulerClient('127.0.0.1', 5566)

    with open('JSON/project.json', 'r+') as datafile:
        project = json.load(datafile)

    client.sendProjectToScheduler(project)