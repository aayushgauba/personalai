from datetime import datetime
from django.shortcuts import render, redirect
from .models import Event
from .forms import EditForm
import datetime
# Create your views here.
def events(request):
    calenderArray = calender()
    date = getDate()
    month = monthName(int(date[1]))
    calenderArray = eventArray(calenderArray, month)
    year = getYear()
    dateSet =[]
    count = 0
    if calenderArray[0]['week'] != 0:
        count = 0
        while count <= calenderArray[0]['week']:
            dateSet.append(count)
            count+=1


    context = {
        'year':year,
        'month':month,
        'calender':calenderArray,
        'dateSet':dateSet,
    }
    return render(request, "events.html", context)

def getDictFromDayAndWeek(calender, day, week):
    temp = calender[day-1]
    array = []
    for item in calender:
        if(item["event"] == True):
            array.append(item)
    for item in array:
        if(item["week"] == week and item["day"] == day):
            temp = item
    return temp

def querysetArray(array):
    queryArray =[]
    for item in array:
        event = Event.objects.get(id = item)
        print
        temp = {}
        temp["id"] = event.id
        temp["Title"] = event.Title
        temp["Date"] = event.Date
        temp["Notes"] = event.Notes
        queryArray.append(temp)
    return queryArray

def event(request, day, week):
    calenderArray = calender()
    dict = getDictFromDayAndWeek(calenderArray, day, week)
    month = monthName(int(dict["month"]))
    calenderArray = eventArray(calenderArray, month)
    year = dict["year"]
    day = dict["day"]
    calenderArray = querysetArray(dict["list"])
    context = {
        'week':week,
        'day':day,
        'year':year,
        'month':month,
        'calender':calenderArray,
    }    
    return render(request, "event.html", context)

def returnDateEvent(origDate):
    year = origDate[0]+origDate[1]+origDate[2]+origDate[3]
    date = ""
    month = ""

    if(origDate[4] == "-" and origDate[7] == "-"):
        date = origDate[5]+origDate[6]
    elif(origDate[4] == "-" and origDate[6] == "-"):
        date = origDate[5]
    if(len(origDate)-1 == 8):
        month = origDate[8]
    elif(len(origDate)-1 == 9):
        month = origDate[8]+ origDate[9]
    totalDate = year + "-" + date + "-" + month
    return totalDate

def eventEdit(request, day, week, event_id):
    event = Event.objects.get(id = event_id)
    form = EditForm({'Title':event.Title, 'Date':event.Date, 'Notes':event.Notes})
    if request.method == "POST":
        date = returnDateEvent(str(request.POST.get("Date")))
        print(date)
        title = request.POST.get("Title")
        notes = request.POST.get("Notes")
        event.Date = date
        event.Title = title
        event.Notes = notes
        event.save()
        return redirect("events")
    return render(request, "eventEdit.html", context = {'form':form})

def eventDelete(request, event_id):
    event = Event.objects.get(id = event_id)
    event.delete()
    return redirect("events")

def eventItem(request, day, week, event_id):

    event = Event.objects.get(id = event_id)
    context = {
        'day':day,
        'week':week,
        'event':event
    }
    return render(request, "eventView.html", context)

def monthName(month):
    if month == 1:
        return "January"
    elif month == 2:
        return "February"
    elif month == 3:
        return "March"
    elif month == 4:
        return "April"
    elif month == 5:
        return "May"                    
    elif month == 6:
        return "June"
    elif month == 7:
        return "July"
    elif month == 8:
        return "August"
    elif month == 9:
        return "September"
    elif month == 10:
        return "October"
    elif month == 11:
        return "November"
    elif month == 12:
        return "December"

def monthString(month):
    month = str(month)
    if month == "January":
        return 1
    elif month == "February":
        return 2
    elif month == "March":
        return 3
    elif month == "April":
        return 4
    elif month == "May":
        return 5                     
    elif month == "June":
        return 6
    elif month == "July":
        return 7
    elif month == "August":
        return 8
    elif month == "September":
        return 9
    elif month == "October":
        return 10
    elif month == "November":
        return 11
    elif month == "December":
        return 12

def eventArray(arrayofDict, month):
    events = Event.objects.all()
    print(events)
    for event in events:
        if(getYearFromDate(str(event.Date)) == getYear()):
            for item in arrayofDict:
                if(int(getMonth(event.Date)) == int(monthString(month))):
                    print(int(getDayFromDate(event.Date)))
                    if(int(getDayFromDate(event.Date)) == int(item["day"])):
                        item["list"].append(event.id)
                        item["event"] = True
    return arrayofDict

def createDict(array, year, month):
    dictArray = []
    for item in array:
        Dict = {}
        Dict["week"] = item[0]
        Dict["day"] = item[1]
        Dict["isCurrent"] = False
        Dict["list"] = []
        Dict["event"] = False
        Dict["year"] = year
        Dict["month"] = month
        dictArray.append(Dict)
    return dictArray    

def getDate():
    dateFull = datetime.datetime.now()
    strDate = str(dateFull)
    count =0
    dateArray = []
    temp = ""
    while(count < len(strDate)):
        if(strDate[count] == "-"):
            dateArray.append(temp)
            temp = ""
        elif(strDate[count] == " "):
            dateArray.append(temp)
            break
        else:
            temp +=strDate[count]
        count+=1
    return dateArray

def getNumDays(month):
    month = int(month)
    if(month == 1):
        return 31
    elif(month == 2):
        if(month%4 ==0):
            return 29
        else:
            return 28
    elif(month == 3):
        return 31
    elif(month == 4):
        return 30
    elif(month == 5):
        return 31
    elif(month == 6):
        return 30
    elif(month == 7):
        return 31
    elif(month == 8):
        return 31
    elif(month == 9):
        return 30
    elif(month == 10):
        return 31
    elif(month == 11):
        return 30
    elif(month == 12):
        return 31

def getFirstDayOfTheMonth():
    dateArray = getDate()
    date = convertDate(datetime.datetime.now())
    month = getMonth(date)
    
def getMonth(date):
    date = str(date)
    if(date[4] == "-" and date[6] == "-"):
        return date[5]
    elif(date[4] == "-" and date[7] == "-"):
        return date[5] + date[6]
        
def getDay():
    dateArray = getDate()
    date = int(dateArray[2])
    return date

def getYear():
    date = getDate()
    year = date[0]
    return year

def convertDate(date):
    newDate = ""
    date = str(date)
    count =len(str(date))-1
    if(date[4] != "-"):
        count =len(str(date))-1
        num = 0
        while(count>=num):
            if(date[count] == "/"):
                newDate += "-"    
            else:
                newDate += date[count]
            count-=1
    else:
        count =0
        num = 9
        while(count<=num):
            if(date[count] == "/"):
                newDate += "-"    
            else:
                newDate += date[count]
            count+=1
    return newDate

def setPreviousDays(array, elem):
    if elem == -1:
        return array
    elif elem > -1:
        if(array[elem + 1][0] == 0):
            array[elem][0] = 6
            return setPreviousDays(array, elem-1)
        elif(array[elem + 1][0] >= 0 and array[elem+ 1][0] <= 6):
            array[elem][0] = array[elem+1][0] -1
            return setPreviousDays(array, elem-1)
            
def setNextDays(array, elem):
    while(elem < len(array)):
        if(array[elem-1][0] == 6):
            array[elem][0] = 0
        else:
            array[elem][0] = array[elem-1][0] +1
        elem+=1
    return array

def getDayFromDate(date):
    date = str(date)
    if(len(date) == 10):
        day = date[8]+date[9]
        return day
    elif(len(date) == 9):
        day = date[8]
        return day

def getYearFromDate(date):
    date = str(date)
    year = date[0]+ date[1]+ date[2]+ date[3]
    return year

def calender():
    array = [[0,'Mon'],[1,'Tues'],[2,'Wed'],[3,'Thurs'],[4,'Fri'],[5,'Sat'], [6,'Sun']]
    date = convertDate(datetime.datetime.now())
    month = getMonth(date)
    numDays = getNumDays(month)
    monthArray = []
    for count in range(1,numDays+1):
        tempArray = [-1, count]
        monthArray.append(tempArray)
    currElem = getDay()-1
    monthArray[currElem][0] = datetime.datetime.now().weekday()
    monthArray = setPreviousDays(monthArray, currElem-1)
    monthArray = setNextDays(monthArray, currElem+1)
    year = getYearFromDate(date)
    monthDictArray = createDict(monthArray, year, month)
    monthDictArray[currElem]['isCurrent'] = True
    return monthDictArray