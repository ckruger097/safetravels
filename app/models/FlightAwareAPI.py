import requests

def getResult(url,question=''): # Get Result is used in every function below, link with URL to get API information and output
    r = requests.get(url)
    r = r.json()

    print('Output of GET %s request:\n%s' %(question, r)) # r stores the API information

def FlightInfoEx(ident,howMany=1,offset=0):
    question = 'FlightInfoEx?'
    url = 'http://yliu57:5cd56d79d2ce3ff9ef8351a84aefbe3479ebf0c5@flightxml.flightaware.com/json/FlightXML2/' + question
    if ident != None:
        url += 'ident='+ ident 
    if howMany != None:
        if ident != None:
            url += '&'
        url += 'howMany='+ ('%s'%(howMany))
    if offset != None:
        if ident != None or howMany != None :
            url += '&'
        url += 'offset='+  ('%s'%(offset))
    getResult(url,question)

# Example:
# FlightInfoEx('UAL2507',15,0)
# FlightInfoEx('UAL2507')


def Arrived(airport, howMany=1, filter='', offset=0):
    question = 'Arrived?'
    url = 'http://yliu57:5cd56d79d2ce3ff9ef8351a84aefbe3479ebf0c5@flightxml.flightaware.com/json/FlightXML2/' + question
    if airport != None:
        url += 'airport='+ airport
    if howMany != None:
        if airport != None:
            url += '&'
        url += 'howMany='+ ('%s'%(howMany))
    if filter != None:
        if airport != None or howMany != None:
            url += '&'
        url += 'filter='+ ('%s'%(filter))
    if offset != None:
        if airport != None or howMany != None or filter != None:
            url += '&'
        url += 'offset='+ ('%s'%(offset))
    getResult(url,question)

# Example:
Arrived('KIAD',5)
Arrived('KIAD',5,'airline',0)


def Departed(airport, howMany=1, filter='', offset=0):
    question = 'Departed?'
    url = 'http://yliu57:5cd56d79d2ce3ff9ef8351a84aefbe3479ebf0c5@flightxml.flightaware.com/json/FlightXML2/' + question
    if airport != None:
        url += 'airport='+ airport
    if howMany != None:
        if airport != None:
            url += '&'
        url += 'howMany='+ ('%s'%(howMany))
    if filter != None:
        if airport != None or howMany != None:
            url += '&'
        url += 'filter='+ ('%s'%(filter))
    if offset != None:
        if airport != None or howMany != None or filter != None:
            url += '&'
        url += 'offset='+ ('%s'%(offset))
    getResult(url,question)


# Example:
# Departed('KIAD',5)
# Departed('KIAD',5,'airline',0)