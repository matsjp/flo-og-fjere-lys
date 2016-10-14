import urllib.request
import datetime
import re
import time
import tweepy
import random

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'vlgFZR0FNwx8LK712NDeuOWIm'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'ox7giq00SMZqpB4tPfM639RsARtiUgESSTOkE2P2eDQfxhHnZZ'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '778961679115845632-SHch5TAREoZIbiv4BBhfPZdqqVF51ZP'#keep the quotes, replace this with your access token
ACCESS_SECRET = '3xSzZdPiaRi00lWEfbajQifQX3mkTMzQrqpKOFjXh32Tu'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

dataList = []
#B = flo R = fjære
lightArray = []
#direction False når det går mot flo, True når det går mot fjære
direction = False
lightTracker = 0
lastChangeTimestamp = 0

def updateTidetxt(tomorrow = False):
    if tomorrow == False:
        # Getting year, month and day and storing them in variables
        # I am doing this because every day i get a new txt document corresponding for tide info for that given day
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)
        # Fixing the formatting of the month and day strings so they work as parameters
        if len(month) == 1:
            month = "0" + month
        day = str(now.day)
        if len(day) == 1:
            day = "0" + day
        # This is the unfinished url for the text document
        url = "http://api.sehavniva.no/tideapi.php?tide_request=locationdata&fromtime=YEAR-MONTH-DAYT00:00&totime=YEAR-MONTH-DAYT23:59&lat=69.647424&lon=18.961323&lang=nb&dst=1&refcode=CD&file=TXT&place=Troms%C3%B8&datatype=TAB"
        # I put the correct parameters into the finished url
        finishedUrl = re.sub("YEAR", year, url)
        finishedUrl = re.sub("YEAR", year, finishedUrl)
        finishedUrl = re.sub("MONTH", month, finishedUrl)
        finishedUrl = re.sub("MONTH", month, finishedUrl)
        finishedUrl = re.sub("DAY", day, finishedUrl)
        finishedUrl = re.sub("DAY", day, finishedUrl)
        downloadLocation = r"C:\Users\Bruker\Documents\floogfjære\tideInfo.txt"

        # This downloads the file
        urllib.request.urlretrieve(finishedUrl, downloadLocation)
        # I get data from the downloaded file
        file = open("tideInfo.txt", "r+")
        lineList = file.readlines()
        file.close()
        newLineList = []
        for i in range(11, len(lineList)):
            newLineList.append(lineList[i])
        # I put data into a new file to make data handling easier
        newFile = open("tide.txt", "w")
        newFile.writelines(newLineList)
        newFile.close
    else:
        # Getting year, month and day and storing them in variables
        # I am doing this because every day i get a new txt document corresponding for tide info for that given day
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        year = str(now.year)
        month = str(now.month)
        # Fixing the formatting of the month and day strings so they work as parameters
        if len(month) == 1:
            month = "0" + month
        day = str(now.day)
        if len(day) == 1:
            day = "0" + day
        # This is the unfinished url for the text document
        url = "http://api.sehavniva.no/tideapi.php?tide_request=locationdata&fromtime=YEAR-MONTH-DAYT00:00&totime=YEAR-MONTH-DAYT23:59&lat=69.647424&lon=18.961323&lang=nb&dst=1&refcode=CD&file=TXT&place=Troms%C3%B8&datatype=TAB"
        # I put the correct parameters into the finished url
        finishedUrl = re.sub("YEAR", year, url)
        finishedUrl = re.sub("YEAR", year, finishedUrl)
        finishedUrl = re.sub("MONTH", month, finishedUrl)
        finishedUrl = re.sub("MONTH", month, finishedUrl)
        finishedUrl = re.sub("DAY", day, finishedUrl)
        finishedUrl = re.sub("DAY", day, finishedUrl)
        downloadLocation = r"C:\Users\Bruker\Documents\floogfjære\tideInfo.txt"

        # This downloads the file
        urllib.request.urlretrieve(finishedUrl, downloadLocation)
        # I get data from the downloaded file
        file = open("tideInfo.txt", "r+")
        lineList = file.readlines()
        file.close()
        newLineList = []
        for i in range(11, len(lineList)):
            newLineList.append(lineList[i])
        # I put data into a new file to make data handling easier
        newFile = open("tide.txt", "w")
        newFile.writelines(newLineList)
        newFile.close

def handleData():
    #I get data from the file and store it in a list
    global dataList
    tideFile = open("tide.txt", "r+")
    lineList = tideFile.readlines()
    for i in range(len(lineList)):
        myList = []
        year = lineList[i][:4]
        month = lineList[i][5:7]
        day = lineList[i][8:10]
        klokke = lineList[i][11:16]
        høyde = lineList[i][-6:-3]
        if " " in høyde:
            høyde = høyde[1:]
        høyde = int(høyde)
        myList.append(year)
        myList.append(month)
        myList.append(day)
        myList.append(klokke)
        myList.append(høyde)
        dataList.append(myList)

    #I determine wether the height of the water indicates flo or fjære
    for t in range(len(dataList)):
        if len(dataList[t]) < 6:
            if t == 0:
                if dataList[t][4] > dataList[t + 1][4]:
                    dataList[t].append("Flo")
                else:
                    dataList[t].append("Fjære")
            else:
                if dataList[t][4] > dataList[t - 1][4]:
                    dataList[t].append("Flo")
                else:
                    dataList[t].append("Fjære")
    #i get the unix timestamp for the specified time
    for a in range(len(dataList)):
        if len(dataList[a]) < 7:
            tempString = dataList[a][0] + " " + dataList[a][1] + " " + dataList[a][2] + " " + dataList[a][3]
            tempDate = datetime.datetime.strptime(tempString, "%Y %m %d %H:%M")
            dataList[a].append(tempDate.timestamp())
#get data of first startup
updateTidetxt()
handleData()
if dataList[0][5] == "Flo":
    direction = True
while True:
    timestampNow = datetime.datetime.now().timestamp()
    if timestampNow > dataList[0][6]:
        msg = dataList[0][0], dataList[0][1], dataList[0][2], dataList[0][3], dataList[0][4], dataList[0][5], \
                dataList[0][6], direction, random.randint(2000, 10000)
        api.update_status(msg)
        # forandre retning på lyset
        direction = not direction
        lastChangeTimestamp = dataList[0][6]
        del dataList[0]
        if len(dataList) == 1:
            updateTidetxt(True)
            handleData()

    if (timestampNow - lastChangeTimestamp) / (dataList[0][6] - lastChangeTimestamp) > 0.8:
        if lightTracker != 1:
            if direction == True:
                    lightArray = ["B", "B", "B"]
            else:
                lightArray = ["R", "R", "R"]
            lightTracker = 1

    elif (timestampNow - lastChangeTimestamp) / (dataList[0][6] - lastChangeTimestamp) > 0.6:
        if lightTracker != 2:
            if direction == True:
                lightArray = ["R", "B", "B"]
            else:
                lightArray = ["R", "R", "B"]
            lightTracker = 2

    elif (timestampNow - lastChangeTimestamp) / (dataList[0][6] - lastChangeTimestamp) > 0.4:
        if lightTracker != 3:
            lightArray = ["R", "O", "B"]
            lightTracker = 3

    elif (timestampNow - lastChangeTimestamp) / (dataList[0][6] - lastChangeTimestamp) > 0.2:
        if lightTracker != 4:
            if direction == True:
                lightArray = ["R", "R", "B"]
            else:
                lightArray = ["R", "B", "B"]
            lightTracker = 4

    elif (timestampNow - lastChangeTimestamp) / (dataList[0][6] - lastChangeTimestamp) > 0:
        if lightTracker != 5:
            if direction == True:
                lightArray = ["R", "R", "R"]
            else:
                lightArray = ["B", "B", "B"]
            lightTracker = 5
    else:
        msg = "This is not supposed to happen", random.randint(1, 10000)
        api.update_status(msg)

    if lightArray != []:
        now = datetime.datetime.now()
        msg = now, lightArray, random.randint(2000, 10000)
        api.update_status(msg)

    lightArray = []
    time.sleep(30)