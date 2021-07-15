import requests
from datetime import timedelta, datetime
import json

us_state_abbrev_full = {
    'AL':'alabama',
    'AK':'alaska',
    'AS':'american samoa',
    'AZ': 'arizona',
    'AR': 'arkansas',
    'CA': 'california',
    'CO': 'colorado',
    'CT': 'connecticut',
    'DE': 'delaware',
    'DC': 'district of columbia',
    'FL': 'florida',
    'GA': 'georgia',
    'GU': 'guam',
    'HI': 'hawaii',
    'ID': 'idaho',
    'IL': 'illinois',
    'IN': 'indiana',
    'IA': 'iowa',
    'KS': 'kansas',
    'KY': 'kentucky',
    'LA': 'louisiana',
    'ME': 'maine',
    'MD': 'maryland',
    'MA': 'massachusetts',
    'MI': 'michigan',
    'MN': 'minnesota',
    'MS': 'mississippi',
    'MO': 'missouri',
    'MT': 'montana',
    'NE': 'nebraska',
    'NV': 'nevada',
    'NH': 'new hampshire',
    'NJ': 'new jersey',
    'NM': 'new mexico',
    'NY': 'new york',
    'NC': 'north carolina',
    'ND': 'north dakota',
    'MP': 'northern mariana islands',
    'OH': 'ohio',
    'OK': 'oklahoma',
    'OR': 'oregon',
    'PA': 'pennsylvania',
    'PR': 'puerto rico',
    'RI': 'rhode island',
    'SC': 'south carolina',
    'SD': 'south dakota',
    'TN': 'tennessee',
    'TX': 'texas',
    'UT': 'utah',
    'VT': 'vermont',
    'VI': 'virgin islands',
    'VA': 'virginia',
    'WA': 'washington',
    'WV': 'west virginia',
    'WI': 'wisconsin',
    'WY': 'wyoming'
}

us_state_primaryAirport = {
    'alabama': ['KBHM','KDHN','KHSV','KMOB','KMGM'],
    'alaska': ['PALH','PAMR','PANC','PANI','PABE','PACV','PASC','PADL','PAFA','PAGS','PAHO','PAJN','PAEN','PAKT','PAKN','PAKW','PADQ','PAOT','PAOM','PAPG','PASM','PASI','PAUN','PADU','PABR','PAVD','PAWG','PAYA'],
    'american samoa': ['NSTU'],
    'arizona': ['KIFP','KFLG','KGCN','KIWA','KPGA','KPHX','KPRC','KTUS','KNYL'],
    'arkansas': ['KXNA','KFSM','KLIT','KTXK'],
    'california': ['KACV','KBFL','KBUR','KCCR','KFAT','KLGB','KLAX','KMMH','KMRY','KOAK','KONT','KSNA','KPSP','KRDD','KSMF','KSAN','KSFO','KSJC','KSBP','KSBA','KSMX','KSTS','KSCK'],
    'colorado': ['KASE','KCOS','KDEN','KDRO','KEGE','KGJT','KGUC','KHDN','KMTJ','KPUB'],
    'connecticut': ['KBDL','KHVN'],
    'delaware': ['KEVY','KILG','KGED','KDOV'],
    'district of columbia': [], # None
    'florida': ['KDAB','KFLL','KRSW','KVPS','KGNV','KJAX','KEYW','KMLB','KMIA','KMCO','KECP','KPNS','KPGD','KSFB','KSRQ','KSGJ','KPIE','KTLH','KTPA','KPBI'],
    'georgia': ['KABY','KATL','KAGS','KBQK','KCSG','KMCN','KSAV','KVLD'],
    'guam': ['PGUM'],
    'hawaii': ['PHTO','PHNL','PHOG','PHKO','PHMK','PHNY','PHLI'],
    'idaho': ['KBOI','KSUN','KIDA','KLWS','KPIH','KTWF'],
    'illinois': ['KBLV','KBMI','KCMI','KMDW','KORD','KMWA','KMLI','KPIA','KUIN','KRFD','KSPI'],
    'indiana': ['KEVV','KFWA','KIND','KSBN'],
    'iowa': ['KCID','KDSM','KDBQ','KSUX','KALO'],
    'kansas': ['KGCK','KHYS','KMHK','KSLN','KICT'],
    'kentucky': ['KCVG','KLEX','KSDF','KOWB','KPAH'],
    'louisiana': ['KAEX','KBTR','KLFT','KLCH','KMLU','KMSY','KSHV'],
    'maine': ['KBGR','KPWM','KPQI','KRKD'],
    'maryland': ['KBWI','KHGR','KSBY'],
    'massachusetts': ['KBED','KBOS','KHYA','KACK','KPVC','KMVY','KORH'],
    'michigan': ['KAPN','KDTW','KESC','KFNT','KGRR','KCMX','KIMT','KAZO','KLAN','KSAW','KMKG','KPLN','KMBS','KCIU','KTVC'],
    'minnesota': ['KBJI','KBRD','KDLH','KHIB','KINL','KMSP','KRST','KSTC'],
    'mississippi': ['KGTR','KGPT','KJAN','KMEI','KTUP'],
    'missouri': ['KCOU','KJLN','KMCI','KSGF','KSTL'],
    'montana': ['KBIL','KBZN','KBTM','KGTF','KHLN','KGPI','KMSO','KSDY','KWYS'],
    'nebraska': ['KGRI','KLNK','KLBF','KOMA','KBFF'] ,
    'nevada': ['KBVU','KEKO','KLAS','KRNO'],
    'new hampshire': ['KLEB','KMHT','KPSM'],
    'new jersey': ['KACY','KEWR','KTTN'],
    'new mexico': ['KABQ','KHOB','KROW','KSAF'],
    'new york': ['KALB','KBGM','KBUF','KELM','KISP','KITH','KJFK','KLGA','KSWF','KIAG','KOGS','KPBG','KROC','KSYR','KART','KHPN'],
    'north carolina': ['KAVL','KCLT','KJQF','KFAY','KGSO','KPGV','KOAJ','KEWN','KRDU','KILM'],
    'north dakota': ['KBIS','KDIK','KFAR','KGFK','KJMS','KMOT','KXWA'],
    'northern mariana islands': ['PGSN','PGRO','PGWT'],
    'ohio': ['KCAK','KCLE','KCMH','KLCK','KDAY','KTOL'],
    'oklahoma': ['KLAW','KOKC','KSWO','KTUL'],
    'oregon': ['KEUG','KMFR','KOTH','KPDX','KRDM'],
    'pennsylvania': ['KABE','KERI','KMDT','KLBE','KPHL','KPIT','KUNV','KAVP','KIPT'],
    'puerto rico': ['TJBQ','TJRV','TJCP','TJPS','TJSJ','TJIG','TJVQ'],
    'rhode island': ['KBID','KPVD','KWST'],
    'south carolina': ['KCHS','KCAE','KFLO','KGSP','KHXD','KMYR'],
    'south dakota': ['KABR','KPIR','KRAP','KFSD','KATY'],
    'tennessee': ['KCHA','KTYS','KMEM','KBNA','KTRI'],
    'texas': ['KABI','KAMA','KAUS','KBPT','KBRO','KCLL','KCRP','KDAL','KDFW','KELP','KHRL','KIAH','KHOU','KGRK','KLRD','KGGG','KLBB','KMFE','KMAF','KSJT','KSAT','KTYR','KACT','KSPS'],
    'utah': ['KCDC','KCNY','KOGD','KPVU','KSLC','KSGU','KVEL'],
    'vermont': ['KBTV'],
    'virgin islands': ['TIST','TISX'],
    'virginia': ['KCHO','KLYH','KPHF','KORF','KRIC','KROA','KSHD','KDCA','KIAD'],
    'washington': ['KBLI','KORS','KFHR','KPSC','KPUW','KBFI','KSEA','KGEG','KALW','KEAT','KYKM'],
    'west virginia': ['KCRW','KCKB','KHTS','KLWB'],
    'wisconsin': ['KATW','KEAU','KGRB','KLSE','KMSN','KMKE','KCWA','KRHI'],
    'wyoming': ['KCPR','KCOD','KGCC','KJAC','KLAR','KRIW','KRKS','KSHR'],
}


us_state_countFlyingInToArrival = {
    'alabama': 0,
    'alaska': 0,
    'american samoa': 0,
    'arizona': 0,
    'arkansas': 0,
    'california': 0,
    'colorado': 0,
    'connecticut': 0,
    'delaware': 0,
    'district of columbia': 0,
    'florida': 0,
    'georgia': 0,
    'guam': 0,
    'hawaii': 0,
    'idaho': 0,
    'illinois': 0,
    'indiana': 0,
    'iowa': 0,
    'kansas': 0,
    'kentucky': 0,
    'louisiana': 0,
    'maine': 0,
    'maryland': 0,
    'massachusetts': 0,
    'michigan': 0,
    'minnesota': 0,
    'mississippi': 0,
    'missouri': 0,
    'montana': 0,
    'nebraska': 0,
    'nevada': 0,
    'new hampshire': 0,
    'new jersey': 0,
    'new mexico': 0,
    'new york': 0,
    'north carolina': 0,
    'north dakota': 0,
    'northern mariana islands': 0,
    'ohio': 0,
    'oklahoma': 0,
    'oregon': 0,
    'pennsylvania': 0,
    'puerto rico': 0,
    'rhode island': 0,
    'south carolina': 0,
    'south dakota': 0,
    'tennessee': 0,
    'texas': 0,
    'utah': 0,
    'vermont': 0,
    'virgin islands': 0,
    'virginia': 0,
    'washington': 0,
    'west virginia': 0,
    'wisconsin': 0,
    'wyoming': 0,
}

us_state_placesRiskOrNot = {
    'alabama': 0,
    'alaska': 0,
    'american samoa': 0,
    'arizona': 0,
    'arkansas': 0,
    'california': 0,
    'colorado': 0,
    'connecticut': 0,
    'delaware': 0,
    'district of columbia': 0,
    'florida': 0,
    'georgia': 0,
    'guam': 0,
    'hawaii': 0,
    'idaho': 0,
    'illinois': 0,
    'indiana': 0,
    'iowa': 0,
    'kansas': 0,
    'kentucky': 0,
    'louisiana': 0,
    'maine': 0,
    'maryland': 0,
    'massachusetts': 0,
    'michigan': 0,
    'minnesota': 0,
    'mississippi': 0,
    'missouri': 0,
    'montana': 0,
    'nebraska': 0,
    'nevada': 0,
    'new hampshire': 0,
    'new jersey': 0,
    'new mexico': 0,
    'new york': 0,
    'north carolina': 0,
    'north dakota': 0,
    'northern mariana islands': 0,
    'ohio': 0,
    'oklahoma': 0,
    'oregon': 0,
    'pennsylvania': 0,
    'puerto rico': 0,
    'rhode island': 0,
    'south carolina': 0,
    'south dakota': 0,
    'tennessee': 0,
    'texas': 0,
    'utah': 0,
    'vermont': 0,
    'virgin islands': 0,
    'virginia': 0,
    'washington': 0,
    'west virginia': 0,
    'wisconsin': 0,
    'wyoming': 0,
}

us_state_numberOfHighRiskFlight = {
    'alabama': 0,
    'alaska': 0,
    'american samoa': 0,
    'arizona': 0,
    'arkansas': 0,
    'california': 0,
    'colorado': 0,
    'connecticut': 0,
    'delaware': 0,
    'district of columbia': 0,
    'florida': 0,
    'georgia': 0,
    'guam': 0,
    'hawaii': 0,
    'idaho': 0,
    'illinois': 0,
    'indiana': 0,
    'iowa': 0,
    'kansas': 0,
    'kentucky': 0,
    'louisiana': 0,
    'maine': 0,
    'maryland': 0,
    'massachusetts': 0,
    'michigan': 0,
    'minnesota': 0,
    'mississippi': 0,
    'missouri': 0,
    'montana': 0,
    'nebraska': 0,
    'nevada': 0,
    'new hampshire': 0,
    'new jersey': 0,
    'new mexico': 0,
    'new york': 0,
    'north carolina': 0,
    'north dakota': 0,
    'northern mariana islands': 0,
    'ohio': 0,
    'oklahoma': 0,
    'oregon': 0,
    'pennsylvania': 0,
    'puerto rico': 0,
    'rhode island': 0,
    'south carolina': 0,
    'south dakota': 0,
    'tennessee': 0,
    'texas': 0,
    'utah': 0,
    'vermont': 0,
    'virgin islands': 0,
    'virginia': 0,
    'washington': 0,
    'west virginia': 0,
    'wisconsin': 0,
    'wyoming': 0,
}


def getResult(airport,theHighRiskInfectionRate,url,question=''): # Get Result is used in every function below, link with URL to get API information and output
    r = requests.get('http://yliu57:5cd56d79d2ce3ff9ef8351a84aefbe3479ebf0c5@flightxml.flightaware.com/json/FlightXML2/SetMaximumResultSize?max_size=1000')
    r = requests.get(url)
    r = r.json()
    # b = len(r['ArrivedResult']['arrivals'])
    # print('total number of flights: %d\n'%(b))
    
    # Count the number of flights flying into the state from other states
    c = 0 # number of flights of primary airports
    for flight in r['ArrivedResult']['arrivals']:
        icao = flight['origin']
        for key in us_state_primaryAirport:
            if icao in us_state_primaryAirport[key]:
                us_state_countFlyingInToArrival[key] = us_state_countFlyingInToArrival[key]+1;
                c+=1;
    # print('us_state_countFlyingInToArrival: %s\n'%(us_state_countFlyingInToArrival))
    # print('total number of flights of primary airport: %d\n'%(c))
    
    
    # 1.Determine the high-risk places(write 0(Not high-risk) or 1(high-risk) in us_state_placesRiskOrNot) 
    urlCovidAPIKey = "apiKey=ad85ef1a0e9b4ad4aecc0ffe0792549e"
    urlCovid = "https://api.covidactnow.org/v2/states.timeseries.json?" + urlCovidAPIKey
    covid = requests.get(urlCovid)
    covid = covid.json()
    
    yesterday = datetime.today() + timedelta(-1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    theDayBeforeYesterday = datetime.today() + timedelta(-2)
    theDayBeforeYesterday = theDayBeforeYesterday.strftime('%Y-%m-%d')

    # theHighRiskInfectionRate = 1.2   # The theHighRiskInfectionRate is changed to be designed by the user
    
    for state1 in covid:
        state1Break = 0
        for state2 in us_state_abbrev_full:
            state2Break = 0
            if state2 == state1["state"]:
                state1Break = 1
                state2Break = 1
                for dayData in state1["metricsTimeseries"]:
                    if dayData["date"] == yesterday:        # Find the infectionRate data yesterday
                        if dayData["infectionRate"] == None:
                            # Find the infectionRate data the day before yesterday if the infectionRate data yesterday is None
                            for dayDataY in state1["metricsTimeseries"]:    
                                 if dayDataY["date"] == theDayBeforeYesterday:  
                                     if dayDataY["infectionRate"]!= None:
                                        num = float(dayDataY["infectionRate"])
                                        if  num > theHighRiskInfectionRate:
                                            state3 = us_state_abbrev_full[state2]
                                            us_state_placesRiskOrNot[state3] = 1
                                            break
                        if dayData["infectionRate"]!= None:
                            num = float(dayData["infectionRate"])
                            if  num > theHighRiskInfectionRate:
                                state3 = us_state_abbrev_full[state2]
                                us_state_placesRiskOrNot[state3] = 1
                                break
            if state2Break == 1: 
               break
    # print('us_state_placesRiskOrNot: %s\n'%(us_state_placesRiskOrNot))

    # 2.count the number of flights from high-risk places (count the number and store in variable totalNumberFlightsHighRiskInAState)
    # 3.Add the value of totalNumberFlightsHighRiskInAState into the right key in us_state_numberOfHighRiskFlight)
    # Most of states have not only one airport so remember to add together and get the total number
    # Use two-layers loop in us_state_primaryAirport and Arrived() method to caculate
    totalNumberFlightsHighRiskInAState = 0
    for key in us_state_countFlyingInToArrival:
        totalNumberFlightsHighRiskInAState += us_state_countFlyingInToArrival[key] * us_state_placesRiskOrNot[key]
    for state in us_state_primaryAirport:
        if airport in us_state_primaryAirport[state]:
            us_state_numberOfHighRiskFlight[state] += totalNumberFlightsHighRiskInAState
    # FINAL DICTIONARY HERE
    # print('us_state_numberOfHighRiskFlight: %s\n'%(us_state_numberOfHighRiskFlight)) 

    for key in us_state_countFlyingInToArrival:     # refresh the dictionary for the next use
        us_state_countFlyingInToArrival[key] = 0

    # print('Output of GET %s request:\n%s' %(question, r)) # r stores the API information


def Arrived(airport, theHighRiskInfectionRate = 1.2):
    question = 'Arrived?'
    url = 'http://yliu57:5cd56d79d2ce3ff9ef8351a84aefbe3479ebf0c5@flightxml.flightaware.com/json/FlightXML2/' + question
    if airport != None:
        url += 'airport='+ airport
    getResult(airport,theHighRiskInfectionRate,url,question)

# Example:
# Arrived('KIAD')
# Arrived('KIAD',5,'airline',0)
def mainFunction(index,theHighRiskInfectionRate = 1.2):  # default theHighRiskInfectionRate is 1.2
    for key in us_state_numberOfHighRiskFlight:     # refresh the dictionary for the next use
        us_state_numberOfHighRiskFlight[key] = 0
    indexLoop = -1
    dictReturn = {}
    for state in us_state_primaryAirport:
        indexLoop +=1
        if indexLoop == index+1:
            break
        if  indexLoop == index:
            for airport in us_state_primaryAirport[state]:
               Arrived(airport,theHighRiskInfectionRate)
            dictReturn[state] = us_state_numberOfHighRiskFlight[state]
    # Arrived('KIAD')
    # print('us_state_numberOfHighRiskFlight: %s\n'%(us_state_numberOfHighRiskFlight))
    print('dictReturn: %s\n'%(dictReturn))
    # j = json.dumps(dictReturn)
    # return j
    return dictReturn