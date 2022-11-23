from urllib import response
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from events.models import Event
from .models import Conversation, KeyWords, Phrase
from files.models import Folder
from events.models import Event
import datetime
import random
from events.views import getDayFromDate, getDay, calender, getDate
# Create your views here.

def responseDay():
    date = getDate()
    events = Event.objects.all().filter(Date = str(str(date[0])+"-"+str(date[1])+"-"+str(date[2])))
    day = str(datetime.datetime.now())[8]+str(datetime.datetime.now())[9]
    response = ""
    # print(calenderArray)
    # for item in calenderArray:
    #     if(str(item["day"])):
    #         print(item)
    #         print(len(item["list"]))
    #         if(len(item["list"]) > 0):
    #             response = "You have " + len(item["list"]) + "events in your schedule"
    if(events.count()==1):
        response = " You have " + str(events.count()) + " event in your schedule"
    elif(events.count()>1):
        response = " You have " + str(events.count()) + " events in your schedule"
    return response


def chat(request):
    getWeather("maryland heights")
    conversation = Conversation.objects.all().order_by("time")
    if request.method == "POST":
        response = request.POST.get("response")
        Conversation.objects.create(response = response, time = datetime.datetime.now(), sender = "Aayush")
        conversationarray = wordToArr(response)
        think(conversationarray, response)
        conversation = Conversation.objects.all().order_by("time")
    return render(request, 'chat.html', context={'conversation':conversation})


def ArrtoWord(array):
    word = ""
    counter = 0
    while(counter<len(array)-1):
        array[counter] = array[counter]+" "
        counter+=1
    
    for item in array:
        word+=item.lower()
    print(word)
    return word

def safetyProtocols(protocol):
    if(protocol.lower() == "chatclear"):
        conversations = Conversation.objects.all()
        for converse in conversations:
            converse.delete()
    if(protocol.lower() == "lockdown"):
        folders = Folder.objects.all()
        for folder in folders:
            folder.Type = True
            folder.save()

def wordToArr(word):
    counter =0
    newWord = ""
    array =[]
    while(counter < len(word)):
        if(word[counter] == " "):
            array.append(newWord.lower())
            newWord = ""
        else:
            newWord+=word[counter]
        counter+=1
    array.append(newWord)
    return array

def returnKeyIdArray(queryset):
    returnArray = []
    for item in queryset:
        returnArray.append(item.id)
    return returnArray

def returnKeyArray(queryset):
    returnArray = []
    for item in queryset:
        returnArray.append(item.Key.lower())
    return returnArray

def findKeyWordPos(sentenceArray):
    queryArray = []
    index = -1
    for item in KeyWords.objects.all():
        queryArray.append(item.Key.lower())
    for item in sentenceArray:
        for obj in queryArray:
            if(item.lower() == obj.lower()):
                index = sentenceArray.index(item)
    return index

def rephraseQues(question):
    quesArray = wordToArr(question)
    index = findKeyWordPos(quesArray)
    elem = quesArray[index]
    quesArray.pop(index)
    newQuesArray = []
    newQuesArray.append(elem)
    for item in quesArray:
        newQuesArray.append(item)
    word = ArrtoWord(newQuesArray)
    return word

def querysetToArr(queryset):
    queryArray = []
    for item in queryset:
        itemArray = []
        itemArray.append(item.response)
        itemArray.append(item.sender)
        queryArray.append(itemArray)
    return queryArray

def quesOrAns(response):
    ansArray = wordToArr(response)
    index = findKeyWordPos(ansArray)
    if(index == -1):
        return False
    else:
        return True

def convertDate(date):
    count =0
    dateArray = []
    temp = ""
    while count < len(date):
        if date[count] == "/":
            dateArray.append(temp)
            temp = ""
            count+=1
        else:
            temp+=date[count]
            count+=1
    dateArray.append(temp)
    newDate = dateArray[2]+"-"+dateArray[0]+"-"+dateArray[1]

    return newDate

def returnName(response):
    wordArray = wordToArr(response)
    if(wordArray[1].lower() == 'event'):
        ind = wordArray.index("on")
        nameArray = wordArray[2:ind]
        name = ArrtoWord(nameArray)
        return name

def returnTitle(response):
    wordArray = wordToArr(response)
    if(wordArray[2].lower() == 'event'):
        ind = wordArray.index("note")
        nameArray = wordArray[3:ind]
        name = ArrtoWord(nameArray)
        return name    

def returnDate(response):
    wordArray = wordToArr(response)
    ind = wordArray.index("on")
    return wordArray[ind+1]

def returnNote(response):
    wordArray = wordToArr(response)
    if(wordArray[2].lower() == 'event'):
        ind = wordArray.index("note")
        nameArray = wordArray[ind+1:len(wordArray)]
        name = ArrtoWord(nameArray)
        return name    

def farenheitToCelcius(temp):
    tempWord = ""
    print(temp)
    if(len(temp) == 4):
        tempWord = temp[0]+temp[1]
    elif(len(temp) == 3):
        tempWord = temp[0]
    elif(len(temp) == 5):
        tempWord = temp[0]+temp[1]+temp[2]
    celcius = int(((int(tempWord)-32)/1.8))
    return str(celcius)

def tempAnalysis(temp):
    temp = int(temp)
    if(temp < 5):
        return "I reccommend that you wear a jacket and full Tshirt possibly a woolen one."
    elif(temp>=5 and temp < 15):
        return "I reccommend that you wear a full Tshirt."
    elif(temp > 15):
        return "I reccommend that you wear a half Tshirt."

def getWeather(city):    
    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content
    
    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    # print(temp)
    temp = farenheitToCelcius(temp)
    print(temp)
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    # formatting data
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    
    # getting all div tag
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    
    # getting other required data
    pos = strd.find('Wind')
    other_data = strd[pos:]
    dict = {}
    dict["Temperature"] = temp
    dict["Time"] = time
    dict["Sky"] = sky
    dict["otherdata"] = other_data
    # printing all data
    return dict

def compiler(response):
    commandArray = wordToArr(response)
    if(commandArray[0].lower() == 'create'):
        if(commandArray[1].lower() == 'directory'):
            Folder.objects.create(Name = commandArray[2], Type = False)
            Conversation.objects.create(response = "Done", time = datetime.datetime.now(), sender = "Mac")
            conversation = Conversation.objects.all().order_by("time")
        elif(commandArray[1].lower() == 'secure'):
            if(commandArray[2].lower() == 'directory'):
                Folder.objects.create(Name = commandArray[3], Type = True)
                Conversation.objects.create(response = "Done", time = datetime.datetime.now(), sender = "Mac")
                conversation = Conversation.objects.all().order_by("time")
        elif(commandArray[1].lower() == 'event'):
            Event.objects.create(Title = returnName(response), Date = convertDate(returnDate(response)), Notes = "")
            Conversation.objects.create(response = "Done", time = datetime.datetime.now(), sender = "Mac")
            conversation = Conversation.objects.all().order_by("time")
    elif(commandArray[0].lower() == 'execute'):
        safetyProtocols(commandArray[1].lower())
    elif(commandArray[0].lower() == 'add'):
        if(commandArray[2].lower() == 'event'):
            eventName = returnTitle(response)
            event = Event.objects.get(Title = eventName)
            note = returnNote(response)
            event.Notes = note
            event.save()


def checkCommand(response):
    commandArray = wordToArr(response)
    if(commandArray[0].lower() == 'create' or commandArray[0].lower() == 'execute' or commandArray[0].lower() == 'add'):
        return True
    else:
        return False

def getTemp(temp):
    if(temp < 15):
        return "cold"
    else:
        return "hot"

def getTime(time):
    now = datetime.datetime.now()
    current_Time = int(now.strftime("%H"))
    current_Time = current_Time - time
    if(current_Time < 0):
        current_Time + 24
    return current_Time    



def think(sentenceArray, response):
    index = findKeyWordPos(sentenceArray)
    if(index != -1):
        if(KeyWords.objects.filter(Key = sentenceArray[index]).count() == 1):
            if(Phrase.objects.filter(Key = sentenceArray[index]).count() == 1):
                Conversation.objects.create(response = Phrase.objects.get(Key = sentenceArray[0]).Ans, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.create(response = Phrase.objects.get(Key = sentenceArray[0]).Ques, time = datetime.datetime.now(), sender = "Mac")
                conversation = Conversation.objects.all().order_by("time")
            elif(Phrase.objects.filter(Key = sentenceArray[index], Ques = rephraseQues(response)).count() != 1 and Phrase.objects.filter(Key = sentenceArray[index], Ques = rephraseQues(response)).count()>0):
                keyArray = returnKeyIdArray(Phrase.objects.filter(Key = sentenceArray[index]))
                select = random.choice(keyArray)
                print(select)
                Conversation.objects.create(response = Phrase.objects.get(id = select).Ans, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.create(response = Phrase.objects.get(id = select).Ques, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
    elif(index == -1 and checkCommand(response) == False):
        queryArray = querysetToArr(Conversation.objects.all())
        quesOrNot = quesOrAns(queryArray[len(queryArray)-1][0])
        if(quesOrNot == False):
            responseArray = wordToArr(queryArray[len(queryArray)-2][0])
            keyIndex = findKeyWordPos(responseArray)
            key = responseArray[keyIndex].lower()
            Phrase.objects.create(Key = key, Ques = queryArray[len(queryArray)-2][0], Ans = queryArray[len(queryArray)-1][0])
    elif(index == -1 and checkCommand(response) == True):
        compiler(response)
    if(sentenceArray[0].lower() == "good"):
        eventString = responseDay()
        if(sentenceArray[1].lower() == "morning"):
            time = getTime(6)
            dict = getWeather("maryland heights")
            temp = dict["Temperature"]
            feel = getTemp(int(temp))
            suggestion = tempAnalysis(temp)         
            if(time >=0 and time <12):                    
                newResponse = response+ " Boss! I hope the day goes good for you. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
            elif(time >=12 and time <5):
                newResponse = response+ " Boss! Good Afternoon. Looks like your day started late. I hope the  rest of your day goes good for you. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
            elif(time >=5):
                newResponse = response+ " Boss! Its more like Good Night. Looks like your day started late. I hope the  rest of your day goes good for you. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
        elif(sentenceArray[1].lower() == "afternoon"):
            time = getTime(6)
            dict = getWeather("maryland heights")
            temp = dict["Temperature"]
            feel = getTemp(int(temp))
            suggestion = tempAnalysis(temp)
            if(time >=0 and time <12):                    
                newResponse = response+ " Boss! Its more like Good Morning. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
            elif(time >=12 and time <5):
                newResponse = response+ " Boss! Good Afternoon. I hope the  rest of your day goes good for you. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
            elif(time >=5):
                newResponse = response+ " Boss! Its more like Good Night. Looks like your day started late. I hope the  rest of your day goes good for you. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
        elif(sentenceArray[1].lower() == "afternoon"):
            time = getTime(6)
            dict = getWeather("maryland heights")
            temp = dict["Temperature"]
            feel = getTemp(int(temp))
            suggestion = tempAnalysis(temp)
            if(time >=0 and time <12):                    
                newResponse = response+ " Boss! Its more like Good Morning. It looks like you are turning nocturnal. I hope you get a good sleep. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
            elif(time >=12 and time <5):
                newResponse = response+ " Boss! Good Afternoon. I hope the  rest of your day goes good for you. I hope you get a good sleep. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")
            elif(time >=5):
                newResponse = response+ " Boss! Its more like Good Night. Looks like your day started late. I hope the  rest of your day goes good for you. The weather will be "+feel+". "+suggestion+eventString
                Conversation.objects.create(response = newResponse, time = datetime.datetime.now(), sender = "Mac")
                Conversation.objects.all().order_by("time")                    
