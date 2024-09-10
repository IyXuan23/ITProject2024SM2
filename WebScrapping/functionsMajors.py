import requests
from bs4 import BeautifulSoup
import json
import os

from functions import parseTable
from functionsCourses import parseA, parseOL, parseUL, parsePara, scrapeMajorText

def writeMajorJSONFile(filePath, name, overview, ilo, structureData):

    data = {
        "major name": name,
        "overview": overview,
        "ILOs": ilo,
        "structure": structureData
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def saveMajorLinks(fileName, targetArray):

    filePath = os.path.join('linkStorage', fileName)
    #store in json for quick access
    with open(filePath, 'w') as json_file:

        data = {'links': targetArray}

        json.dump(data, json_file, indent=4)

def checkForMajorMinorSpec(element):

    if hasattr(element, 'name'):

        if (element.name == 'h1' or element.name == 'h2' or element.name == 'h3' 
        or element.name == 'h4'):

            title = element.get_text().lower()
            if ('majors' in title or 'major' in title):
                return 'major'
            elif ('minor' in title or 'minors' in title):
                return 'minor'
            elif ('specialisation'in title or 'specialistions' in title or 'discipline' in title or 'disciplines' in title):
                return 'spec'

    return None

def parseMajorTableLinks(table):
    
    links = []

    rows = table.find_all('tr')[1:]
    for row in rows:
        tds = row.find_all('td')
        
        a = tds[0].find('a')
        if a == None:
            continue

        pair = [a.get_text(strip=True), ('https://handbook.unimelb.edu.au' + a.get('href'))]
        print(pair)

        links.append(pair)

    return links    

def getMajorLinks(links):

    """from the list of all possible course links, we shall get a list of possible majors"""

    majorsLinks = []

    for url in links:

        print(url[2])
        
        majorSpecialisationURL = url[2] + '/majors-minors-specialisations'

        response = requests.get(majorSpecialisationURL)
        soup = BeautifulSoup(response.text, 'html.parser')

        #subject has a majors/minors/specialisations page
        if response.url == majorSpecialisationURL:

            #look for the table holding all the majors
            tableList = soup.find_all('table')
            
            if len(tableList) > 0:

                for table in tableList:
                    prevElem = table.find_previous()
                    
                    #loop until we find a classification for the table
                    while checkForMajorMinorSpec(prevElem) == None:
                        prevElem = prevElem.find_previous()

                    tableType = checkForMajorMinorSpec(prevElem)
                    if tableType == 'major':
                        links = parseMajorTableLinks(table)
                        majorsLinks.extend(links)

                    if tableType == 'minor':
                        print('minor')
                    if tableType == 'spec':
                        print('spec')

    #get the uniques, discard the rest
    uniqueNames = {}
    for name, link in majorsLinks:
        if name not in uniqueNames:
            uniqueNames[name] = link

    uniqueNames = list(uniqueNames.items())

    saveMajorLinks('majorLinks.json', uniqueNames)

def scrapeMajorOverview(soup):

    headerText = []
    ILOs = []

    headers = soup.find_all('h2')
    
    overviewHeader = soup.find('h2', text='Overview')
    stopDiv = soup.find('div', class_='course__prev-next-buttons')

    nextElem = overviewHeader.find_next()

    while nextElem not in headers and nextElem != stopDiv:
        txt = scrapeMajorText(nextElem)
        if txt != None and txt != '':
            headerText.append(txt)
        nextElem = nextElem.find_next()
    
    ILODiv = soup.find('div', id='learning-outcomes')
    if ILODiv != None:
        for elements in ILODiv.contents:
            scrapeMajorText(nextElem)
            if txt != None and txt != '':
                ILOs.append(txt)

    return headerText, ILOs            

def scrapeMajorStructure(url):


    structureText = {}

    structureLink = url.replace('/print', '/course-structure')

    response = requests.get(structureLink)
    soup = BeautifulSoup(response.text, 'html.parser')

    if response.url != structureLink:
        return []

    container = soup.find('div', class_='sidebar-tabs__panel')

    headers = container.find_all('h1')
    headers.extend(container.find_all('h2'))
    headers.extend(container.find_all('h3'))
    headers.extend(container.find_all('h4'))

    stopDiv = soup.find('div', class_='course__prev-next-buttons')

    for header in headers:
        
        headerContent = []

        headerName = header.get_text()
        nextElem = header.find_next()
        while nextElem not in headers and nextElem != stopDiv:
            txt = scrapeMajorText(nextElem)
            if txt != '' and txt != None:
                headerContent.append(txt)
            nextElem = nextElem.find_next()        

        structureText[headerName] = headerContent

    return structureText
    

def scrapeMajorInformation(links):    
    
    for link in links:
        
        #note link[0] is the name, link[1] is the url
        response = requests.get(link[1])
        soup = BeautifulSoup(response.text, 'html.parser')

        overview, ilo = scrapeMajorOverview(soup)
        structureData = scrapeMajorStructure(link[1])

        fileName = link[0] + '_info.json'
        fileName = fileName.replace('/', '-')

        filePath = os.path.join('majorInfo', fileName)

        writeMajorJSONFile(filePath, link[0], overview, ilo, structureData)
        print('scrapped' + link[0])