import requests
from bs4 import BeautifulSoup
import json
import os

def writeCoursesJSONFile(filePath, overviewData, overviewTable, reqData, skillsData):

    data = {
        'Overview text': overviewData,
        'Overview table': overviewTable,
        'Entry and participation requirements': reqData,
        'Attribute, outcomes and skills': skillsData
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def parseOverviewTable(table):

    jsonData = {}

    rows = table.find_all('tr')
    for row in rows:
        header = row.find('th').get_text(strip=True)
        data = row.find('td').get_text(strip=True)

        jsonData[header] = data

    return jsonData

def scrapeOverview(url):

    overviewText = []
    overviewTable = None

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #scrap subject details
    overviewData = soup.find('div', class_='sidebar-tabs__panel')

    header = overviewData.find('h2')
    stopDiv = overviewData.find('div', class_='course__overview-box-links')

    #start at the header and go down, and stop when reaching the stop div
    nextElem = header.find_next()
    while nextElem != stopDiv:

        nextElem = nextElem.find_next()

        if hasattr(nextElem, 'name') and nextElem.name == 'p':
            overviewText.append(nextElem.get_text(strip=True))

        if hasattr(nextElem, 'name') and nextElem.name == 'table':
            overviewTable = parseOverviewTable(nextElem)

    courseName = overviewTable['Award title'].replace(" ", '') 

    return overviewText, overviewTable, courseName

def titleSearcherReq(lst):

    """(helper) function will look for the header containing [Entry requirements] and 
    [Inherent requirements (core participation requirements)] and return the list of elements."""
    targetList = []

    for item in lst:
        if hasattr(item, 'get_text') and item.get_text() == 'Entry requirements':
            targetList.append(item)

        if (hasattr(item, 'get_text') and item.get_text() == 
            'Inherent requirements (core participation requirements)'):

            targetList.append(item)

    return targetList        

def parseUL(ul):

    ulText = []
    lis = ul.find_all('li')

    for li in lis:
        ulText.append(li.get_text())

    return ulText    

def parseOL(ol):

    olText = []
    lis = ol.find_all('li')
    index = 1

    for li in lis:
        olText.append(str(index) + '. ' + li.get_text())
        index += 1

    return olText    

def scrapeReq(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #scrap subject details
    reqDiv = soup.find('div', class_='sidebar-tabs__panel')

    h2s = reqDiv.find_all('h2')
    stopDiv = soup.find('div', 'course__prev-next-buttons')

    #look for [entry requirements] and [inherent requirements...]
    headers = titleSearcherReq(h2s)

    reqData = {}

    for header in headers:
        
        headerText = header.get_text(strip=True)
        nextElem = header.find_next()

        textData = []

        while (nextElem != stopDiv and nextElem not in headers):
            
            if hasattr(nextElem, 'name') and nextElem.name == 'p':
                text = nextElem.get_text(strip=True)
                if text != '':
                    textData.append(text)

            if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                textData.extend(parseUL(nextElem))    

            if hasattr(nextElem, 'name') and nextElem.name == 'ol':
                textData.extend(parseOL(nextElem))

            nextElem = nextElem.find_next()

        reqData[headerText] = textData

    return reqData    

def titleSearcherSkills(lst):
    
    """(helper) function will look for the header containing [Professional accreditation] and 
    return the list of elements."""
    targetList = []

    for item in lst:
        if hasattr(item, 'get_text') and item.get_text() == 'Professional accreditation':
            targetList.append(item)

    return targetList      
    

def scrapeSkills(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    skillsContainer = soup.find('div', class_='sidebar-tabs__panel')

    headers = titleSearcherSkills(skillsContainer.find_all('h2'))
    stopDiv = skillsContainer.find('div', id='learning-outcomes')

    skillsData = {}

    for header in headers:
        
        headerText = header.get_text(strip=True)
        nextElem = header.find_next()

        textData = []

        while (nextElem != stopDiv and nextElem not in headers):

            if hasattr(nextElem, 'name') and nextElem.name == 'p':
                text = nextElem.get_text(strip=True)
                if text != '':
                    textData.append(text)

            if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                textData.extend(parseUL(nextElem))    

            if hasattr(nextElem, 'name') and nextElem.name == 'ol':
                textData.extend(parseOL(nextElem))

            nextElem = nextElem.find_next()

        skillsData[headerText] = textData

    return skillsData    


def scrapeCourses(url):


    #https://handbook.unimelb.edu.au/courses/b-sci
    overviewText, overviewTable, courseName = scrapeOverview(url)

    #https://handbook.unimelb.edu.au/2024/courses/b-sci/entry-participation-requirements
    reqData = scrapeReq(url + '/entry-participation-requirements')

    #https://handbook.unimelb.edu.au/2024/courses/b-sci/attributes-outcomes-skills
    skillsData = scrapeSkills(url + '/attributes-outcomes-skills')

    #writing to JSON file
    fileName = courseName + '_info.json'
    filePath = os.path.join('courseInfo', fileName)

    writeCoursesJSONFile(filePath, overviewText, overviewTable, reqData, skillsData)