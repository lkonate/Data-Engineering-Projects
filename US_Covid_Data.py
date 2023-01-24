# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Creating Scalable Data Pipelines With Graph Animation Using AWS & Python  #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# The program retrieves covid data of the 10 most affected US states and display
# the corresponding histogram for visualization.


import json
import time
import pandas as pd

import boto3
import requests
from bs4 import BeautifulSoup
from sseclient import SSEClient

import datetime as dt
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.colors as pcl
from matplotlib.animation import FuncAnimation

#fig = plt.figure()
clrs = pcl.TABLEAU_COLORS
td = dt.date.today()
td = dt.date.strftime(td, "%m/%d/%Y")

def getAwsRes(region = 'us-east-1', qName = 'us-covid-data'):
    # Get the service resource
    client = boto3.client('sqs', region) # OK
    # Create the queue. This returns an SQS.Queue instance
    queue = client.create_queue(QueueName=qName, Attributes={'DelaySeconds': '5'})
    # Create an Amazon S3 Bucket
    s3 = boto3.client('s3')
    return client, queue, s3


class dataPipeline:
    def __init__(self, url, state_dik = {}):
        self.url = url
        self.x = []
        self.y = []
        self.state_dik = state_dik
        self.client = getAwsRes()[0]
        self.QueueUrl = getAwsRes()[1]['QueueUrl']
        self.s3 = getAwsRes()[2]
        #self.fig, (self.ax1, self.ax2) = plt.subplots(1,2, sharey =True)
        self.fig, self.ax = plt.subplots(1,1)

    def dataParser(self):
        try:
            res = requests.get(self.url, stream = True)
            soup = BeautifulSoup(res.text, features='lxml')
            stateList = soup.select("table")[0].select("tr")[2:]
        except:
            raise
        else:
            self.stateDicBuilder(stateList)
        self.msgQueuer(self.state_dik)

    def stateDicBuilder(self, stList):
            if stList:
                self.keyValueBuilder(stList)

    def keyValueBuilder(self, stList):
        try:
            for i, state in enumerate(stList[:-1]):
                tds = state.select("td")
                k = tds[1].select("a")[0].text # state 
                v = tds[4].text # number of deaths
                v = int(float(v.strip(',').strip().replace(',','')))
                self.state_dik[k] = v
        except:
            pass

    def msgQueuer(self, data):
        try:
            response = self.client.send_message(  #this returns a dictionary object
                QueueUrl = self.QueueUrl,
                DelaySeconds = 5, # delay each message by 5 sec 
                MessageBody = json.dumps(data)
            )
        except:
            raise
        else:
            #print('\t Message id %s added to queue' % response['MessageId'], sep='', end='', flush=True)        
            print('\t Message id %s added to queue' % response['MessageId'])        
        self.msgBatchReader()

    def msgBatchReader(self):
        try:
            response = self.client.receive_message( #this returns a dictionary object
                QueueUrl = self.QueueUrl,
                MaxNumberOfMessages=5, # max number of msgs in batch
                VisibilityTimeout=5,
                WaitTimeSeconds=5, # delay each message by 5 sec 
            )
        except:
            raise
            print('No data available yet; sys awaiting next message ...')
        else:
            self.msgBatchProcessor(response)

    def msgBatchProcessor(self, resp):
        body = resp['Messages'][0]['Body']
        bucket='covid-usa'
        key= resp['Messages'][0]['MessageId']
        receipthandle = resp['Messages'][0]['ReceiptHandle']
        try:
            response = self.s3.put_object(
                Bucket = bucket,
                Key= key, 
                Body= body,
                ACL='public-read' 
                )
        except:
            raise
        else:
            #print('\r%s file saved to aws repository...' % key, sep=' ', end='', flush=True)
            print('\r%s file saved to aws repository...' % key)
            time.sleep(2)
            print('Now plotting data of most affected US states')
            self.plotData()
            self.msgDeQueuer(receipthandle)

    def msgDeQueuer(self, handl):
        try:
            self.client.delete_message(
                QueueUrl = self.QueueUrl,
                ReceiptHandle = handl
            )
            print('msg dequeued')
        except:
            raise

    def plotData(self):
        self.state_dik = { k: self.state_dik[k] for k in sorted(self.state_dik, key= self.state_dik.get)[-10:]}
        self.dPlot()

    def dPlot(self):
        #self.ax1.plot(list(self.state_dik.keys()), list(self.state_dik.values()), color = 'r')
        self.ax.bar(list(self.state_dik.keys()), list(self.state_dik.values()), color = clrs)        
        plt.title("Covid Most affected US States as of {}".format(td))
        plt.xlabel("States")
        plt.ylabel("Death Tolls")
        plt.tick_params(rotation=30)
        plt.show()

if __name__ == '__main__':
    data_url = 'https://www.worldometers.info/coronavirus/country/us/'
    dppl = dataPipeline(data_url)
    dppl.dataParser()
