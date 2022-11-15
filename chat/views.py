from urllib import response
from django.shortcuts import render

from events.models import Event
from .models import Conversation, KeyWords, Phrase
from files.models import Folder
from events.models import Event
import datetime
import random
# Create your views here.
def chat(request):
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
